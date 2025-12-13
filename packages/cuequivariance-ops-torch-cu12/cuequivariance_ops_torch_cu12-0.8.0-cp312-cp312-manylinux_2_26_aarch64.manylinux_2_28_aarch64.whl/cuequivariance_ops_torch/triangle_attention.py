# SPDX-FileCopyrightText: Copyright (c) 2024 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: LicenseRef-NvidiaProprietary
#
# NVIDIA CORPORATION, its affiliates and licensors retain all intellectual
# property and proprietary rights in and to this material, related
# documentation and any modifications thereto. Any use, reproduction,
# disclosure or distribution of this material and related documentation
# without an express license agreement from NVIDIA CORPORATION or
# its affiliates is strictly prohibited.

import math
import os
import warnings
from typing import List, Optional, Tuple

import torch

import cuequivariance_ops_torch._ext as ops
from cuequivariance_ops_torch.utils import is_in_export_mode, maybe_to

CUEQ_TRIATTN_FALLBACK_THRESHOLD: int = int(
    os.getenv("CUEQ_TRIATTN_FALLBACK_THRESHOLD", "100")
)

warnings.simplefilter("once")


@torch.jit.ignore
def _get_device_cc(device: torch.device) -> List[int]:
    """Get CUDA compute capability of the device.

    Args:
        device: The torch CUDA device to query for compute capability.

    Returns:
        A list of two integers representing the major and minor version of the
        compute capability (e.g., [8, 0] for compute capability 8.0).
    """
    # Torch custom_op schema doesn't support Tuple[int, int], so we need to convert it to List[int]
    return list(torch.cuda.get_device_capability(device=device))


def _fallback_threshold():
    """
    Returns cached value of the environment variable
    """
    return CUEQ_TRIATTN_FALLBACK_THRESHOLD


@torch.jit.ignore
def _should_use_tf32(q) -> bool:
    """
    Whether or not TF32 triangle attention kernel should be used for q
    Always False for 16-bit types, otehrwise depends on global setting and env
    """
    if q.dtype != torch.float32:
        return False
    tf32_override = os.getenv("NVIDIA_TF32_OVERRIDE")
    return (
        tf32_override != "0" and torch.backends.cuda.matmul.allow_tf32
    ) or tf32_override == "1"


def _permute_final_dims(tensor: torch.Tensor, inds: List[int]):
    zero_index = -1 * len(inds)
    first_inds = list(range(len(tensor.shape[:zero_index])))
    return tensor.permute(first_inds + [zero_index + i for i in inds])


def _triangle_attention_torch(
    query: torch.Tensor,
    key: torch.Tensor,
    value: torch.Tensor,
    bias: torch.Tensor,
    mask: Optional[torch.Tensor] = None,
    scale: Optional[float] = None,
    out: Optional[torch.Tensor] = None,
):
    """PyTorch reference implementation matching CUDA kernel API and precision. Fallback option for short sequences."""
    if scale is None:
        scale = 1.0 / (query.shape[-1] ** 0.5)

    # Permute key for matrix multiplication
    key = _permute_final_dims(key, (1, 0))

    # Compute attention scores
    a = torch.matmul(query * scale, key)

    # Add biases
    if mask is not None:
        mask = -1e9 * (~mask).float()
        biases = [mask, bias]
    else:
        biases = [bias]

    for b in biases:
        a += b

    a = torch.nn.functional.softmax(a, -1)
    if out is None:
        a = torch.matmul(a, value)
    else:
        a = torch.matmul(a, value, out=out)
    return a


def _can_run_sm100f(q, k, training=False):
    """
    Checks sm100f kernel support conditions for q and k on current device
    sm100f kernel requires:
    1. Compiled with CUDA 13.0+ (build-time requirement)
    2. cc 10.0 or 10.3 (runtime device requirement)
    3. q, k and v are of dtype BF16 or FP16
    4. q.shape[1] == q.shape[3] == k.dim(3) is multiple of 8
    5. q.shape[-1] (hidden dimension) is multiple of 8 and <= 128
    6. bias is of same dtype as q/k/v
    TODO: support FP32/TF32 in sm100f kernel
    """
    # Check if SM100f kernels were compiled (requires CUDA 13.0+)
    if not ops.has_sm100f_support():
        return False, _get_device_cc(q.device)

    device_cc = _get_device_cc(q.device)
    device_can_run_sm100f = device_cc == [10, 0] or device_cc == [10, 3]
    hidden_dim = q.shape[-1]

    run_sm100f = (
        device_can_run_sm100f
        and q.dtype in [torch.bfloat16, torch.float16]
        and hidden_dim <= 128
        and hidden_dim % 8 == 0
    )

    # only forward kernel has this limitation
    if run_sm100f and (not training) and k.shape[3] % 8 != 0:
        # When all other conditions are met except for S_kv % 8 == 0,
        # we issue a warning to let the user know so that they can pad their
        # input to use the kernel. We don't want to implicitly pad the input here
        # because we would otherwise have to handle the padding for backward pass
        # and because it's usually way more efficient to pad from the beginning
        # of the data or model workflow than padding at every triangle_attention API
        # call.
        run_sm100f = False
        warnings.warn(
            "Can't use SM100f kernel because q.shape[3] is not a multiple of 8. Please consider padding for maximum performance on Blackwell."
        )
    return run_sm100f, device_cc


def _convert_bias(bias, q, run_sm100f):
    """
    Converts bias according to sm100f/sm80 kernel requirements
    FIXME: bias.dtype consistency across different kernels
    """
    if run_sm100f:
        # sm100f kernel requires bias to be same dtype as q
        if bias.dtype != q.dtype:
            warnings.warn(
                f"SM100f kernel expects bias to be of the same dtype as q so it's going to be cast to {q.dtype}. Check if you can change your code for maximum performance on Blackwell."
            )
            bias = bias.to(q.dtype)
    else:
        # non-sm100f kernel requires bias to be float32
        if bias.dtype != torch.float32:
            warnings.warn(
                "Non-SM100f kernel expects bias to be float32 so it's going to be cast to torch.float32. Check if you can change your code for maximum performance."
            )
            bias = bias.to(torch.float32)
    return bias


def _allocate_s_kv(mask, run_sm100f):
    """
    Allocates extra buffer for sm100f kernel, if needed
    """
    if mask is not None and run_sm100f:
        # a pytorch-managed memory buffer for storing actual_s_kv internally
        actual_s_kv = torch.empty(
            mask.shape[:2],
            dtype=torch.int32,
            device=mask.device,
        ).requires_grad_(False)
    else:
        # when mask is None, actual_s_kv needs to be None
        actual_s_kv = None
    return actual_s_kv


# TODO: support needs_input_grad
@torch.library.custom_op(
    "cuequivariance::triangle_attention_bwd",
    mutates_args=(),
    device_types="cuda",
)
def _(
    d_o: torch.Tensor,
    o: torch.Tensor,
    q: torch.Tensor,
    k: torch.Tensor,
    v: torch.Tensor,
    bias: torch.Tensor,
    mask: Optional[torch.Tensor],
    lse: torch.Tensor,
    scale: Optional[float],
) -> List[torch.Tensor]:
    """
    Custom Torch operation for backward pass of triangle attention
    """
    B = q.shape[0]
    N = q.shape[1]
    H = q.shape[2]
    S_qo = q.shape[3]
    S_kv = k.shape[3]
    hidden_dim = q.shape[-1]

    if k.shape != (B, N, H, S_kv, hidden_dim):
        raise ValueError(
            "triangle_attention_bwd: input k must have shape (B, N, H, S_kv, hidden_dim) but got: "
            f"{k.shape}"
        )
    if v.shape != (B, N, H, S_kv, hidden_dim):
        raise ValueError(
            "triangle_attention_bwd: input v must have shape (B, N, H, S_kv, hidden_dim) but got: "
            f"{v.shape}"
        )
    if bias.shape != (B, 1, H, S_qo, S_kv):
        raise ValueError(
            "triangle_attention_bwd: input bias must have shape (B, 1, H, S_qo, S_kv) but got: "
            f"{bias.shape}"
        )
    if mask is not None and mask.shape != (B, N, 1, 1, S_kv):
        raise ValueError(
            "triangle_attention_bwd: input mask must have shape (B, N, 1, 1, S_kv) but got: "
            f"{mask.shape}"
        )

    if d_o.shape != (B, N, H, S_qo, hidden_dim):
        raise ValueError(
            "triangle_attention_bwd: input d_o must have shape (B, N, H, S_qo, hidden_dim) but got: "
            f"{d_o.shape}"
        )

    if o.shape != (B, N, H, S_qo, hidden_dim):
        raise ValueError(
            "triangle_attention_bwd: input o must have shape (B, N, H, S_qo, hidden_dim) but got: "
            f"{o.shape}"
        )

    if lse.shape != (B, N, H, S_qo):
        raise ValueError(
            "triangle_attention_bwd: input lse must have shape (B, N, H, S_qo, 1) but got: "
            f"{lse.shape}"
        )

    # There are usage cases, e.g., custom autograd.Function that fuses TriAttn
    # with other ops, which requires manual calling of triangle_attention_bwd
    # so we need to re-establish the sm100f run condition here.
    run_sm100f, device_cc = _can_run_sm100f(q, k, True)
    bias = _convert_bias(bias, q, run_sm100f)

    q = q.detach().contiguous()
    k = k.detach().contiguous()
    v = v.detach().contiguous()
    bias = bias.detach().contiguous()
    d_q = torch.zeros_like(q)
    d_k = torch.empty_like(k)
    d_v = torch.empty_like(v)
    d_tb = torch.zeros_like(bias)
    d_o_dot = q.new_empty(q.shape[:-1], dtype=torch.float32)
    dq_fp32_buf = (
        d_q if q.dtype == torch.float32 else q.new_zeros(q.shape, dtype=torch.float32)
    )
    stream = torch.cuda.current_stream().cuda_stream
    use_tf32 = _should_use_tf32(q)

    d_tb_fp32_buf = None
    if run_sm100f:
        # sm100f kernel requires an additional fp32 buffer for triangle_bias,
        # which has to be zero initialized and with a shape along the (S_qo, S_kv)
        # multiple of 64 and 128
        shape_d_tb_fp32_buf = list(d_tb.shape)
        shape_d_tb_fp32_buf[-2] = math.ceil(shape_d_tb_fp32_buf[-2] / 64) * 64
        shape_d_tb_fp32_buf[-1] = math.ceil(shape_d_tb_fp32_buf[-1] / 128) * 128
        d_tb_fp32_buf = torch.zeros(
            shape_d_tb_fp32_buf, dtype=torch.float32, device=d_tb.device
        )

    if mask is not None:
        mask = mask.to(dtype=torch.bool).detach().contiguous()

    ops.triangle_attention_bwd(
        d_q,
        d_k,
        d_v,
        d_tb,
        d_o_dot,
        dq_fp32_buf,
        d_tb_fp32_buf,
        d_o.detach().contiguous(),
        o.detach().contiguous(),
        lse.detach().contiguous(),
        q,
        k,
        v,
        mask,
        bias,
        scale,
        use_tf32,
        device_cc,
        stream,
    )

    return d_q, d_k, d_v, d_tb


@torch.library.register_fake(
    "cuequivariance::triangle_attention_bwd",
)
def _(
    d_o: torch.Tensor,
    o: torch.Tensor,
    q: torch.Tensor,
    k: torch.Tensor,
    v: torch.Tensor,
    bias: torch.Tensor,
    mask: Optional[torch.Tensor],
    lse: torch.Tensor,
    scale: Optional[float],
) -> List[torch.Tensor]:
    """
    Fake Torch operation for backward pass of triangle attention
    """
    return (
        torch.empty_like(q),
        torch.empty_like(k),
        torch.empty_like(v),
        torch.empty_like(bias),
    )


def ensure_dims(ten: torch.Tensor, n: int) -> torch.Tensor:
    while len(ten.shape) < n:
        ten = ten.unsqueeze(0)
    return ten


@torch.library.custom_op(
    "cuequivariance::triangle_attention",
    mutates_args=(),
    device_types="cuda",
)
def _(
    q: torch.Tensor,
    k: torch.Tensor,
    v: torch.Tensor,
    bias: torch.Tensor,
    mask: Optional[torch.Tensor] = None,
    scale: Optional[float] = None,
) -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
    """
    Custom Torch operation for forward pass of triangle attention
    FIXME: softmax_lse and softmax_max dtype consistency with q/k/v
    """
    stream = torch.cuda.current_stream().cuda_stream
    q = q.detach().contiguous()
    o = torch.empty_like(q)
    softmax_lse = q.new_empty(q.shape[:-1], dtype=torch.float32)
    softmax_max = q.new_empty(q.shape[:-1], dtype=torch.float32)

    run_sm100f, device_cc = _can_run_sm100f(q, k, False)
    actual_s_kv = _allocate_s_kv(mask, run_sm100f)
    bias = _convert_bias(bias, q, run_sm100f)

    # Call kernel
    ops.triangle_attention(
        o,
        softmax_lse,
        softmax_max,
        q,
        k.detach().contiguous(),
        v.detach().contiguous(),
        mask,
        actual_s_kv,
        bias.detach().contiguous(),
        scale,
        _should_use_tf32(q),
        device_cc,
        stream,
    )
    return o, softmax_lse, softmax_max


@torch.library.register_fake(
    "cuequivariance::triangle_attention",
)
def _(
    q: torch.Tensor,
    k: torch.Tensor,
    v: torch.Tensor,
    bias: torch.Tensor,
    mask: Optional[torch.Tensor] = None,
    scale: Optional[float] = None,
) -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
    """
    Fake Torch operation for forward pass of triangle attention
    """
    return (torch.empty_like(q), q.new_empty(q.shape[:-1]), q.new_empty(q.shape[:-1]))


def _backward(ctx, d_output, *args):
    """
    Autograd fixture for backward pass of triangle attention
    """
    q, k, v, bias, o, lse = ctx.saved_tensors
    d_q, d_k, d_v, dbias = torch.ops.cuequivariance.triangle_attention_bwd(
        d_output,
        o,
        q,
        k,
        v,
        bias,
        ctx.mask,
        lse,
        ctx.scale,
    )
    return d_q, d_k, d_v, dbias, None, None


def _setup_context(ctx, inputs, output):
    """
    Autograd fixture for backward pass of triangle attention
    """
    q, k, v, bias, mask, scale = inputs
    o, lse, _ = output
    ctx.save_for_backward(q, k, v, bias, o, lse)
    ctx.mask = mask.detach() if mask is not None else None
    ctx.scale = scale


torch.library.register_autograd(
    "cuequivariance::triangle_attention",
    _backward,
    setup_context=_setup_context,
)


@torch.library.custom_op(
    "cuequivariance::triangle_attention_mask",
    mutates_args=(),
    device_types="cuda",
)
def _(
    q: torch.Tensor,
    k: torch.Tensor,
    v: torch.Tensor,
    bias: torch.Tensor,
    mask: torch.Tensor,
    scale: float,
) -> torch.Tensor:
    o, _, _ = torch.ops.cuequivariance.triangle_attention(
        q, k, v, bias, mask, scale=scale
    )
    return o


@torch.library.register_fake(
    "cuequivariance::triangle_attention_mask",
)
def _(
    q: torch.Tensor,
    k: torch.Tensor,
    v: torch.Tensor,
    bias: torch.Tensor,
    mask: torch.Tensor,
    scale: float,
) -> torch.Tensor:
    return torch.empty_like(q)


@torch.library.custom_op(
    "cuequivariance::triangle_attention_nomask",
    mutates_args=(),
    device_types="cuda",
)
def _(
    q: torch.Tensor,
    k: torch.Tensor,
    v: torch.Tensor,
    bias: torch.Tensor,
    scale: float,
) -> torch.Tensor:
    o, _, _ = torch.ops.cuequivariance.triangle_attention(q, k, v, bias, scale=scale)
    return o


@torch.library.register_fake(
    "cuequivariance::triangle_attention_nomask",
)
def _(
    q: torch.Tensor,
    k: torch.Tensor,
    v: torch.Tensor,
    bias: torch.Tensor,
    scale: float,
) -> torch.Tensor:
    return torch.empty_like(q)


def triangle_attention(
    q: torch.Tensor,
    k: torch.Tensor,
    v: torch.Tensor,
    bias: torch.Tensor,
    mask: Optional[torch.Tensor] = None,
    scale: Optional[float] = None,
    return_aux: bool = False,
) -> torch.Tensor | Tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
    # To achieve runtime q.shape check along specific axes for sm100f kernel,
    # we need to make sure q.ndim is 5
    # FIXME: understand the usage requirement from ensure_dims and replace
    # ensure_dims with more specific assertion than silently prepending singleton
    # dimensions.
    q = ensure_dims(q, 5)
    k = ensure_dims(k, 5)
    v = ensure_dims(v, 5)
    bias = ensure_dims(bias, 5)

    # Handle mask if provided
    if mask is not None:
        # mask is never differentiable
        mask = ensure_dims(mask.to(dtype=torch.bool), 5).detach().contiguous()

    B = q.shape[0]
    N = q.shape[1]
    H = q.shape[2]
    S_qo = q.shape[3]
    S_kv = k.shape[3]
    hidden_dim = q.shape[-1]

    if k.shape != (B, N, H, S_kv, hidden_dim):
        raise ValueError(
            "triangle_attention: input k must have shape (B, N, H, S_kv, hidden_dim) but got: "
            f"{k.shape}"
        )
    if v.shape != (B, N, H, S_kv, hidden_dim):
        raise ValueError(
            "triangle_attention: input v must have shape (B, N, H, S_kv, hidden_dim) but got: "
            f"{v.shape}"
        )
    if bias.shape != (B, 1, H, S_qo, S_kv):
        raise ValueError(
            "triangle_attention: input bias must have shape (B, 1, H, S_qo, S_kv) but got: "
            f"{bias.shape}"
        )
    if mask is not None and mask.shape != (B, N, 1, 1, S_kv):
        raise ValueError(
            "triangle_attention: input mask must have shape (B, N, 1, 1, S_kv) but got: "
            f"{mask.shape}"
        )

    """
    torch.get_autocast_dtype breaks jit.script() here
    and we don't want this conversion inside the custom op
    (because then we have no way of saving casted q,k,v for backward except returning them)
    Since scripting under autocast is not super reliable anyway, we just do autocast here.
    Chances that q, k and v are not cast by this time are slim, too - so the worst that can
    happen is we lose some efficiency in that exotic case of autocast + jit.script().
    """
    # Handle autocast first to get the actual dtype we'll be working with
    if not torch._jit_internal.is_scripting():
        if torch.is_autocast_enabled():
            autocast_dtype = torch.get_autocast_dtype("cuda")
            q = maybe_to(q, autocast_dtype)
            k = maybe_to(k, autocast_dtype)
            v = maybe_to(v, autocast_dtype)

    # Now check the actual dtype we're working with
    dtype = q.dtype
    FORCE_FALLBACK = 1000000

    actual_threshold = (
        100 if torch._jit_internal.is_scripting() else CUEQ_TRIATTN_FALLBACK_THRESHOLD
    )

    if dtype == torch.float16 or dtype == torch.bfloat16:
        # Check if we can use the kernel backend based on hidden_dim restrictions
        # Otherwise use fallback
        if hidden_dim > 128 or hidden_dim % 8 != 0:
            actual_threshold = FORCE_FALLBACK
            if return_aux:
                raise ValueError(
                    f"return_aux requires hidden_dim % 8 == 0 and <= 128 for {dtype}, "
                    f"got hidden_dim={hidden_dim}"
                )

        # Make threshold higher for small hidden dimensions
        elif hidden_dim < 32:
            actual_threshold = max(actual_threshold, 200)

    elif dtype == torch.float32:
        # Check kernel restrictions
        if hidden_dim > 32 or hidden_dim % 4 != 0:
            actual_threshold = FORCE_FALLBACK
            if return_aux:
                raise ValueError(
                    f"return_aux requires hidden_dim % 4 == 0 and <= 32 for {dtype}, "
                    f"got hidden_dim={hidden_dim}"
                )
        # Make threshold higher for small hidden dimensions
        elif hidden_dim < 32:
            actual_threshold = max(actual_threshold, 200)

    if return_aux:
        # We do not simulate extra return values in fallback
        actual_threshold = 0
    else:
        if not torch.jit.is_scripting():
            if is_in_export_mode() and actual_threshold != FORCE_FALLBACK:
                # Force no fallback, TRT plugin has internal fallback
                actual_threshold = 0

    # Falling back to Torch if threshold is not met
    if q.size(3) <= actual_threshold:
        return _triangle_attention_torch(q, k, v, bias, mask, scale)

    if scale is None:
        scale = 1.0 / (q.shape[-1] ** 0.5)

    if torch.jit.is_scripting():
        use_real_op = True
    else:
        use_real_op = not is_in_export_mode()
    if use_real_op:
        output, sm_lse, sm_max = torch.ops.cuequivariance.triangle_attention(
            q,
            k,
            v,
            bias,
            mask,
            scale=scale,
        )
        if return_aux:
            return output, sm_lse, sm_max
        else:
            return output
    else:
        if mask is None:
            output = torch.ops.cuequivariance.triangle_attention_nomask(
                q, k, v, bias, scale=scale
            )
        else:
            output = torch.ops.cuequivariance.triangle_attention_mask(
                q, k, v, bias, mask, scale=scale
            )
        return output
