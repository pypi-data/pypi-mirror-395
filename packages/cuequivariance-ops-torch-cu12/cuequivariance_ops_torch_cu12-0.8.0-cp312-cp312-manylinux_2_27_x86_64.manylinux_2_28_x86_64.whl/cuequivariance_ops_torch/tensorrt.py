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

import numpy.typing as npt
import tensorrt as trt
import tensorrt.plugin as trtp
import torch

import cuequivariance_ops_torch._ext as ops
from cuequivariance_ops_torch.fused_layer_norm_torch import (
    Layout,
    _layer_norm_transpose,
)
from cuequivariance_ops_torch.fused_tensor_product import fused_tensor_product
from cuequivariance_ops_torch.triangle_attention import (
    _allocate_s_kv,
    _can_run_sm100f,
    _convert_bias,
    _fallback_threshold,
    _should_use_tf32,
    _triangle_attention_torch,
)


def register_plugins():
    pass


def trt_to_torch_dtype_dict():
    """
    Map of TRT dtype -> Torch dtype
    """
    return {
        trt.int32: torch.int32,
        trt.float32: torch.float32,
        trt.float16: torch.float16,
        trt.bfloat16: torch.bfloat16,
        trt.int64: torch.int64,
        trt.int8: torch.int8,
        trt.bool: torch.bool,
    }


def torch_to_trt_dtype_dict():
    """
    Map of Torch dtype -> TRT dtype
    """
    return {
        torch.int32: trt.int32,
        torch.float32: trt.float32,
        torch.float16: trt.float16,
        torch.bfloat16: trt.bfloat16,
        torch.int64: trt.int64,
        torch.int8: trt.int8,
        torch.bool: trt.bool,
    }


def _to_meta_one(desc):
    dtype = trt_to_torch_dtype_dict()[desc.dtype]
    shape = [s.constant_value() if s.is_constant else 0 for s in desc.shape_expr]
    return torch.empty(shape, dtype=dtype, device="meta")


def _from_meta_one(m):
    return trtp.from_shape_expr(
        [trtp.ShapeExpr(s if s > 0 else -1) for s in m.shape],
        dtype=torch_to_trt_dtype_dict()[m.dtype],
    )


def _to_meta(*args):
    return [None if a is None else _to_meta_one(a) for a in args]


def _from_meta(*args):
    return [None if a is None else _from_meta_one(a) for a in args]


def _to_torch(*args):
    ret = []
    for a in args:
        if a is None:
            ret = ret + [
                None,
            ]
        elif isinstance(a, trtp.Tensor):
            if a.dtype == trt.bfloat16:
                a._immutable = False
                a._dtype = trt.float16
                tt = torch.as_tensor(a, device="cuda").view(dtype=torch.bfloat16)
            else:
                tt = torch.as_tensor(a, device="cuda")
            ret = ret + [
                tt,
            ]
        else:
            raise ValueError(f"Unexpected type: {type(a)}")
    return ret


@trtp.register("cuequivariance::identity_2")
def _(
    s: trtp.TensorDesc, z: trtp.TensorDesc
) -> Tuple[trtp.TensorDesc, trtp.TensorDesc]:
    return s.like(), z.like()


@trtp.impl("cuequivariance::identity_2")
def _(
    s: trtp.Tensor,
    z: trtp.Tensor,
    outputs: Tuple[trtp.Tensor],
    stream: int,
):
    with torch.cuda.stream(torch.cuda.ExternalStream(stream)):
        s_, z_, s_copy, z_copy = _to_torch(s, z, outputs[0], outputs[1])
        s_copy.copy_(s_)
        z_copy.copy_(z_)


@trtp.register("cuequivariance::segmented_transpose")
def _(
    tensor: trtp.TensorDesc, segment_info: trtp.TensorDesc, contiguous: bool
) -> trtp.TensorDesc:
    return tensor.like()


@trtp.impl("cuequivariance::segmented_transpose")
def _(
    tensor: trtp.Tensor,
    segment_info: trtp.Tensor,
    contiguous: bool,
    outputs: Tuple[trtp.Tensor],
    stream: int,
):
    with torch.cuda.stream(torch.cuda.ExternalStream(stream)):
        tensor_ = torch.as_tensor(tensor, device="cuda")
        segment_info_ = torch.as_tensor(segment_info, device="cuda")
        ret = torch.as_tensor(outputs[0], device="cuda")
        ops.segmented_transpose(
            ret,
            tensor_,
            segment_info_,
            contiguous,
            stream,
        )


@trtp.register("cuequivariance::triangle_attention")
def _(
    q: trtp.TensorDesc,
    k: trtp.TensorDesc,
    v: trtp.TensorDesc,
    b: trtp.TensorDesc,
    mask: trtp.TensorDesc,
    scale: float,
) -> Tuple[trtp.TensorDesc, trtp.TensorDesc, trtp.TensorDesc]:
    aux = trtp.from_shape_expr(
        (q.shape_expr[0], q.shape_expr[1], q.shape_expr[2], q.shape_expr[3]),
        dtype=trt.float32,
    )
    return q.like(), aux, aux.like()


@trtp.register("cuequivariance::triangle_attention_mask")
def _(
    q: trtp.TensorDesc,
    k: trtp.TensorDesc,
    v: trtp.TensorDesc,
    b: trtp.TensorDesc,
    mask: trtp.TensorDesc,
    scale: float,
) -> trtp.TensorDesc:
    return q.like()


@trtp.register("cuequivariance::triangle_attention_nomask")
def _(
    q: trtp.TensorDesc,
    k: trtp.TensorDesc,
    v: trtp.TensorDesc,
    b: trtp.TensorDesc,
    scale: float,
) -> trtp.TensorDesc:
    return q.like()


def _tri_attn(q_, k_, v_, b_, mask_, scale, ret, lse, lse_max, stream):
    seq_len = q_.shape[-2]

    # print (f"seq_len = {seq_len}, threshold={_fallback_threshold()}")
    if lse is None and lse_max is None and seq_len <= _fallback_threshold():
        # Use original PyTorch implementation for short sequences
        _triangle_attention_torch(q_, k_, v_, b_, mask_, scale, out=ret)
    else:
        if lse is None:
            lse = q_.new_empty(q_.shape[:-1], dtype=torch.float32)
        if lse_max is None:
            lse_max = q_.new_empty(q_.shape[:-1], dtype=torch.float32)

        run_sm100f, device_cc = _can_run_sm100f(q_, k_)
        actual_s_kv = _allocate_s_kv(mask_, run_sm100f)
        b_ = _convert_bias(b_, q_, run_sm100f)

        ops.triangle_attention(
            ret,
            lse,
            lse_max,
            q_,
            k_,
            v_,
            mask_,
            actual_s_kv,
            b_,
            scale,
            _should_use_tf32(q_),
            device_cc,
            stream,
        )


@trtp.impl("cuequivariance::triangle_attention")
def _(
    q: trtp.Tensor,
    k: trtp.Tensor,
    v: trtp.Tensor,
    b: trtp.Tensor,
    mask: trtp.Tensor,
    scale: float,
    outputs: Tuple[trtp.Tensor],
    stream: int,
):
    with torch.cuda.stream(torch.cuda.ExternalStream(stream)):
        q_, k_, v_, b_, mask_, ret, lse, lse_max = _to_torch(q, k, v, b, mask, *outputs)
        _tri_attn(q_, k_, v_, b_, mask_, scale, ret, lse, lse_max, stream)


@trtp.impl("cuequivariance::triangle_attention_mask")
def _(
    q: trtp.Tensor,
    k: trtp.Tensor,
    v: trtp.Tensor,
    b: trtp.Tensor,
    mask: trtp.Tensor,
    scale: float,
    outputs: Tuple[trtp.Tensor],
    stream: int,
):
    with torch.cuda.stream(torch.cuda.ExternalStream(stream)):
        ret, q_, k_, v_, b_, mask_ = _to_torch(outputs[0], q, k, v, b, mask)
        _tri_attn(q_, k_, v_, b_, mask_, scale, ret, None, None, stream)


@trtp.impl("cuequivariance::triangle_attention_nomask")
def _(
    q: trtp.Tensor,
    k: trtp.Tensor,
    v: trtp.Tensor,
    b: trtp.Tensor,
    scale: float,
    outputs: Tuple[trtp.Tensor],
    stream: int,
):
    with torch.cuda.stream(torch.cuda.ExternalStream(stream)):
        ret, q_, k_, v_, b_ = _to_torch(outputs[0], q, k, v, b)
        _tri_attn(q_, k_, v_, b_, None, scale, ret, None, None, stream)


@trtp.register("cuequivariance::layer_norm_transpose")
def _(
    x: trtp.TensorDesc,
    w: trtp.TensorDesc,
    b: trtp.TensorDesc,
    eps: float,
    elementwise_affine: bool,
    layout: int,
) -> Tuple[trtp.TensorDesc, trtp.TensorDesc, trtp.TensorDesc]:
    if layout == Layout.BND_BND:
        B, N, D = x.shape_expr
        out = trtp.from_shape_expr((B, N, D), dtype=x.dtype)
    elif layout == Layout.BDN_BND:
        B, D, N = x.shape_expr
        out = trtp.from_shape_expr((B, N, D), dtype=x.dtype)
    elif layout == Layout.BND_BDN:
        B, N, D = x.shape_expr
        out = trtp.from_shape_expr((B, D, N), dtype=x.dtype)
    elif layout == Layout.DBN_BND:
        D, B, N = x.shape_expr
        out = trtp.from_shape_expr((B, N, D), dtype=x.dtype)
    elif layout == Layout.BND_DBN:
        B, N, D = x.shape_expr
        out = trtp.from_shape_expr((D, B, N), dtype=x.dtype)
    else:
        raise ValueError

    mean = trtp.from_shape_expr((B, N), dtype=trt.float32)
    rstd = trtp.from_shape_expr((B, N), dtype=trt.float32)
    return out, mean, rstd


@trtp.impl("cuequivariance::layer_norm_transpose")
def _(
    x: trtp.Tensor,
    w: trtp.Tensor,
    b: trtp.Tensor,
    eps: float,
    elementwise_affine: bool,
    layout: int,
    outputs: Tuple[trtp.Tensor],
    stream: int,
):
    x_, w_, b_ = _to_torch(x, w, b)
    out, mean, rstd = _to_torch(*outputs)
    if layout == Layout.BND_BND:
        B, N, D = x_.shape
    elif layout == Layout.BDN_BND:
        B, D, N = x_.shape
    elif layout == Layout.BND_BDN:
        B, N, D = x_.shape
    elif layout == Layout.DBN_BND:
        D, B, N = x_.shape
    elif layout == Layout.BND_DBN:
        B, N, D = x_.shape
    _layer_norm_transpose(
        x_, w_, b_, eps, elementwise_affine, layout, out, mean, rstd, B, N, D
    )


@trtp.register("cuequivariance::attention_pair_bias_mask")
def _(
    z: trtp.TensorDesc,
    w_proj_z: trtp.TensorDesc,
    b_proj_z: trtp.TensorDesc,
    w_ln: trtp.TensorDesc,
    b_ln: trtp.TensorDesc,
    mask: trtp.TensorDesc,
    num_heads: int,
    multiplicity: int,
    eps: float,
    inf: float,
    grad_enabled: bool,
    return_z_proj: bool,
    is_cached_z_proj: bool,
    valid_optional_inputs: npt.NDArray[bool],
) -> Tuple[trtp.TensorDesc, trtp.TensorDesc]:
    if is_cached_z_proj:
        B, _, U, V = z.shape_expr
        DIM_Z = None
    else:
        B, U, V, DIM_Z = z.shape_expr

    out_mask = trtp.from_shape_expr((B * multiplicity, num_heads, U, V), dtype=z.dtype)
    if is_cached_z_proj:
        z_proj = z.like()
    else:
        z_proj = trtp.from_shape_expr((B, num_heads, U, V), dtype=z.dtype)
    return out_mask, z_proj


@trtp.impl("cuequivariance::attention_pair_bias_mask")
def _(
    z: trtp.Tensor,
    w_proj_z: trtp.Tensor,
    b_proj_z: trtp.Tensor,
    w_ln: trtp.Tensor,
    b_ln: trtp.Tensor,
    mask: trtp.Tensor,
    num_heads: int,
    multiplicity: int,
    eps: float,
    inf: float,
    grad_enabled: bool,
    return_z_proj: bool,
    is_cached_z_proj: bool,
    valid_optional_inputs: npt.NDArray[bool],
    outputs: Tuple[trtp.Tensor],
    stream: int,
):
    with torch.cuda.stream(torch.cuda.ExternalStream(stream)):
        (z_, w_proj_z_, b_proj_z_, w_ln_, b_ln_, mask_) = _to_torch(
            z, w_proj_z, b_proj_z, w_ln, b_ln, mask
        )
        out_mask_, z_proj_ = _to_torch(*outputs)
        out_mask, z_proj, _, _, _ = torch.ops.cuequivariance.attention_pair_bias_mask(
            z_,
            w_proj_z_,
            b_proj_z_,
            w_ln_,
            b_ln_,
            mask_,
            num_heads,
            multiplicity,
            eps,
            inf,
            grad_enabled,
            return_z_proj,
            is_cached_z_proj,
            valid_optional_inputs,
        )
        out_mask_.copy_(out_mask)
        z_proj_.copy_(z_proj)


@trtp.register("cuequivariance::tri_mul_update")
def _(
    x: trtp.TensorDesc,
    mask: trtp.TensorDesc,
    norm_in_weight: trtp.TensorDesc,
    norm_in_bias: trtp.TensorDesc,
    p_in_weight: trtp.TensorDesc,
    p_in_bias: trtp.TensorDesc,
    g_in_weight: trtp.TensorDesc,
    g_in_bias: trtp.TensorDesc,
    norm_out_weight: trtp.TensorDesc,
    norm_out_bias: trtp.TensorDesc,
    p_out_weight: trtp.TensorDesc,
    p_out_bias: trtp.TensorDesc,
    g_out_weight: trtp.TensorDesc,
    g_out_bias: trtp.TensorDesc,
    direction: str,
    eps: float,
    precision: int,
    valid_mask_in_out_bias: npt.NDArray[bool],
) -> trtp.TensorDesc:
    return x.like()


def _tri_mul_update_impl(
    stream: int,
    direction: str,
    eps: float,
    precision: int,
    valid_mask_in_out_bias: npt.NDArray[bool],
    *inouts,
):
    with torch.cuda.stream(torch.cuda.ExternalStream(stream)):
        (
            out,
            x,
            mask,
            norm_in_weight,
            norm_in_bias,
            p_in_weight,
            p_in_bias,
            g_in_weight,
            g_in_bias,
            norm_out_weight,
            norm_out_bias,
            p_out_weight,
            p_out_bias,
            g_out_weight,
            g_out_bias,
        ) = _to_torch(*inouts)
        # QDP has issues with sending string arguments
        direction = direction.rstrip("\0")

        ret = torch.ops.cuequivariance.tri_mul_update(
            x,
            mask,
            norm_in_weight,
            norm_in_bias,
            p_in_weight,
            p_in_bias,
            g_in_weight,
            g_in_bias,
            norm_out_weight,
            norm_out_bias,
            p_out_weight,
            p_out_bias,
            g_out_weight,
            g_out_bias,
            direction,
            eps,
            precision,
            valid_mask_in_out_bias,
        )
        out.copy_(ret)


@trtp.impl("cuequivariance::tri_mul_update")
def _(
    x: trtp.Tensor,
    mask: trtp.Tensor,
    norm_in_weight: trtp.Tensor,
    norm_in_bias: trtp.Tensor,
    p_in_weight: trtp.Tensor,
    p_in_bias: trtp.Tensor,
    g_in_weight: trtp.Tensor,
    g_in_bias: trtp.Tensor,
    norm_out_weight: trtp.Tensor,
    norm_out_bias: trtp.Tensor,
    p_out_weight: trtp.Tensor,
    p_out_bias: trtp.Tensor,
    g_out_weight: trtp.Tensor,
    g_out_bias: trtp.Tensor,
    direction: str,
    eps: float,
    precision: int,
    valid_mask_in_out_bias: npt.NDArray[bool],
    outputs: Tuple[trtp.Tensor],
    stream: int,
):
    _tri_mul_update_impl(
        stream,
        direction,
        eps,
        precision,
        valid_mask_in_out_bias,
        outputs[0],
        x,
        mask,
        norm_in_weight,
        norm_in_bias,
        p_in_weight,
        p_in_bias,
        g_in_weight,
        g_in_bias,
        norm_out_weight,
        norm_out_bias,
        p_out_weight,
        p_out_bias,
        g_out_weight,
        g_out_bias,
    )


def update_batch_size(batch_size, t):
    if t is None:
        return batch_size  # unused tensor
    if t[1].is_constant and t[1].constant_value() == 0:
        return batch_size  # unused tensor
    if t[0].is_constant and t[0].constant_value() == 1:
        return batch_size  # shared tensor
    return t[0]  # first batched tensor


def get_batch_size(in0, in1, in2):
    result = trtp.ShapeExpr(1)
    result = update_batch_size(result, in0)
    result = update_batch_size(result, in1)
    result = update_batch_size(result, in2)
    return result


@trtp.register("cuequivariance::fused_tensor_product")
def _(
    in0: trtp.TensorDesc,
    in1: trtp.TensorDesc,
    in2: trtp.TensorDesc,
    tp_path_csr_offsets_fwd: trtp.TensorDesc,
    tp_path_csr_offsets_dgrad_in0: trtp.TensorDesc,
    tp_path_csr_offsets_dgrad_in1: trtp.TensorDesc,
    tp_path_csr_offsets_dgrad_in2: trtp.TensorDesc,
    tp_path_offsets_fwd: trtp.TensorDesc,
    tp_path_offsets_dgrad_in0: trtp.TensorDesc,
    tp_path_offsets_dgrad_in1: trtp.TensorDesc,
    tp_path_offsets_dgrad_in2: trtp.TensorDesc,
    tp_path_cg_values_fwd: trtp.TensorDesc,
    tp_path_cg_values_dgrad_in0: trtp.TensorDesc,
    tp_path_cg_values_dgrad_in1: trtp.TensorDesc,
    tp_path_cg_values_dgrad_in2: trtp.TensorDesc,
    connection_mode: int,
    output_stride: int,
) -> trtp.TensorDesc:
    if not in0.shape_expr[0].is_fake:
        bs = get_batch_size(in0.shape_expr, in1.shape_expr, in2.shape_expr)
        return trtp.from_shape_expr((bs, output_stride), dtype=in0.dtype)
    else:
        return in0.like()


@trtp.impl("cuequivariance::fused_tensor_product")
def _(
    in0: trtp.Tensor,
    in1: trtp.Tensor,
    in2: trtp.Tensor,
    tp_path_csr_offsets_fwd: trtp.Tensor,
    tp_path_csr_offsets_dgrad_in0: trtp.Tensor,
    tp_path_csr_offsets_dgrad_in1: trtp.Tensor,
    tp_path_csr_offsets_dgrad_in2: trtp.Tensor,
    tp_path_offsets_fwd: trtp.Tensor,
    tp_path_offsets_dgrad_in0: trtp.Tensor,
    tp_path_offsets_dgrad_in1: trtp.Tensor,
    tp_path_offsets_dgrad_in2: trtp.Tensor,
    tp_path_cg_values_fwd: trtp.Tensor,
    tp_path_cg_values_dgrad_in0: trtp.Tensor,
    tp_path_cg_values_dgrad_in1: trtp.Tensor,
    tp_path_cg_values_dgrad_in2: trtp.Tensor,
    connection_mode: int,
    output_stride: int,
    outputs: Tuple[trtp.Tensor],
    stream: int,
):
    (
        in0_,
        in1_,
        in2_,
        tp_path_csr_offsets_fwd_,
        tp_path_offsets_fwd_,
        tp_path_cg_values_fwd_,
    ) = _to_torch(
        in0,
        in1,
        in2,
        tp_path_csr_offsets_fwd,
        tp_path_offsets_fwd,
        tp_path_cg_values_fwd,
    )
    (result_,) = _to_torch(outputs[0])

    with torch.cuda.stream(torch.cuda.ExternalStream(stream)):
        result = fused_tensor_product(
            in0_,
            in1_,
            in2_,
            tp_path_csr_offsets_fwd_,
            None,
            None,
            None,
            tp_path_offsets_fwd_,
            None,
            None,
            None,
            tp_path_cg_values_fwd_,
            None,
            None,
            None,
            connection_mode,
            output_stride,
        )
        result_.copy_(result)


"""
try:
    from torch_tensorrt.dynamo.conversion.plugins import generate_plugin_converter

    generate_plugin_converter(
        "cuequivariance::triangle_attention", supports_dynamic_shapes=True
    )
    generate_plugin_converter(
        "cuequivariance::triangle_attention_mask", supports_dynamic_shapes=True
    )
    generate_plugin_converter(
        "cuequivariance::triangle_attention_nomask", supports_dynamic_shapes=True
    )
except Exception as e:
    raise e
"""
