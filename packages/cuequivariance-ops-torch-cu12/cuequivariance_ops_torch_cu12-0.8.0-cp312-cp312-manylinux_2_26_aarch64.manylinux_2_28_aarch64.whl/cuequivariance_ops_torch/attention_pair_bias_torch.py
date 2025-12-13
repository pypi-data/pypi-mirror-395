# SPDX-FileCopyrightText: Copyright (c) 2024 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: LicenseRef-NvidiaProprietary
#
# NVIDIA CORPORATION, its affiliates and licensors retain all intellectual
# property and proprietary rights in and to this material, related
# documentation and any modifications thereto. Any use, reproduction,
# disclosure or distribution of this material and related documentation
# without an express license agreement from NVIDIA CORPORATION or
# its affiliates is strictly prohibited.

import os
from typing import Optional, Tuple

import torch
import triton
from torch.fx._symbolic_trace import is_fx_tracing

from cuequivariance_ops.triton.pair_bias import (
    pair_bias_linear_mask_forward_kernel,
    pair_bias_mask_forward_kernel,
    pair_bias_norm_linear_mask_forward_kernel,
)
from cuequivariance_ops_torch.fused_layer_norm_torch import (
    Layout,
    _layer_norm_transpose_bwd,
)
from cuequivariance_ops_torch.utils import (
    is_in_export_mode,
    maybe_to,
    nvtx_range_pop,
    nvtx_range_push,
)

CUEQ_ATTENTION_PAIR_BIAS_FALLBACK_THRESHOLD: int = int(
    os.getenv("CUEQ_ATTENTION_PAIR_BIAS_FALLBACK_THRESHOLD", "100")
)


def _attention_pair_bias_mask_torch(
    z: torch.Tensor,
    mask: torch.Tensor,
    w_proj_z: torch.Tensor,
    b_proj_z: Optional[torch.Tensor],
    w_ln: Optional[torch.Tensor],
    b_ln: Optional[torch.Tensor],
    num_heads: int,
    multiplicity: int,
    eps: float,
    inf: float,
    return_z_proj: bool,
    is_cached_z_proj: bool,
) -> tuple[torch.Tensor, Optional[torch.Tensor]]:
    """Original PyTorch implementation of attention pair bias mask."""
    z_dtype = z.dtype
    B_mask = mask.shape[0]
    B_z = z.shape[0]
    mask_with_multiplicity = B_mask == B_z * multiplicity and multiplicity > 1

    if is_cached_z_proj:
        z_proj = z
        w_proj_z = None
        b_proj_z = None
        w_ln = None
        b_ln = None
    else:
        B, U, V, DIM_Z = z.shape
        z_norm = torch.nn.functional.layer_norm(
            z,
            (DIM_Z,),
            weight=maybe_to(w_ln, z_dtype),
            bias=maybe_to(b_ln, z_dtype),
            eps=eps,
        )

        z_proj = torch.nn.functional.linear(
            z_norm, maybe_to(w_proj_z, z_dtype), bias=maybe_to(b_proj_z, z_dtype)
        )
        z_proj = torch.einsum("bijh->bhij", z_proj).contiguous()

    if mask_with_multiplicity:
        z_proj_expanded = z_proj.repeat_interleave(multiplicity, dim=0).contiguous()
    else:
        z_proj_expanded = z_proj

    out = z_proj_expanded + (1.0 - mask[:, None, None].float()) * (-inf)
    out = out.to(z_dtype)

    if not mask_with_multiplicity:
        out = out.repeat_interleave(multiplicity, dim=0).contiguous()

    if return_z_proj:
        z_proj = z_proj.to(z_dtype)
    else:
        z_proj = None

    return out, z_proj


def _attention_pair_bias_torch(
    s: torch.Tensor,
    q: torch.Tensor,
    k: torch.Tensor,
    v: torch.Tensor,
    z: torch.Tensor,
    mask: torch.Tensor,
    num_heads: int,
    w_proj_z: torch.Tensor,
    w_proj_g: torch.Tensor,
    w_proj_o: torch.Tensor,
    w_ln_z: Optional[torch.Tensor],
    b_ln_z: Optional[torch.Tensor],
    b_proj_z: Optional[torch.Tensor] = None,
    b_proj_g: Optional[torch.Tensor] = None,
    b_proj_o: Optional[torch.Tensor] = None,
    inf: float = 1e6,
    eps: float = 1e-5,
    attn_scale: Optional[float] = None,
    return_z_proj: bool = False,
    is_cached_z_proj: bool = False,
    multiplicity: int = 1,
) -> [torch.Tensor, Optional[torch.Tensor]]:
    """Original PyTorch implementation of attention pair bias."""
    B, H, U, D_Q = q.shape

    z_dtype = z.dtype

    bias, z_proj = _attention_pair_bias_mask_torch(
        z,
        mask,
        w_proj_z,
        b_proj_z,
        w_ln_z,
        b_ln_z,
        num_heads=num_heads,
        multiplicity=multiplicity,
        eps=eps,
        inf=inf,
        return_z_proj=return_z_proj,
        is_cached_z_proj=is_cached_z_proj,
    )

    attn = torch.einsum("bhid,bhjd->bhij", q, k)
    if attn_scale is None:
        attn = attn / (D_Q**0.5)
    else:
        attn = attn * attn_scale

    attn = attn + bias
    attn = attn.softmax(dim=-1)
    out = torch.einsum("bhij,bhjd->bihd", attn, v).reshape(B, -1, H * D_Q)

    g = torch.nn.functional.linear(s, w_proj_g, bias=b_proj_g)
    g = torch.sigmoid(g)
    o = torch.nn.functional.linear(g * out, w_proj_o, bias=b_proj_o)
    o = o.to(z_dtype)
    z_proj = z_proj.to(z_dtype) if z_proj is not None else None
    return o, z_proj


def _attention_pair_bias_mask(
    z: torch.Tensor,
    w_proj_z: Optional[torch.Tensor],
    b_proj_z: Optional[torch.Tensor],
    w_ln: Optional[torch.Tensor],
    b_ln: Optional[torch.Tensor],
    mask: torch.Tensor,
    num_heads: int,
    multiplicity: int,
    eps: float,
    inf: float,
    grad_enabled: bool,
    return_z_proj: bool,
    is_cached_z_proj: bool,
):
    nvtx_range_push("_attention_pair_bias_mask")
    z = z.contiguous()
    if mask is not None:
        mask = mask.contiguous()
    if w_proj_z is not None:
        w_proj_z = w_proj_z.contiguous()
    if b_proj_z is not None:
        b_proj_z = b_proj_z.contiguous()
    if w_ln is not None:
        w_ln = w_ln.contiguous()
    if b_ln is not None:
        b_ln = b_ln.contiguous()
    has_bias = b_proj_z is not None
    elementwise_affine = w_ln is not None or b_ln is not None

    if is_cached_z_proj:
        assert z.shape[1] == num_heads
        B, _, U, V = z.shape
        DIM_Z = None
    else:
        B, U, V, DIM_Z = z.shape

    if multiplicity > 1 and B * multiplicity == mask.shape[0]:
        mask_with_multiplicity = True
    else:
        mask_with_multiplicity = False

    z_norm, mean, rstd = None, None, None

    out_mask = torch.empty(
        (B * multiplicity, num_heads, U, V), dtype=z.dtype, device=z.device
    )

    if return_z_proj and not is_cached_z_proj:
        z_proj = torch.empty(
            (B, num_heads, U, V),
            dtype=z.dtype,
            device=z.device,
        )
    elif return_z_proj:
        z_proj = z.clone().contiguous()
    else:
        z_proj = None

    if is_cached_z_proj:
        # TODO better perf-tuning
        TILE_V = 128
        NUM_HEADS_PER_BLK = 4
        num_warps = 8
        num_stages = 2

        grid = (
            triton.cdiv(V, TILE_V),
            U,
            triton.cdiv(num_heads, NUM_HEADS_PER_BLK) * B,
        )

        NEEDS_INT64 = (
            DIM_Z is not None
            and (B * U * V * DIM_Z >= 2**31 - 1)
            or (B * multiplicity * num_heads * U * V >= 2**31 - 1)
        )

        pair_bias_mask_forward_kernel[grid](
            z,
            mask,
            U,
            V,
            multiplicity,
            out_mask,
            TILE_V=TILE_V,
            NUM_HEADS=num_heads,
            NUM_HEADS_PER_BLK=NUM_HEADS_PER_BLK,
            INF=inf,
            MASK_WITH_MULTIPLICITY=mask_with_multiplicity,
            num_warps=num_warps,
            num_stages=num_stages,
        )

    else:
        if DIM_Z in (16, 32, 64, 128):
            # TODO better perf-tuning
            TILE_V = 64
            NUM_HEADS_PER_BLK = 16
            HEAD_BLKS = triton.cdiv(num_heads, NUM_HEADS_PER_BLK)
            TILE_K = 32 if DIM_Z > 16 else 16
            num_warps = 4
            num_stages = 3

            grid = (triton.cdiv(V, TILE_V), U, HEAD_BLKS * B)

            if grad_enabled:
                z_norm = torch.empty((B, U, V, DIM_Z), dtype=z.dtype, device=z.device)
                mean = torch.empty((B, U, V), dtype=torch.float32, device=z.device)
                rstd = torch.empty((B, U, V), dtype=torch.float32, device=z.device)

            NEEDS_INT64 = (B * U * V * DIM_Z >= 2**31 - 1) or (
                B * multiplicity * num_heads * U * V >= 2**31 - 1
            )

            pair_bias_norm_linear_mask_forward_kernel[grid](
                z,
                mask,
                w_proj_z,
                b_proj_z,
                w_ln,
                b_ln,
                U,
                V,
                multiplicity,
                out_mask,
                z_norm,
                z_proj,
                mean,
                rstd,
                TILE_V=TILE_V,
                TILE_K=TILE_K,
                NUM_HEADS=num_heads,
                NUM_HEADS_PER_BLK=NUM_HEADS_PER_BLK,
                DIM_Z=DIM_Z,
                INF=inf,
                EPS=eps,
                ELEMENTWISE_AFFINE=elementwise_affine,
                IS_TRAINING=grad_enabled,
                HAS_BIAS=has_bias,
                MASK_WITH_MULTIPLICITY=mask_with_multiplicity,
                CACHE_Z_PROJ=return_z_proj,
                NEEDS_INT64=NEEDS_INT64,
                num_warps=num_warps,
                num_stages=num_stages,
            )

        else:
            z_norm, mean, rstd = torch.ops.cuequivariance.layer_norm_transpose(
                z.view(B, -1, DIM_Z),
                w_ln,
                b_ln,
                eps=eps,
                layout=Layout.BND_BND,
                elementwise_affine=elementwise_affine,
            )

            z_norm = z_norm.view(B, U, V, DIM_Z).contiguous()
            mean = mean.contiguous()
            rstd = rstd.contiguous()

            # TODO better perf-tuning
            TILE_V = 64
            NUM_HEADS_PER_BLK = 16
            HEAD_BLKS = triton.cdiv(num_heads, NUM_HEADS_PER_BLK)
            TILE_K = 16 if DIM_Z <= 16 else (32 if DIM_Z % 32 == 0 else 16)
            num_warps = 4
            num_stages = 3

            grid = (triton.cdiv(V, TILE_V), U, HEAD_BLKS * B)
            assert DIM_Z % TILE_K == 0, (
                f"DIM_Z {DIM_Z} must be divisible by TILE_K {TILE_K}"
            )
            NEEDS_INT64 = (B * U * V * DIM_Z >= 2**31 - 1) or (
                B * multiplicity * num_heads * U * V >= 2**31 - 1
            )
            pair_bias_linear_mask_forward_kernel[grid](
                z_norm,
                mask,
                w_proj_z,
                b_proj_z,
                U,
                V,
                multiplicity,
                out_mask,
                z_proj,
                TILE_V=TILE_V,
                TILE_K=TILE_K,
                NUM_HEADS=num_heads,
                NUM_HEADS_PER_BLK=NUM_HEADS_PER_BLK,
                DIM_Z=DIM_Z,
                INF=inf,
                NEEDS_INT64=NEEDS_INT64,
                HAS_BIAS=has_bias,
                MASK_WITH_MULTIPLICITY=mask_with_multiplicity,
                CACHE_Z_PROJ=return_z_proj,
                num_warps=num_warps,
                num_stages=num_stages,
            )

            if not grad_enabled:
                z_norm, mean, rstd = None, None, None

    nvtx_range_pop()
    return out_mask, z_proj, z_norm, mean, rstd


@torch.library.custom_op(
    "cuequivariance::attention_pair_bias_mask",
    mutates_args=(),
    device_types="cuda",
)
def _(
    z: torch.Tensor,
    w_proj_z: torch.Tensor,
    b_proj_z: Optional[torch.Tensor],
    w_ln: Optional[torch.Tensor],
    b_ln: Optional[torch.Tensor],
    mask: torch.Tensor,
    num_heads: int,
    multiplicity: int,
    eps: float,
    inf: float,
    grad_enabled: bool,
    return_z_proj: bool,
    is_cached_z_proj: bool,
    valid_optional_inputs: list[bool],
) -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor, torch.Tensor, torch.Tensor]:
    return _attention_pair_bias_mask(
        z,
        w_proj_z,
        b_proj_z if valid_optional_inputs[0] else None,
        w_ln if valid_optional_inputs[1] else None,
        b_ln if valid_optional_inputs[2] else None,
        mask if valid_optional_inputs[3] else None,
        num_heads,
        multiplicity,
        eps,
        inf,
        grad_enabled,
        return_z_proj,
        is_cached_z_proj,
    )


@torch.library.register_fake(
    "cuequivariance::attention_pair_bias_mask",
)
def _attention_pair_bias_mask_fake(
    z: torch.Tensor,
    w_proj_z: torch.Tensor,
    b_proj_z: Optional[torch.Tensor],
    w_ln: Optional[torch.Tensor],
    b_ln: Optional[torch.Tensor],
    mask: torch.Tensor,
    num_heads: int,
    multiplicity: int,
    eps: float,
    inf: float,
    grad_enabled: bool,
    return_z_proj: bool,
    is_cached_z_proj: bool,
    valid_optional_inputs: list[bool],
) -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor, torch.Tensor, torch.Tensor]:
    """
    Fake Torch operation for forward pass of attention_pair_bias
    """
    if is_cached_z_proj:
        assert z.shape[1] == num_heads
        B, _, U, V = z.shape
        DIM_Z = None
    else:
        B, U, V, DIM_Z = z.shape

    out_mask = z.new_empty((B * multiplicity, num_heads, U, V)).contiguous()
    if return_z_proj:
        if is_cached_z_proj:
            z_proj = torch.empty_like(z).contiguous()
        else:
            z_proj = z.new_empty((B, num_heads, U, V)).contiguous()
    else:
        z_proj = None

    if grad_enabled and not is_cached_z_proj:
        z_norm = z.new_empty((B, U, V, DIM_Z)).contiguous()
        mean = z.new_empty((B, U, V), dtype=torch.float32).contiguous()
        rstd = torch.empty((B, U, V), dtype=torch.float32).contiguous()
    else:
        z_norm, mean, rstd = None, None, None
    return (out_mask, z_proj, z_norm, mean, rstd)


def _setup_context(ctx, inputs, output):
    (
        z,
        w_proj_z,
        b_proj_z,
        w_ln,
        b_ln,
        mask,
        num_heads,
        multiplicity,
        eps,
        inf,
        grad_enabled,
        return_z_proj,
        is_cached_z_proj,
        _,
    ) = inputs
    out_mask, z_proj, z_norm, mean, rstd = output
    ctx.save_for_backward(z, w_proj_z, b_proj_z, w_ln, b_ln, z_norm, mean, rstd)

    ctx.multiplicity = multiplicity
    ctx.return_z_proj = return_z_proj
    ctx.is_cached_z_proj = is_cached_z_proj
    ctx.num_heads = num_heads


def _backward(ctx, grad_out_mask, grad_out_z_proj, *args):
    """
    Autograd fixture for backward pass of attention_pair_bias
    """
    z, w_proj_z, b_proj_z, w_ln, b_ln, z_norm, mean, rstd = ctx.saved_tensors

    grad_z, grad_w_proj_z, grad_b_proj_z, grad_w_ln, grad_b_ln = (
        torch.ops.cuequivariance.attention_pair_bias_mask_bwd(
            grad_out_mask,
            grad_out_z_proj,
            z_norm,
            mean,
            rstd,
            z,
            w_proj_z,
            b_proj_z,
            w_ln,
            b_ln,
            ctx.num_heads,
            ctx.multiplicity,
            ctx.return_z_proj,
            ctx.is_cached_z_proj,
        )
    )
    return (
        grad_z,
        grad_w_proj_z,
        grad_b_proj_z,
        grad_w_ln,
        grad_b_ln,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
    )


torch.library.register_autograd(
    "cuequivariance::attention_pair_bias_mask",
    _backward,
    setup_context=_setup_context,
)


@torch.library.custom_op(
    "cuequivariance::attention_pair_bias_mask_bwd",
    mutates_args=(),
    device_types="cuda",
)
def _(
    grad_out_mask: torch.Tensor,
    grad_out_z_proj: Optional[torch.Tensor],
    z_norm: torch.Tensor,
    mean: torch.Tensor,
    rstd: torch.Tensor,
    z: torch.Tensor,
    w_proj_z: torch.Tensor,
    b_proj_z: Optional[torch.Tensor],
    w_ln: Optional[torch.Tensor],
    b_ln: Optional[torch.Tensor],
    num_heads: int,
    multiplicity: int,
    return_z_proj: bool,
    is_cached_z_proj: bool,
) -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor, torch.Tensor, torch.Tensor]:
    nvtx_range_push("attention_pair_bias_mask_bwd")

    # Make only tensors computed during backpropagation contiguous
    if grad_out_mask is not None:
        grad_out_mask = grad_out_mask.contiguous()

    if is_cached_z_proj:
        assert z.shape[1] == num_heads
        B, _, U, V = z.shape
        DIM_Z = None
    else:
        B, U, V, DIM_Z = z.shape

    if multiplicity > 1:
        # if multiplicity > 1, we need to sum over the multiplicity dimension
        grad_out_mask = grad_out_mask.view(-1, multiplicity, *grad_out_mask.shape[1:])
        grad_out_mask = grad_out_mask.sum(dim=1)

    grad_out_mask = grad_out_mask.view(B, num_heads, -1)

    if is_cached_z_proj:
        grad_z = grad_out_mask.clone().view(B, num_heads, U, V).contiguous()
        grad_w_proj_z = None
        grad_b_proj_z = None
        grad_w_ln = None
        grad_b_ln = None

    else:
        B, U, V, DIM_Z = z.shape
        grad_w_proj_z = grad_out_mask @ z_norm.view(B, -1, DIM_Z)
        grad_w_proj_z = grad_w_proj_z.sum(dim=0).contiguous()
        if b_proj_z is not None:
            grad_b_proj_z = grad_out_mask.sum(dim=-1).sum(dim=0).contiguous()
        else:
            grad_b_proj_z = None

        # gradient through layernorm in unfused fashion
        grad_z_norm = grad_out_mask.transpose(1, 2) @ w_proj_z
        elementwise_affine = w_ln is not None or b_ln is not None

        mean = mean.view(B, -1)
        rstd = rstd.view(B, -1)

        grad_z, grad_w_ln, grad_b_ln = _layer_norm_transpose_bwd(
            grad_z_norm,
            z.view(B, -1, DIM_Z),
            w_ln,
            mean,
            rstd,
            elementwise_affine,
            Layout.BND_BND,
        )
        grad_z = grad_z.view(z.shape).contiguous()  # B, U, V, DIM_Z)

        if grad_w_ln is not None:
            grad_w_ln = (
                grad_w_ln.view(-1, grad_w_ln.shape[-1])
                .sum(dim=0)
                .to(w_ln.dtype)
                .contiguous()
            )
        if grad_b_ln is not None:
            grad_b_ln = (
                grad_b_ln.view(-1, grad_b_ln.shape[-1])
                .sum(dim=0)
                .to(b_ln.dtype)
                .contiguous()
            )

    nvtx_range_pop()

    return (
        grad_z,
        grad_w_proj_z,
        grad_b_proj_z,
        grad_w_ln,
        grad_b_ln,
    )


@torch.library.register_fake(
    "cuequivariance::attention_pair_bias_mask_bwd",
)
def _(
    grad_out_mask: torch.Tensor,
    grad_out_z_proj: Optional[torch.Tensor],
    z_norm: torch.Tensor,
    mean: torch.Tensor,
    rstd: torch.Tensor,
    z: torch.Tensor,
    w_proj_z: torch.Tensor,
    b_proj_z: Optional[torch.Tensor],
    w_ln: Optional[torch.Tensor],
    b_ln: Optional[torch.Tensor],
    num_heads: int,
    multiplicity: int,
    return_z_proj: bool,
    is_cached_z_proj: bool,
) -> Tuple[
    torch.Tensor,
    torch.Tensor,
    Optional[torch.Tensor],
    Optional[torch.Tensor],
    Optional[torch.Tensor],
]:
    nvtx_range_push("attention_pair_bias_mask_bwd")

    grad_z = torch.empty_like(z)
    if is_cached_z_proj:
        grad_w_proj_z = None
        grad_b_proj_z = None
        grad_w_ln = None
        grad_b_ln = None

    else:
        grad_w_proj_z = torch.empty_like(w_proj_z)
        grad_b_proj_z = torch.empty_like(b_proj_z) if b_proj_z is not None else None
        grad_w_ln = torch.empty_like(w_ln) if w_ln is not None else None
        grad_b_ln = torch.empty_like(b_ln) if b_ln is not None else None

    return (
        grad_z,
        grad_w_proj_z,
        grad_b_proj_z,
        grad_w_ln,
        grad_b_ln,
    )


def attention_pair_bias_mask(
    z: torch.Tensor,
    mask: torch.Tensor,
    w_proj_z: torch.Tensor,
    b_proj_z: Optional[torch.Tensor],
    w_ln: Optional[torch.Tensor],
    b_ln: Optional[torch.Tensor],
    num_heads: int,
    multiplicity: int,
    eps: float = 1e-5,
    inf: float = 1e6,
    return_z_proj: bool = False,
    is_cached_z_proj: bool = False,
):
    # Use original PyTorch implementation for short sequences in eager mode only
    if not torch._jit_internal.is_scripting() and not torch.compiler.is_compiling():
        seq_seq_len = z.shape[-2] * z.shape[-3]
        if seq_seq_len <= CUEQ_ATTENTION_PAIR_BIAS_FALLBACK_THRESHOLD**2:
            out, z_proj = _attention_pair_bias_mask_torch(
                z,
                mask,
                w_proj_z,
                b_proj_z,
                w_ln,
                b_ln,
                num_heads,
                multiplicity,
                eps,
                inf,
                return_z_proj,
                is_cached_z_proj,
            )
            if torch.is_autocast_enabled():
                autocast_dtype = torch.get_autocast_dtype("cuda")
                out = maybe_to(out, autocast_dtype)
                z_proj = maybe_to(z_proj, autocast_dtype)
            return out, z_proj

    if torch.is_autocast_enabled():
        autocast_dtype = torch.get_autocast_dtype("cuda")
        z = maybe_to(z, autocast_dtype)
        mask = maybe_to(mask, autocast_dtype)
        w_proj_z = maybe_to(w_proj_z, autocast_dtype)
        b_proj_z = maybe_to(b_proj_z, autocast_dtype)
        w_ln = maybe_to(w_ln, autocast_dtype)
        b_ln = maybe_to(b_ln, autocast_dtype)

    valid_optional_inputs = [True, True, True, True]
    if is_in_export_mode():
        dummy = z.new_empty((1, 1))
        if b_proj_z is None:
            b_proj_z = dummy
            valid_optional_inputs[0] = False
        if w_ln is None:
            w_ln = dummy
            valid_optional_inputs[1] = False
        if b_ln is None:
            b_ln = dummy
            valid_optional_inputs[2] = False
        if mask is None:
            mask = dummy
            valid_optional_inputs[3] = False

    out_mask, z_proj, _, _, _ = torch.ops.cuequivariance.attention_pair_bias_mask(
        z,
        w_proj_z,
        b_proj_z,
        w_ln,
        b_ln,
        mask,
        num_heads,
        multiplicity,
        eps,
        inf,
        torch.is_grad_enabled(),
        return_z_proj,
        is_cached_z_proj,
        valid_optional_inputs,
    )
    return out_mask, z_proj


def attention_pair_bias(
    s: torch.Tensor,
    q: torch.Tensor,
    k: torch.Tensor,
    v: torch.Tensor,
    z: torch.Tensor,
    mask: torch.Tensor,
    num_heads: int,
    w_proj_z: Optional[torch.Tensor],
    w_proj_g: torch.Tensor,
    w_proj_o: torch.Tensor,
    w_ln_z: Optional[torch.Tensor] = None,
    b_ln_z: Optional[torch.Tensor] = None,
    b_proj_z: Optional[torch.Tensor] = None,
    b_proj_g: Optional[torch.Tensor] = None,
    b_proj_o: Optional[torch.Tensor] = None,
    inf: float = 1e6,
    eps: float = 1e-5,
    attn_scale: Optional[float] = None,
    return_z_proj: bool = True,
    is_cached_z_proj: bool = False,
):
    # q: query sequence (B x M) x H x U x DH
    # k/v: key/value sequence (B x M) x H x V x DH
    # z: pairwise tensor B x U x V x DIM_Z
    # mask: B x V or (B x M) x V

    BM, H, S, DH = q.shape
    B = z.shape[0]
    assert BM % B == 0
    multiplicity = BM // B

    # Use original PyTorch implementation for short sequences in eager mode only
    if not (
        torch._jit_internal.is_scripting()
        or torch.compiler.is_compiling()
        or torch.onnx.is_in_onnx_export()
        or is_fx_tracing()
    ):
        seq_seq_len = z.shape[-2] * z.shape[-3]
        if (
            seq_seq_len <= CUEQ_ATTENTION_PAIR_BIAS_FALLBACK_THRESHOLD**2
            or DH % 32 != 0
        ):
            out, z_proj = _attention_pair_bias_torch(
                s,
                q,
                k,
                v,
                z,
                mask,
                num_heads,
                w_proj_z,
                w_proj_g,
                w_proj_o,
                w_ln_z,
                b_ln_z,
                b_proj_z,
                b_proj_g,
                b_proj_o,
                inf=inf,
                eps=eps,
                attn_scale=attn_scale,
                return_z_proj=return_z_proj,
                is_cached_z_proj=is_cached_z_proj,
                multiplicity=multiplicity,
            )
            if torch.is_autocast_enabled():
                autocast_dtype = torch.get_autocast_dtype("cuda")
                out = maybe_to(out, autocast_dtype)
                z_proj = maybe_to(z_proj, autocast_dtype)
            return out, z_proj

    bias, z_proj = attention_pair_bias_mask(
        z,
        mask,
        w_proj_z,
        b_proj_z,
        w_ln_z,
        b_ln_z,
        num_heads=H,
        multiplicity=multiplicity,
        eps=eps,
        inf=inf,
        return_z_proj=return_z_proj,
        is_cached_z_proj=is_cached_z_proj,
    )
    if not torch.compiler.is_compiling():
        with torch.nn.attention.sdpa_kernel(
            backends=[
                torch.nn.attention.SDPBackend.CUDNN_ATTENTION,
                torch.nn.attention.SDPBackend.FLASH_ATTENTION,
                torch.nn.attention.SDPBackend.EFFICIENT_ATTENTION,
            ],
            set_priority=True,
        ):
            o = torch.nn.functional.scaled_dot_product_attention(
                q,
                k,
                v,
                attn_mask=bias,
                is_causal=False,
                scale=attn_scale,
            )

    else:
        with torch.nn.attention.sdpa_kernel(
            backends=[
                torch.nn.attention.SDPBackend.CUDNN_ATTENTION,
                torch.nn.attention.SDPBackend.FLASH_ATTENTION,
                torch.nn.attention.SDPBackend.EFFICIENT_ATTENTION,
            ],
        ):
            o = torch.nn.functional.scaled_dot_product_attention(
                q,
                k,
                v,
                attn_mask=bias,
                is_causal=False,
                scale=attn_scale,
            )

    # TODO more efficient transpose
    o = torch.einsum("bhid->bihd", o).contiguous().view(B * multiplicity, -1, H * DH)

    g = torch.nn.functional.linear(s, w_proj_g, bias=b_proj_g)
    g = torch.sigmoid(g)
    o = torch.nn.functional.linear(g * o, w_proj_o, bias=b_proj_o)

    return o, z_proj
