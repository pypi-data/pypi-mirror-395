# SPDX-FileCopyrightText: Copyright (c) 2024 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: LicenseRef-NvidiaProprietary
#
# NVIDIA CORPORATION, its affiliates and licensors retain all intellectual
# property and proprietary rights in and to this material, related
# documentation and any modifications thereto. Any use, reproduction,
# disclosure or distribution of this material and related documentation
# without an express license agreement from NVIDIA CORPORATION or
# its affiliates is strictly prohibited.


from typing import Tuple

import torch
import triton

from cuequivariance_ops.triton import (
    Layout,
    layer_norm_transpose_backward_kernel,
    layer_norm_transpose_backward_single_pass_kernel,
    layer_norm_transpose_forward_kernel,
    layer_norm_transpose_forward_single_pass_kernel,
)


def _kernel_heuristic(B, N, D, dtype):
    # TODO: verify heuristic and better tuning

    # small powers of 2 can be worked on in a single pass
    # here: TILE_SIZE == D, bound by max. size
    # and ideally using at least TILE_N_MIN = 32
    USE_SINGLE_PASS_KERNEL = D in (32, 64, 128)

    if USE_SINGLE_PASS_KERNEL:
        TILE_D = D

    else:
        # if single pass is not possible, we iterate over D in chunks of TILE_D
        if D <= 64:
            TILE_D = 64
        elif D <= 128:
            TILE_D = 128
        else:
            TILE_D = 256

    # choose TILE_N such that transposed can be worked on well in a single warp
    # --> 32 * 2 for FP16/BF16, 32 for FP32
    if dtype == torch.float32:
        TILE_N_MIN = 32
    else:
        TILE_N_MIN = 64
    # given TILE_D, we operate on at most TILE_N_MAX = 8192 // TILE_D
    TILE_N_MAX = 16384 // TILE_D

    assert TILE_N_MAX >= TILE_N_MIN, (
        f"TILE_N_MAX {TILE_N_MAX} < TILE_N_MIN {TILE_N_MIN} for TILE_D {TILE_D}"
    )

    # if MAX and MIN are the same, we use that as tile size
    if TILE_N_MAX == TILE_N_MIN:
        TILE_N = TILE_N_MIN

    # else: ensure at least 148 * 4 thread blocks
    # TODO maybe configure waves depending on hardware
    # TODO check if 148 * 4 blocks is reasonable assumption
    else:
        TILE_N = TILE_N_MIN
        PREV_TILE_N = TILE_N
        MIN_BLOCKS = 148 * 4
        while (TILE_N <= TILE_N_MAX) and (B * triton.cdiv(N, TILE_N) > MIN_BLOCKS):
            PREV_TILE_N = TILE_N
            TILE_N *= 2
        TILE_N = PREV_TILE_N

    SIZE_PER_BLOCK = TILE_N * TILE_D
    num_warps = 4
    if SIZE_PER_BLOCK >= 32768:
        num_warps = 32
    elif SIZE_PER_BLOCK >= 8192:
        num_warps = 16
    elif SIZE_PER_BLOCK >= 2048:
        num_warps = 8

    return USE_SINGLE_PASS_KERNEL, TILE_N, TILE_D, num_warps


def _allocate_outputs_bwd(x, layout):
    if layout == Layout.BND_BND:
        B, N, D = x.shape
    elif layout == Layout.BDN_BND:
        B, D, N = x.shape
    elif layout == Layout.BND_BDN:
        B, N, D = x.shape
    elif layout == Layout.DBN_BND:
        D, B, N = x.shape
    elif layout == Layout.BND_DBN:
        B, N, D = x.shape
    else:
        raise ValueError
    TILE_D = 64
    TILE_N = 64 if x.dtype != torch.float32 else 32
    num_tiles = triton.cdiv(N, TILE_N)
    grad_w = torch.empty((B, num_tiles, D), dtype=torch.float32, device=x.device)
    grad_b = torch.empty((B, num_tiles, D), dtype=torch.float32, device=x.device)
    grad_x = torch.empty_like(x)
    return grad_x, grad_w, grad_b, B, N, D, TILE_D, TILE_N, num_tiles


def _allocate_outputs(x, layout):
    if layout == Layout.BND_BND:
        B, N, D = x.shape
        out = torch.empty(B, N, D, dtype=x.dtype, device=x.device)
    elif layout == Layout.BDN_BND:
        B, D, N = x.shape
        out = torch.empty(B, N, D, dtype=x.dtype, device=x.device)
    elif layout == Layout.BND_BDN:
        B, N, D = x.shape
        out = torch.empty(B, D, N, dtype=x.dtype, device=x.device)
    elif layout == Layout.DBN_BND:
        D, B, N = x.shape
        out = torch.empty(B, N, D, dtype=x.dtype, device=x.device)
    elif layout == Layout.BND_DBN:
        B, N, D = x.shape
        out = torch.empty(D, B, N, dtype=x.dtype, device=x.device)
    else:
        raise ValueError

    mean = torch.empty(B, N, dtype=torch.float32, device=x.device)
    rstd = torch.empty(B, N, dtype=torch.float32, device=x.device)
    return out, mean, rstd, B, N, D


def _layer_norm_transpose(
    x, w, b, eps, elementwise_affine, layout, out, mean, rstd, B, N, D
):
    # TODO use heuristic another day
    # use_single_pass_kernel, TILE_N, TILE_D, num_warps = _kernel_heuristic(
    #
    #     B, N, D, x.dtype
    # )
    use_single_pass_kernel = False
    TILE_D = 64
    TILE_N = 64
    num_warps = 8
    num_stages = 2

    x = x.contiguous()
    w = w.contiguous()
    b = b.contiguous()

    if use_single_pass_kernel:
        kernel = layer_norm_transpose_forward_single_pass_kernel
    else:
        kernel = layer_norm_transpose_forward_kernel

    grid = (triton.cdiv(N, TILE_N), B, 1)

    NEEDS_INT64 = B * N * D >= 2**31 - 1

    kernel[grid](
        x,
        w,
        b,
        out,
        mean,
        rstd,
        B,
        N,
        D=D,
        EPS=eps,
        TILE_N=TILE_N,
        TILE_D=TILE_D,
        ELEMENTWISE_AFFINE=elementwise_affine,
        LAYOUT=layout,
        NEEDS_INT64=NEEDS_INT64,
        num_warps=num_warps,
        num_stages=num_stages,
    )


@torch.library.custom_op("cuequivariance::layer_norm_transpose", mutates_args=())
def _(
    x: torch.Tensor,
    w: torch.Tensor,
    b: torch.Tensor,
    eps: float,
    elementwise_affine: bool,
    layout: int,
) -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
    out, mean, rstd, B, N, D = _allocate_outputs(x, layout)
    _layer_norm_transpose(
        x, w, b, eps, elementwise_affine, layout, out, mean, rstd, B, N, D
    )
    return out, mean, rstd


def _layer_norm_transpose_bwd(
    grad_out: torch.Tensor,
    x: torch.Tensor,
    w: torch.Tensor,
    mean: torch.Tensor,
    rstd: torch.Tensor,
    elementwise_affine: bool,
    layout: int,
) -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
    grad_out = grad_out.contiguous()
    x = x.contiguous()
    w = w.contiguous()
    mean = mean.contiguous()
    rstd = rstd.contiguous()

    # TODO use heuristic another day
    # TODO check if backward needs different heuristic
    # use_single_pass_kernel, TILE_N, TILE_D, num_warps = _kernel_heuristic(
    #     B, N, D, x.dtype
    # )
    use_single_pass_kernel = False

    grad_x, grad_w, grad_b, B, N, D, TILE_D, TILE_N, num_tiles = _allocate_outputs_bwd(
        x, layout
    )

    num_warps = 8
    num_stages = 2

    if use_single_pass_kernel:
        kernel = layer_norm_transpose_backward_single_pass_kernel
    else:
        kernel = layer_norm_transpose_backward_kernel

    NEEDS_INT64 = B * N * D >= 2**31 - 1

    grid = (num_tiles, B, 1)
    kernel[grid](
        grad_out,
        x,
        w,
        mean,
        rstd,
        grad_x,
        grad_w,
        grad_b,
        B,
        N,
        D=D,
        TILE_N=TILE_N,
        TILE_D=TILE_D,
        ELEMENTWISE_AFFINE=elementwise_affine,
        LAYOUT=layout,
        NEEDS_INT64=NEEDS_INT64,
        num_warps=num_warps,
        num_stages=num_stages,
    )

    if not elementwise_affine:
        grad_w, grad_b = None, None

    return grad_x, grad_w, grad_b


@torch.library.custom_op("cuequivariance::layer_norm_transpose_bwd", mutates_args=())
def _(
    grad_out: torch.Tensor,
    x: torch.Tensor,
    w: torch.Tensor,
    mean: torch.Tensor,
    rstd: torch.Tensor,
    elementwise_affine: bool,
    layout: int,
) -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
    grad_x, grad_w, grad_b = _layer_norm_transpose_bwd(
        grad_out,
        x,
        w,
        mean,
        rstd,
        elementwise_affine,
        layout,
    )
    return grad_x, grad_w, grad_b


@torch.library.register_fake("cuequivariance::layer_norm_transpose_bwd")
def _(
    grad_out,
    x,
    w,
    mean,
    rstd,
    elementwise_affine,
    layout,
) -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
    grad_x, grad_w, grad_b, B, N, D, TILE_D, TILE_N, num = _allocate_outputs_bwd(
        x, layout
    )
    if not elementwise_affine:
        grad_w, grad_b = None, None

    return grad_x, grad_w, grad_b


@torch.library.register_fake("cuequivariance::layer_norm_transpose")
def _layer_norm_transpose_fake(
    x: torch.Tensor,
    w: torch.Tensor,
    b: torch.Tensor,
    eps: float,
    elementwise_affine: bool,
    layout: int,
) -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
    out, mean, rstd, B, N, D = _allocate_outputs(x, layout)
    return out.contiguous(), mean.contiguous(), rstd.contiguous()


def _setup_context(ctx, inputs, output):
    ctx.inputs = inputs[4:]
    # ctx.save_for_backward(x, w, mean, rstd)
    ctx.save_for_backward(*inputs[:2], *output[1:])


def _layer_norm_transpose_backward(ctx, grad_out, mean, rstd):
    grad_out = grad_out.contiguous()
    elementwise_affine, layout = ctx.inputs
    x, w, mean, rstd = ctx.saved_tensors

    grad_x, grad_w, grad_b = torch.ops.cuequivariance.layer_norm_transpose_bwd(
        grad_out,
        x,
        w,
        mean,
        rstd,
        elementwise_affine,
        layout,
    )

    # this should have been inside backward op above - but for some reason, torch.compile wants it here
    if elementwise_affine:
        if grad_w is not None:
            grad_w = grad_w.view(-1, grad_w.shape[-1]).sum(dim=0).to(w.dtype)
        if grad_b is not None:
            grad_b = grad_b.view(-1, grad_b.shape[-1]).sum(dim=0).to(w.dtype)

    return grad_x, grad_w, grad_b, None, None, None


torch.library.register_autograd(
    "cuequivariance::layer_norm_transpose",
    _layer_norm_transpose_backward,
    setup_context=_setup_context,
)


def layer_norm_transpose(
    x, w, b, eps=1e-5, elementwise_affine=True, layout: str = "nd->nd"
):
    """Apply fused layer normalization with support for various input layouts.

    This function performs layer normalization on the input tensor with optional
    elementwise affine transformation. It supports various input layouts and can
    transform between different tensor shapes.

    The normalization process consists of two steps:
    1. Normalize the input by subtracting mean and dividing by standard deviation
    2. Apply an affine transformation: output = weight * normalized_input + bias

    Args:
        x (torch.Tensor): Input tensor. Shape depends on the layout.
        w (torch.Tensor): Weight tensor for scaling the normalized values. Shape should be (D,).
            These weights allow the network to learn the optimal scale for each feature.
            Only used if elementwise_affine=True.
        b (torch.Tensor): Bias tensor for shifting the normalized values. Shape should be (D,).
            These biases allow the network to learn the optimal offset for each feature.
            Only used if elementwise_affine=True.
        eps (float, optional): Small constant for numerical stability. Defaults to 1e-5.
        elementwise_affine (bool, optional): Whether to apply elementwise affine transformation.
            If False, weight and bias are not used (equivalent to weight=1, bias=0).
            Defaults to True.
        layout (str, optional): Input/output layout specification. Defaults to "nd->nd".
            Supported layouts:
            - "nd->nd": (N, D) -> (N, D)
            - "nd->dn": (N, D) -> (D, N)
            - "bnd->bnd": (B, N, D) -> (B, N, D)
            - "bdn->bnd": (B, D, N) -> (B, N, D)
            - "bnd->bdn": (B, N, D) -> (B, D, N)
            - "dbn->bnd": (D, B, N) -> (B, N, D)
            - "bnd->dbn": (B, N, D) -> (D, B, N)
            - "bijd->bijd": (B, I, J, D) -> (B, I, J, D)
            - "bijd->bdij": (B, I, J, D) -> (B, D, I, J)
            - "bdij->bijd": (B, D, I, J) -> (B, I, J, D)
            - "dbij->bijd": (D, B, I, J) -> (B, I, J, D)
            - "bijd->dbij": (B, I, J, D) -> (D, B, I, J)

    Returns:
        torch.Tensor: Normalized tensor with shape determined by the output layout.

    Raises:
        ValueError: If the specified layout is not supported.

    Example:
        >>> x = torch.randn(1, 128, 128, device="cuda", dtype=torch.float, requires_grad=True)
        >>> w = torch.randn(128, device="cuda", dtype=torch.float, requires_grad=True)
        >>> b = torch.randn(128, device="cuda", dtype=torch.float, requires_grad=True)
        >>> out = layer_norm_transpose(x, w, b, layout="bnd->bnd")
    """
    supported_layouts = (
        "nd->nd",
        "nd->dn",
        "dn->nd",
        "bnd->bnd",
        "bnd->bdn",
        "bdn->bnd",
        "dbn->bnd",
        "bnd->dbn",
        "bijd->bijd",
        "bijd->bdij",
        "bdij->bijd",
        "dbij->bijd",
        "bijd->dbij",
    )

    if layout == "nd->nd":
        N, D = x.shape
        B = 1
        x = x.view(1, N, D)
        out_shape = (N, D)
        layout = Layout.BND_BND

    elif layout == "nd->dn":
        N, D = x.shape
        B = 1
        x = x.view(1, N, D)
        out_shape = (D, N)
        layout = Layout.BND_BDN

    elif layout == "dn->nd":
        D, N = x.shape
        B = 1
        x = x.view(1, D, N)
        out_shape = (N, D)
        layout = Layout.BDN_BND

    elif layout == "bnd->bnd":
        B, N, D = x.shape
        out_shape = (B, N, D)
        layout = Layout.BND_BND

    elif layout == "bdn->bnd":
        B, D, N = x.shape
        out_shape = (B, N, D)
        layout = Layout.BDN_BND

    elif layout == "bnd->bdn":
        B, N, D = x.shape
        out_shape = (B, D, N)
        layout = Layout.BND_BDN

    elif layout == "dbn->bnd":
        D, B, N = x.shape
        out_shape = (B, N, D)
        layout = Layout.DBN_BND

    elif layout == "bnd->dbn":
        B, N, D = x.shape
        out_shape = (D, B, N)
        layout = Layout.BND_DBN

    elif layout == "bijd->bijd":
        B, II, J, D = x.shape
        out_shape = (B, II, J, D)
        x = x.view(B, II * J, D)
        layout = Layout.BND_BND

    elif layout == "bijd->bdij":
        B, II, J, D = x.shape
        out_shape = (B, D, II, J)
        x = x.view(B, II * J, D)
        layout = Layout.BND_BDN

    elif layout == "bdij->bijd":
        B, D, II, J = x.shape
        out_shape = (B, II, J, D)
        x = x.view(B, D, II * J)
        layout = Layout.BDN_BND

    elif layout == "dbij->bijd":
        D, B, II, J = x.shape
        out_shape = (B, II, J, D)
        x = x.view(D, B, II * J)
        layout = Layout.DBN_BND

    elif layout == "bijd->dbij":
        B, II, J, D = x.shape
        out_shape = (D, B, II, J)
        x = x.view(B, II * J, D)
        layout = Layout.BND_DBN

    else:
        raise ValueError(
            f"layout {layout} not supported. supported layouts are: {supported_layouts}"
        )

    out, _, _ = torch.ops.cuequivariance.layer_norm_transpose(
        x, w, b, eps, elementwise_affine, layout
    )
    return out.view(*out_shape)
