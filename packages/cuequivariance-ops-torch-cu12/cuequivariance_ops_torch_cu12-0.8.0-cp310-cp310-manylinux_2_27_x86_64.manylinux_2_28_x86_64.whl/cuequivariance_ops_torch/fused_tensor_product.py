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
from typing import List, Optional

import torch
import torch.nn as nn

import cuequivariance_ops_torch._ext as ops
from cuequivariance_ops_torch.utils import (
    get_operator_from_module,
    maybe_detach,
    maybe_empty_like,
)

op4_mode_mappings = {
    "u__u_u": "UVU",
    "u__uw_w": "U1W",
    "u__uv_v": "U1W",
    "_v_vw_w": "1VW",
    "u_v_uv_u": "UVU",
    "u_v_uv_v": "UVV",
    "u_u_uw_w": "UUW",
    "u_v_uvw_w": "UVW",
}

op3_mode_mappings = {
    "u_u_u": "UUU",
    "u_v_uv": "UVUV",
    "u_uv_v": "UUVV",
    "u__u": "U1U1",
    "_v_v": "1V1V",
}


all_mode_mappings = {**op3_mode_mappings, **op4_mode_mappings}


mode_mappings_to_int = {}
int_mappings_to_mode = {}
int_mode = 0
for mode in all_mode_mappings.values():
    mode_mappings_to_int[mode] = int_mode
    int_mappings_to_mode[int_mode] = mode
    int_mode += 1


# Determines if in2 operand is needed
def mode_is_op4(mode: int):
    return mode >= len(op3_mode_mappings)


def sort_tensor_product_info_for_operand(
    path_offsets_and_dims: torch.Tensor, path_cg_values: torch.Tensor, op_idx: int
):
    # idx = 0 -> in0
    # idx = 1 -> in1
    # idx = 2 -> in2
    # idx = 3 -> out
    key = path_offsets_and_dims[:, op_idx]
    perm = key.sort(descending=False, stable=True)[1]
    return path_offsets_and_dims[perm, :], path_cg_values[perm]


def path_offsets_to_csr(
    path_offsets_and_dims: torch.Tensor, op_idx: int, op_stride: int
):
    diff = torch.diff(
        path_offsets_and_dims[:, op_idx],
        n=1,
        append=path_offsets_and_dims.new_tensor([op_stride]),
    )
    path_csr_offsets = diff.nonzero().to(dtype=torch.int32).squeeze(dim=1)
    path_csr_offsets = torch.cat(
        [
            path_csr_offsets.new_tensor([0]),
            path_csr_offsets + 1,
        ]
    )
    return path_csr_offsets


def make_tensor_product_info(
    op_idx: int,
    op_stride: int,
    path_offsets: torch.Tensor,
    path_cg_values: torch.Tensor,
):
    path_offsets = path_offsets.clone().detach()
    path_cg_values = path_cg_values.clone().detach()
    path_offsets, path_cg_values = sort_tensor_product_info_for_operand(
        path_offsets, path_cg_values, op_idx
    )
    path_csr_offsets = path_offsets_to_csr(path_offsets, op_idx, op_stride)

    path_cg_values = path_cg_values
    path_offsets = path_offsets
    path_csr_offsets = path_csr_offsets

    return (
        path_csr_offsets,
        path_offsets,
        path_cg_values,
    )


def make_tensor_product_infos(
    strides: list[int],
    path_offsets_and_dims: list[int],
    path_cg_values: list[float],
    math_dtype: torch.dtype,
):
    path_cg_values = torch.tensor(path_cg_values, dtype=math_dtype)
    path_offsets_and_dims = torch.IntTensor(path_offsets_and_dims)

    tp_infos = None

    if len(strides) == 4:
        tp_infos = (
            make_tensor_product_info(
                3, strides[3], path_offsets_and_dims, path_cg_values
            ),
            make_tensor_product_info(
                0, strides[0], path_offsets_and_dims, path_cg_values
            ),
            make_tensor_product_info(
                1, strides[1], path_offsets_and_dims, path_cg_values
            ),
            make_tensor_product_info(
                2, strides[2], path_offsets_and_dims, path_cg_values
            ),
        )

    elif len(strides) == 3:
        tp_infos = (
            make_tensor_product_info(
                2, strides[2], path_offsets_and_dims, path_cg_values
            ),
            make_tensor_product_info(
                0, strides[0], path_offsets_and_dims, path_cg_values
            ),
            make_tensor_product_info(
                1, strides[1], path_offsets_and_dims, path_cg_values
            ),
        )

    else:
        raise NotImplementedError

    return tp_infos


class TensorProductPathData(nn.Module):
    def __init__(
        self,
        path_csr_offsets: torch.Tensor,
        path_offsets: torch.Tensor,
        path_cg_values: torch.Tensor,
        math_dtype: torch.dtype,
    ):
        super().__init__()
        # for now, don't have these buffers as part of the state dict to avoid
        # breaking changes w.r.t. loading state-dicts for now
        self.register_buffer("path_csr_offsets", path_csr_offsets, persistent=False)
        self.register_buffer("path_offsets", path_offsets, persistent=False)
        # Register float cg_values as int via bitcasting, so that model.to(dtype)
        # won't affect the precision of cg_values buffer
        if math_dtype == torch.float32:
            int_type = torch.int32
        elif math_dtype == torch.float64:
            int_type = torch.int64
        else:
            msg = "Unsupported dtype for path_cg_values, expected torch.float32 or torch.float64"
            msg += f", but got {path_cg_values.dtype}"
            raise ValueError(msg)

        self.register_buffer(
            "path_cg_values",
            path_cg_values.to(dtype=math_dtype).view(dtype=int_type),
            persistent=False,
        )

    @torch.jit.ignore
    def forward(self, *args, **kwargs):
        raise NotImplementedError(
            "TensorProductPathData module is not intended to be called."
        )


def update_batch_size(batch_size: int, t: torch.Tensor):
    if t is None:
        return batch_size  # unused tensor
    torch._assert(t.dim() == 2, "expect 2-d tensors")
    if t.shape[1] == 0:
        return batch_size  # unused tensor
    if t.shape[0] == 1:
        return batch_size  # shared tensor
    if batch_size == 1:
        return t.shape[0]  # first batched tensor
    torch._assert(batch_size == t.shape[0], "mismatch in batch size")
    return batch_size  # subsequent batched tensor


def get_batch_size(in0: torch.Tensor, in1: torch.Tensor, in2: torch.Tensor):
    result = 1
    result = update_batch_size(result, in0)
    result = update_batch_size(result, in1)
    result = update_batch_size(result, in2)
    return result


def tensor_product_info_as_ctype(
    path_csr_offsets: torch.Tensor,
    path_offsets: torch.Tensor,
    path_cg_values: torch.Tensor,
):
    float_type = torch.float32 if path_cg_values.dtype == torch.int32 else torch.float64
    return ops.make_tensor_product_info(
        path_csr_offsets,
        path_offsets,
        path_cg_values.view(dtype=float_type),
    )


@torch.library.custom_op(
    "cuequivariance::fused_tensor_product",
    mutates_args=(),
    device_types="cuda",
)
def _(
    in0: torch.Tensor,
    in1: torch.Tensor,
    in2: Optional[torch.Tensor],
    tp_path_csr_offsets_fwd: torch.Tensor,
    tp_path_csr_offsets_dgrad_in0: torch.Tensor,
    tp_path_csr_offsets_dgrad_in1: torch.Tensor,
    tp_path_csr_offsets_dgrad_in2: torch.Tensor,
    tp_path_offsets_fwd: torch.Tensor,
    tp_path_offsets_dgrad_in0: torch.Tensor,
    tp_path_offsets_dgrad_in1: torch.Tensor,
    tp_path_offsets_dgrad_in2: torch.Tensor,
    tp_path_cg_values_fwd: torch.Tensor,
    tp_path_cg_values_dgrad_in0: torch.Tensor,
    tp_path_cg_values_dgrad_in1: torch.Tensor,
    tp_path_cg_values_dgrad_in2: torch.Tensor,
    connection_mode: int,
    output_stride: int,
) -> torch.Tensor:
    batch_size = get_batch_size(in0, in1, in2)
    out = torch.empty((batch_size, output_stride), device=in0.device, dtype=in0.dtype)
    stream = torch.cuda.current_stream().cuda_stream

    fwd_fun = get_operator_from_module(
        ops,
        "fused_tensor_product_fwd",
        (
            in0.dtype,
            in1.dtype,
            in2.dtype if mode_is_op4(connection_mode) else out.dtype,
            out.dtype,
            torch.float32
            if tp_path_cg_values_fwd.dtype == torch.int32
            else torch.float64,
        ),
    )

    tp_info_fwd = tensor_product_info_as_ctype(
        tp_path_csr_offsets_fwd,
        tp_path_offsets_fwd,
        tp_path_cg_values_fwd,
    )

    fwd_fun(
        out,
        maybe_detach(in0),
        maybe_detach(in1),
        maybe_detach(in2),
        getattr(ops.ConnectionMode, int_mappings_to_mode[connection_mode]),
        tp_info_fwd,
        stream_id=stream,
    )

    return out


@torch.library.custom_op(
    "cuequivariance::fused_tensor_product_bwd",
    mutates_args=(),
    device_types="cuda",
)
def _(
    grad_out: torch.Tensor,
    in0: torch.Tensor,
    in1: torch.Tensor,
    in2: Optional[torch.Tensor],
    tp_path_csr_offsets_fwd: torch.Tensor,
    tp_path_csr_offsets_dgrad_in0: torch.Tensor,
    tp_path_csr_offsets_dgrad_in1: torch.Tensor,
    tp_path_csr_offsets_dgrad_in2: torch.Tensor,
    tp_path_offsets_fwd: torch.Tensor,
    tp_path_offsets_dgrad_in0: torch.Tensor,
    tp_path_offsets_dgrad_in1: torch.Tensor,
    tp_path_offsets_dgrad_in2: torch.Tensor,
    tp_path_cg_values_fwd: torch.Tensor,
    tp_path_cg_values_dgrad_in0: torch.Tensor,
    tp_path_cg_values_dgrad_in1: torch.Tensor,
    tp_path_cg_values_dgrad_in2: torch.Tensor,
    connection_mode: int,
    needs_grad_in0: bool,
    needs_grad_in1: bool,
    needs_grad_in2: bool,
) -> List[torch.Tensor]:
    # calling function takes care of ensuring contiguous and detach
    grad_in0 = maybe_empty_like(in0, needs_grad_in0)
    grad_in1 = maybe_empty_like(in1, needs_grad_in1)
    grad_in2 = maybe_empty_like(in2, needs_grad_in2)

    in0 = maybe_detach(in0)
    in1 = maybe_detach(in1)
    in2 = maybe_detach(in2)
    grad_out = maybe_detach(grad_out)

    stream = torch.cuda.current_stream().cuda_stream
    bwd_fun = get_operator_from_module(
        ops,
        "fused_tensor_product_bwd",
        (
            in0.dtype,
            in1.dtype,
            in2.dtype if mode_is_op4(connection_mode) else grad_out.dtype,
            grad_out.dtype,
            torch.float32
            if tp_path_cg_values_dgrad_in0.dtype == torch.int32
            else torch.float64,
        ),
    )

    tp_info_dgrad_in0 = tensor_product_info_as_ctype(
        tp_path_csr_offsets_dgrad_in0,
        tp_path_offsets_dgrad_in0,
        tp_path_cg_values_dgrad_in0,
    )
    tp_info_dgrad_in1 = tensor_product_info_as_ctype(
        tp_path_csr_offsets_dgrad_in1,
        tp_path_offsets_dgrad_in1,
        tp_path_cg_values_dgrad_in1,
    )
    tp_info_dgrad_in2 = tensor_product_info_as_ctype(
        tp_path_csr_offsets_dgrad_in2,
        tp_path_offsets_dgrad_in2,
        tp_path_cg_values_dgrad_in2,
    )

    bwd_fun(
        grad_in0,
        grad_in1,
        grad_in2,
        grad_out,
        maybe_detach(in0),
        maybe_detach(in1),
        maybe_detach(in2),
        getattr(ops.ConnectionMode, int_mappings_to_mode[connection_mode]),
        tp_info_dgrad_in0,
        tp_info_dgrad_in1,
        tp_info_dgrad_in2,
        stream_id=stream,
    )

    grads = []
    if grad_in0 is not None:
        grads.append(grad_in0)
    if grad_in1 is not None:
        grads.append(grad_in1)
    if grad_in2 is not None:
        grads.append(grad_in2)

    return grads


@torch.library.custom_op(
    "cuequivariance::fused_tensor_product_bwd_bwd",
    mutates_args=(),
    device_types="cuda",
)
def _(
    grad_grad_in0: Optional[torch.Tensor],
    grad_grad_in1: Optional[torch.Tensor],
    grad_grad_in2: Optional[torch.Tensor],
    grad_out: torch.Tensor,
    in0: torch.Tensor,
    in1: torch.Tensor,
    in2: Optional[torch.Tensor],
    tp_path_csr_offsets_fwd: torch.Tensor,
    tp_path_csr_offsets_dgrad_in0: torch.Tensor,
    tp_path_csr_offsets_dgrad_in1: torch.Tensor,
    tp_path_csr_offsets_dgrad_in2: torch.Tensor,
    tp_path_offsets_fwd: torch.Tensor,
    tp_path_offsets_dgrad_in0: torch.Tensor,
    tp_path_offsets_dgrad_in1: torch.Tensor,
    tp_path_offsets_dgrad_in2: torch.Tensor,
    tp_path_cg_values_fwd: torch.Tensor,
    tp_path_cg_values_dgrad_in0: torch.Tensor,
    tp_path_cg_values_dgrad_in1: torch.Tensor,
    tp_path_cg_values_dgrad_in2: torch.Tensor,
    connection_mode: int,
    needs_grad_in0: bool,
    needs_grad_in1: bool,
    needs_grad_in2: bool,
) -> List[torch.Tensor]:
    # grad_grad_out can't be None due to PyTorch limitations, so always allocate
    grad_grad_out = torch.empty_like(grad_out)
    grad_in0 = maybe_empty_like(in0, needs_grad_in0)
    grad_in1 = maybe_empty_like(in1, needs_grad_in1)
    grad_in2 = maybe_empty_like(in2, needs_grad_in2)

    stream = torch.cuda.current_stream().cuda_stream

    bwd_bwd_fun = get_operator_from_module(
        ops,
        "fused_tensor_product_bwd_bwd",
        (
            in0.dtype,
            in1.dtype,
            in2.dtype if mode_is_op4(connection_mode) else grad_out.dtype,
            grad_out.dtype,
            torch.float32
            if tp_path_cg_values_fwd.dtype == torch.int32
            else torch.float64,
        ),
    )

    tp_info_fwd = tensor_product_info_as_ctype(
        tp_path_csr_offsets_fwd,
        tp_path_offsets_fwd,
        tp_path_cg_values_fwd,
    )
    tp_info_dgrad_in0 = tensor_product_info_as_ctype(
        tp_path_csr_offsets_dgrad_in0,
        tp_path_offsets_dgrad_in0,
        tp_path_cg_values_dgrad_in0,
    )
    tp_info_dgrad_in1 = tensor_product_info_as_ctype(
        tp_path_csr_offsets_dgrad_in1,
        tp_path_offsets_dgrad_in1,
        tp_path_cg_values_dgrad_in1,
    )
    tp_info_dgrad_in2 = tensor_product_info_as_ctype(
        tp_path_csr_offsets_dgrad_in2,
        tp_path_offsets_dgrad_in2,
        tp_path_cg_values_dgrad_in2,
    )

    bwd_bwd_fun(
        grad_in0,
        grad_in1,
        grad_in2,
        grad_grad_out,
        maybe_detach(grad_grad_in0),
        maybe_detach(grad_grad_in1),
        maybe_detach(grad_grad_in2),
        maybe_detach(grad_out),
        maybe_detach(in0),
        maybe_detach(in1),
        maybe_detach(in2),
        getattr(ops.ConnectionMode, int_mappings_to_mode[connection_mode]),
        tp_info_fwd,
        tp_info_dgrad_in0,
        tp_info_dgrad_in1,
        tp_info_dgrad_in2,
        stream_id=stream,
    )

    grads = [grad_grad_out]
    if needs_grad_in0:
        grads.append(grad_in0)
    if needs_grad_in1:
        grads.append(grad_in1)
    if needs_grad_in2:
        grads.append(grad_in2)

    return grads


@torch.library.register_fake("cuequivariance::fused_tensor_product")
def _(
    in0: torch.Tensor,
    in1: torch.Tensor,
    in2: Optional[torch.Tensor],
    tp_path_csr_offsets_fwd: torch.Tensor,
    tp_path_csr_offsets_dgrad_in0: torch.Tensor,
    tp_path_csr_offsets_dgrad_in1: torch.Tensor,
    tp_path_csr_offsets_dgrad_in2: torch.Tensor,
    tp_path_offsets_fwd: torch.Tensor,
    tp_path_offsets_dgrad_in0: torch.Tensor,
    tp_path_offsets_dgrad_in1: torch.Tensor,
    tp_path_offsets_dgrad_in2: torch.Tensor,
    tp_path_cg_values_fwd: torch.Tensor,
    tp_path_cg_values_dgrad_in0: torch.Tensor,
    tp_path_cg_values_dgrad_in1: torch.Tensor,
    tp_path_cg_values_dgrad_in2: torch.Tensor,
    connection_mode: int,
    output_stride: int,
) -> torch.Tensor:
    batch_size = get_batch_size(in0, in1, in2)
    return torch.empty((batch_size, output_stride), device=in0.device, dtype=in0.dtype)


@torch.library.register_fake("cuequivariance::fused_tensor_product_bwd")
def _(
    grad_out: torch.Tensor,
    in0: torch.Tensor,
    in1: torch.Tensor,
    in2: Optional[torch.Tensor],
    tp_path_csr_offsets_fwd: torch.Tensor,
    tp_path_csr_offsets_dgrad_in0: torch.Tensor,
    tp_path_csr_offsets_dgrad_in1: torch.Tensor,
    tp_path_csr_offsets_dgrad_in2: torch.Tensor,
    tp_path_offsets_fwd: torch.Tensor,
    tp_path_offsets_dgrad_in0: torch.Tensor,
    tp_path_offsets_dgrad_in1: torch.Tensor,
    tp_path_offsets_dgrad_in2: torch.Tensor,
    tp_path_cg_values_fwd: torch.Tensor,
    tp_path_cg_values_dgrad_in0: torch.Tensor,
    tp_path_cg_values_dgrad_in1: torch.Tensor,
    tp_path_cg_values_dgrad_in2: torch.Tensor,
    connection_mode: int,
    needs_grad_in0: bool,
    needs_grad_in1: bool,
    needs_grad_in2: bool,
) -> List[torch.Tensor]:
    grad_in0 = maybe_empty_like(in0, needs_grad_in0)
    grad_in1 = maybe_empty_like(in1, needs_grad_in1)
    grad_in2 = maybe_empty_like(in2, needs_grad_in2)

    grads = []
    if grad_in0 is not None:
        grads.append(grad_in0)
    if grad_in1 is not None:
        grads.append(grad_in1)
    if grad_in2 is not None:
        grads.append(grad_in2)

    return grads


@torch.library.register_fake("cuequivariance::fused_tensor_product_bwd_bwd")
def _(
    grad_grad_in0: Optional[torch.Tensor],
    grad_grad_in1: Optional[torch.Tensor],
    grad_grad_in2: Optional[torch.Tensor],
    grad_out: torch.Tensor,
    in0: torch.Tensor,
    in1: torch.Tensor,
    in2: Optional[torch.Tensor],
    tp_path_csr_offsets_fwd: torch.Tensor,
    tp_path_csr_offsets_dgrad_in0: torch.Tensor,
    tp_path_csr_offsets_dgrad_in1: torch.Tensor,
    tp_path_csr_offsets_dgrad_in2: torch.Tensor,
    tp_path_offsets_fwd: torch.Tensor,
    tp_path_offsets_dgrad_in0: torch.Tensor,
    tp_path_offsets_dgrad_in1: torch.Tensor,
    tp_path_offsets_dgrad_in2: torch.Tensor,
    tp_path_cg_values_fwd: torch.Tensor,
    tp_path_cg_values_dgrad_in0: torch.Tensor,
    tp_path_cg_values_dgrad_in1: torch.Tensor,
    tp_path_cg_values_dgrad_in2: torch.Tensor,
    connection_mode: int,
    needs_grad_in0: bool,
    needs_grad_in1: bool,
    needs_grad_in2: bool,
) -> List[torch.Tensor]:
    grad_grad_out = torch.empty_like(grad_out)
    grad_in0 = maybe_empty_like(in0, needs_grad_in0)
    grad_in1 = maybe_empty_like(in1, needs_grad_in1)
    grad_in2 = maybe_empty_like(in2, needs_grad_in2)

    grads = [grad_grad_out]
    if grad_in0 is not None:
        grads.append(grad_in0)
    if grad_in1 is not None:
        grads.append(grad_in1)
    if grad_in2 is not None:
        grads.append(grad_in2)

    return grads


def fused_tensor_product_setup_fwd_context(ctx, inputs, output):
    (
        in0,
        in1,
        in2,
        tp_path_csr_offsets_fwd,
        tp_path_csr_offsets_dgrad_in0,
        tp_path_csr_offsets_dgrad_in1,
        tp_path_csr_offsets_dgrad_in2,
        tp_path_offsets_fwd,
        tp_path_offsets_dgrad_in0,
        tp_path_offsets_dgrad_in1,
        tp_path_offsets_dgrad_in2,
        tp_path_cg_values_fwd,
        tp_path_cg_values_dgrad_in0,
        tp_path_cg_values_dgrad_in1,
        tp_path_cg_values_dgrad_in2,
        connection_mode,
        _,
    ) = inputs
    ctx.save_for_backward(
        in0,
        in1,
        in2,
        tp_path_csr_offsets_fwd,
        tp_path_csr_offsets_dgrad_in0,
        tp_path_csr_offsets_dgrad_in1,
        tp_path_csr_offsets_dgrad_in2,
        tp_path_offsets_fwd,
        tp_path_offsets_dgrad_in0,
        tp_path_offsets_dgrad_in1,
        tp_path_offsets_dgrad_in2,
        tp_path_cg_values_fwd,
        tp_path_cg_values_dgrad_in0,
        tp_path_cg_values_dgrad_in1,
        tp_path_cg_values_dgrad_in2,
    )
    ctx.connection_mode = connection_mode


def fused_tensor_product_setup_bwd_context(ctx, inputs, output):
    (
        grad_out,
        in0,
        in1,
        in2,
        tp_path_csr_offsets_fwd,
        tp_path_csr_offsets_dgrad_in0,
        tp_path_csr_offsets_dgrad_in1,
        tp_path_csr_offsets_dgrad_in2,
        tp_path_offsets_fwd,
        tp_path_offsets_dgrad_in0,
        tp_path_offsets_dgrad_in1,
        tp_path_offsets_dgrad_in2,
        tp_path_cg_values_fwd,
        tp_path_cg_values_dgrad_in0,
        tp_path_cg_values_dgrad_in1,
        tp_path_cg_values_dgrad_in2,
        connection_mode,
        _,
        _,
        _,
    ) = inputs
    ctx.save_for_backward(
        grad_out,
        in0,
        in1,
        in2,
        tp_path_csr_offsets_fwd,
        tp_path_csr_offsets_dgrad_in0,
        tp_path_csr_offsets_dgrad_in1,
        tp_path_csr_offsets_dgrad_in2,
        tp_path_offsets_fwd,
        tp_path_offsets_dgrad_in0,
        tp_path_offsets_dgrad_in1,
        tp_path_offsets_dgrad_in2,
        tp_path_cg_values_fwd,
        tp_path_cg_values_dgrad_in0,
        tp_path_cg_values_dgrad_in1,
        tp_path_cg_values_dgrad_in2,
    )
    ctx.connection_mode = connection_mode


@torch.compiler.allow_in_graph
def fused_tensor_product_bwd_bwd(ctx, grad_grads):
    needs_grad_in0 = ctx.needs_input_grad[1]
    needs_grad_in1 = ctx.needs_input_grad[2]
    needs_grad_in2 = ctx.needs_input_grad[3] and mode_is_op4(ctx.connection_mode)

    grad_idx = 0
    grad_grad_in0, grad_grad_in1, grad_grad_in2 = None, None, None
    if needs_grad_in0:
        grad_grad_in0 = grad_grads[grad_idx]
        grad_idx += 1
    if needs_grad_in1:
        grad_grad_in1 = grad_grads[grad_idx]
        grad_idx += 1
    if needs_grad_in2:
        grad_grad_in2 = grad_grads[grad_idx]

    (
        grad_out,
        in0,
        in1,
        in2,
        tp_path_csr_offsets_fwd,
        tp_path_csr_offsets_dgrad_in0,
        tp_path_csr_offsets_dgrad_in1,
        tp_path_csr_offsets_dgrad_in2,
        tp_path_offsets_fwd,
        tp_path_offsets_dgrad_in0,
        tp_path_offsets_dgrad_in1,
        tp_path_offsets_dgrad_in2,
        tp_path_cg_values_fwd,
        tp_path_cg_values_dgrad_in0,
        tp_path_cg_values_dgrad_in1,
        tp_path_cg_values_dgrad_in2,
    ) = ctx.saved_tensors
    grads = torch.ops.cuequivariance.fused_tensor_product_bwd_bwd(
        grad_grad_in0,
        grad_grad_in1,
        grad_grad_in2,
        grad_out,
        in0,
        in1,
        in2,
        tp_path_csr_offsets_fwd,
        tp_path_csr_offsets_dgrad_in0,
        tp_path_csr_offsets_dgrad_in1,
        tp_path_csr_offsets_dgrad_in2,
        tp_path_offsets_fwd,
        tp_path_offsets_dgrad_in0,
        tp_path_offsets_dgrad_in1,
        tp_path_offsets_dgrad_in2,
        tp_path_cg_values_fwd,
        tp_path_cg_values_dgrad_in0,
        tp_path_cg_values_dgrad_in1,
        tp_path_cg_values_dgrad_in2,
        ctx.connection_mode,
        needs_grad_in0,
        needs_grad_in1,
        needs_grad_in2,
    )

    grad_grad_out = grads[0]

    grad_idx = 1
    grad_in0, grad_in1, grad_in2 = None, None, None
    if needs_grad_in0:
        grad_in0 = grads[grad_idx]
        grad_idx += 1
    if needs_grad_in1:
        grad_in1 = grads[grad_idx]
        grad_idx += 1
    if needs_grad_in2:
        grad_in2 = grads[grad_idx]

    return (
        grad_grad_out,
        grad_in0,
        grad_in1,
        grad_in2,
        None,
        None,
        None,
        None,
        None,
        None,
        None,
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


def fused_tensor_product_bwd(ctx, grad_output):
    (
        in0,
        in1,
        in2,
        tp_path_csr_offsets_fwd,
        tp_path_csr_offsets_dgrad_in0,
        tp_path_csr_offsets_dgrad_in1,
        tp_path_csr_offsets_dgrad_in2,
        tp_path_offsets_fwd,
        tp_path_offsets_dgrad_in0,
        tp_path_offsets_dgrad_in1,
        tp_path_offsets_dgrad_in2,
        tp_path_cg_values_fwd,
        tp_path_cg_values_dgrad_in0,
        tp_path_cg_values_dgrad_in1,
        tp_path_cg_values_dgrad_in2,
    ) = ctx.saved_tensors

    needs_grad_in0 = ctx.needs_input_grad[0]
    needs_grad_in1 = ctx.needs_input_grad[1]
    needs_grad_in2 = ctx.needs_input_grad[2] and mode_is_op4(ctx.connection_mode)

    grads = torch.ops.cuequivariance.fused_tensor_product_bwd(
        grad_output,
        in0,
        in1,
        in2,
        tp_path_csr_offsets_fwd,
        tp_path_csr_offsets_dgrad_in0,
        tp_path_csr_offsets_dgrad_in1,
        tp_path_csr_offsets_dgrad_in2,
        tp_path_offsets_fwd,
        tp_path_offsets_dgrad_in0,
        tp_path_offsets_dgrad_in1,
        tp_path_offsets_dgrad_in2,
        tp_path_cg_values_fwd,
        tp_path_cg_values_dgrad_in0,
        tp_path_cg_values_dgrad_in1,
        tp_path_cg_values_dgrad_in2,
        ctx.connection_mode,
        needs_grad_in0,
        needs_grad_in1,
        needs_grad_in2,
    )

    grad_idx = 0
    grad_in0, grad_in1, grad_in2 = None, None, None

    # for g in grads:
    #        g.detach_()

    if needs_grad_in0:
        grad_in0 = grads[grad_idx]
        grad_idx += 1
    if needs_grad_in1:
        grad_in1 = grads[grad_idx]
        grad_idx += 1
    if needs_grad_in2:
        grad_in2 = grads[grad_idx]
        grad_idx += 1

    return (
        grad_in0,
        grad_in1,
        grad_in2,
        None,
        None,
        None,
        None,
        None,
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
    "cuequivariance::fused_tensor_product",
    fused_tensor_product_bwd,
    setup_context=fused_tensor_product_setup_fwd_context,
)

torch.library.register_autograd(
    "cuequivariance::fused_tensor_product_bwd",
    fused_tensor_product_bwd_bwd,
    setup_context=fused_tensor_product_setup_bwd_context,
)


def fused_tensor_product(
    in0: torch.Tensor,
    in1: torch.Tensor,
    in2: Optional[torch.Tensor],
    tp_path_csr_offsets_fwd: torch.Tensor,
    tp_path_csr_offsets_dgrad_in0: torch.Tensor,
    tp_path_csr_offsets_dgrad_in1: torch.Tensor,
    tp_path_csr_offsets_dgrad_in2: torch.Tensor,
    tp_path_offsets_fwd: torch.Tensor,
    tp_path_offsets_dgrad_in0: torch.Tensor,
    tp_path_offsets_dgrad_in1: torch.Tensor,
    tp_path_offsets_dgrad_in2: torch.Tensor,
    tp_path_cg_values_fwd: torch.Tensor,
    tp_path_cg_values_dgrad_in0: torch.Tensor,
    tp_path_cg_values_dgrad_in1: torch.Tensor,
    tp_path_cg_values_dgrad_in2: torch.Tensor,
    connection_mode: int,
    output_stride: int,
) -> torch.Tensor:
    return torch.ops.cuequivariance.fused_tensor_product(
        in0,
        in1,
        in2,
        tp_path_csr_offsets_fwd,
        tp_path_csr_offsets_dgrad_in0,
        tp_path_csr_offsets_dgrad_in1,
        tp_path_csr_offsets_dgrad_in2,
        tp_path_offsets_fwd,
        tp_path_offsets_dgrad_in0,
        tp_path_offsets_dgrad_in1,
        tp_path_offsets_dgrad_in2,
        tp_path_cg_values_fwd,
        tp_path_cg_values_dgrad_in0,
        tp_path_cg_values_dgrad_in1,
        tp_path_cg_values_dgrad_in2,
        connection_mode,
        output_stride,
    )


class FusedTensorProductOp4(nn.Module):
    r"""Generic implementation of a Fused Segmented Tensor Product
    contracting three inputs and producing a single output (four operands).

    Parameters
    ----------
    operand_segment_modes : list[str]
        description of the segment mode of each operand (of length 4)
    operand_segment_offsets : list[list[int]]
        list of segment offsets of each operand (outer length equal to 4)
    operand_segment_shapes : list[list[list[int]]]
        list of segment shapes of each operand represented as a list of dimensions
        (outer length equal to 4)
    path_indices : list[list[int]]
        list of segment indices for each operand and for each path
        (outer length equal to number of contraction paths)
    path_coefficients : list[float]
        list of coefficients weighing each path
    math_dtype : torch.dtype, optional
        The data type of path coefficients and internal computations, by default torch.float32

    Example
    ---------------------------
    >>> modes = ["u", "u", "uw", "w"]
    >>> offsets = [
    ...     [0, 16],
    ...     [0, 16],
    ...     [0, 128],
    ...     [0, 8],
    ... ]
    >>> shapes = [
    ...     [[16], [16]],
    ...     [[16], [16]],
    ...     [[16, 8], [16, 8]],
    ...     [[8], [8]],
    ... ]
    >>> path_indices = [
    ...     [0, 0, 0, 0],
    ...     [0, 1, 0, 0],
    ...     [1, 0, 1, 1],
    ...     [1, 1, 1, 1],
    ... ]
    >>> path_coefficients = [
    ...     0.5, 0.25, 0.75, -0.25,
    ... ]
    >>> tp = FusedTensorProductOp4(
    ...     modes,
    ...     offsets,
    ...     shapes,
    ...     path_indices,
    ...     path_coefficients,
    ...     torch.float32,
    ... ).to(device="cuda")
    >>> in0 = torch.randn((1024, 32), device="cuda")
    >>> in1 = torch.randn((1024, 32), device="cuda)
    >>> in2 = torch.randn((1024, 256), device="cuda)
    >>> out = tp(in0, in1, in2)
    >>> out.shape
    torch.Size(1024, 16)

    """

    def __init__(
        self,
        operand_segment_modes: list[str],
        operand_segment_offsets: list[list[int]],
        operand_segment_shapes: list[list[list[int]]],
        path_indices: list[list[int]],
        path_coefficients: list[float],
        math_dtype: torch.dtype = torch.float32,
    ):
        super().__init__()

        mode = "_".join(operand_segment_modes)

        # for know, we can always extract
        # u,v,w from individual operands
        dims_dict = {
            "u__u_u": (0, 1, -1),
            "u__uw_w": (0, 1, 3),
            "u__uv_v": (0, 1, 3),
            "_v_vw_w": (0, 1, 3),
            "u_v_uv_u": (0, 1, -1),
            "u_v_uv_v": (0, 1, -1),
            "u_u_uw_w": (0, -1, 3),
            "u_v_uvw_w": (0, 1, 3),
        }

        assert mode in op4_mode_mappings, (
            f"{mode} not found, expected {list(op4_mode_mappings.keys())}"
        )

        u_op_idx, v_op_idx, w_op_idx = dims_dict[mode]

        if (
            len(operand_segment_modes) != 4
            or len(operand_segment_offsets) != 4
            or len(operand_segment_shapes) != 4
        ):
            raise ValueError("Expected 4 operands (3 inputs, 1 output)")

        if len(path_indices) != len(path_coefficients):
            msg = (
                "path_coefficients and path_indices both have to be of length num_paths"
            )
            msg += f", got {len(path_coefficients)} & {len(path_indices)} respectively."

            raise ValueError(msg)

        operand_segment_strides = [
            [math.prod(segment) for segment in op] for op in operand_segment_shapes
        ]

        strides = [sum(op) for op in operand_segment_strides]

        path_offsets_and_dims = []
        self.connection_mode = mode_mappings_to_int[op4_mode_mappings[mode]]

        for indices in path_indices:
            u = (
                operand_segment_strides[u_op_idx][indices[u_op_idx]]
                if u_op_idx != -1
                else -1
            )
            v = (
                operand_segment_strides[v_op_idx][indices[v_op_idx]]
                if v_op_idx != -1
                else -1
            )
            w = (
                operand_segment_strides[w_op_idx][indices[w_op_idx]]
                if w_op_idx != -1
                else -1
            )

            path_offsets_and_dims.append(
                (
                    operand_segment_offsets[0][indices[0]],
                    operand_segment_offsets[1][indices[1]],
                    operand_segment_offsets[2][indices[2]],
                    operand_segment_offsets[3][indices[3]],
                    u,
                    v,
                    w,
                    -1,
                )
            )

        tp_infos = make_tensor_product_infos(
            strides, path_offsets_and_dims, path_coefficients, math_dtype
        )

        self.stride_out = strides[-1]
        self._tensor_product_info_fwd = TensorProductPathData(*tp_infos[0], math_dtype)
        self._tensor_product_info_bwd_dgrad_in0 = TensorProductPathData(
            *tp_infos[1], math_dtype
        )
        self._tensor_product_info_bwd_dgrad_in1 = TensorProductPathData(
            *tp_infos[2], math_dtype
        )
        self._tensor_product_info_bwd_dgrad_in2 = TensorProductPathData(
            *tp_infos[3], math_dtype
        )

    def forward(
        self,
        in0: torch.Tensor,
        in1: torch.Tensor,
        in2: torch.Tensor,
    ) -> torch.Tensor:
        out = fused_tensor_product(
            in0,
            in1,
            in2,
            self._tensor_product_info_fwd.path_csr_offsets,
            self._tensor_product_info_bwd_dgrad_in0.path_csr_offsets,
            self._tensor_product_info_bwd_dgrad_in1.path_csr_offsets,
            self._tensor_product_info_bwd_dgrad_in2.path_csr_offsets,
            self._tensor_product_info_fwd.path_offsets,
            self._tensor_product_info_bwd_dgrad_in0.path_offsets,
            self._tensor_product_info_bwd_dgrad_in1.path_offsets,
            self._tensor_product_info_bwd_dgrad_in2.path_offsets,
            self._tensor_product_info_fwd.path_cg_values,
            self._tensor_product_info_bwd_dgrad_in0.path_cg_values,
            self._tensor_product_info_bwd_dgrad_in1.path_cg_values,
            self._tensor_product_info_bwd_dgrad_in2.path_cg_values,
            self.connection_mode,
            self.stride_out,
        )

        return out

    def _opcheck(self, in0: torch.Tensor, in1: torch.Tensor, in2: torch.Tensor):
        torch.library.opcheck(
            torch.ops.cuequivariance.fused_tensor_product,
            (
                in0,
                in1,
                in2,
                self._tensor_product_info_fwd.path_csr_offsets,
                self._tensor_product_info_bwd_dgrad_in0.path_csr_offsets,
                self._tensor_product_info_bwd_dgrad_in1.path_csr_offsets,
                self._tensor_product_info_bwd_dgrad_in2.path_csr_offsets,
                self._tensor_product_info_fwd.path_offsets,
                self._tensor_product_info_bwd_dgrad_in0.path_offsets,
                self._tensor_product_info_bwd_dgrad_in1.path_offsets,
                self._tensor_product_info_bwd_dgrad_in2.path_offsets,
                self._tensor_product_info_fwd.path_cg_values,
                self._tensor_product_info_bwd_dgrad_in0.path_cg_values,
                self._tensor_product_info_bwd_dgrad_in1.path_cg_values,
                self._tensor_product_info_bwd_dgrad_in2.path_cg_values,
                self.connection_mode,
                self.stride_out,
            ),
        )


class FusedTensorProductOp3(nn.Module):
    r"""Generic implementation of a Fused Segmented Tensor Product
    contracting two inputs and producing a single output (three operands).

    Parameters
    ----------
    operand_segment_modes : list[str]
        description of the segment mode of each operand (of length 3)
    operand_segment_offsets : list[list[int]]
        list of segment offsets of each operand (outer length equal to 3)
    operand_segment_shapes : list[list[list[int]]]
        list of segment shapes of each operand represented as a list of dimensions
        (outer length equal to 3)
    path_indices : list[list[int]]
        list of segment indices for each operand and for each path
        (outer length equal to number of contraction paths)
    path_coefficients : list[float]
        list of coefficients weighing each path
    math_dtype : torch.dtype, optional
        The data type of path coefficients and internal computations, by default torch.float32

    Example
    ---------------------------
    >>> modes = ["u", "uv", "v"]
    >>> offsets = [
    ...     [0, 16],
    ...     [0, 128],
    ...     [0, 8],
    ... ]
    >>> shapes = [
    ...     [[16], [16]],
    ...     [[16, 8], [16, 8]],
    ...     [[8], [8]],
    ... ]
    >>> path_indices = [
    ...     [0, 0, 0],
    ...     [0, 1, 0],
    ...     [1, 0, 1],
    ...     [1, 1, 1],
    ... ]
    >>> path_coefficients = [
    ...     0.5, 0.25, 0.75, -0.25,
    ... ]
    >>> tp = FusedTensorProductOp3(
    ...     modes,
    ...     offsets,
    ...     shapes,
    ...     path_indices,
    ...     path_coefficients,
    ...     torch.float32,
    ... ).to(device="cuda")
    >>> in0 = torch.randn((1024, 32), device="cuda")
    >>> in1 = torch.randn((1024, 256), device="cuda)
    >>> out = tp(in0, in1)
    >>> out.shape
    torch.Size(1024, 16)

    """

    def __init__(
        self,
        operand_segment_modes: list[str],
        operand_segment_offsets: list[list[int]],
        operand_segment_shapes: list[list[list[int]]],
        path_indices: list[list[int]],
        path_coefficients: list[float],
        math_dtype: torch.dtype = torch.float32,
    ):
        super().__init__()

        mode = "_".join(operand_segment_modes)

        # for know, we can always extract
        # u,v,w from individual operands
        dims_dict = {
            "u_u_u": (0, -1),
            "u_v_uv": (0, 1),
            "u_uv_v": (0, 2),
            "u__u": (0, 1),
            "_v_v": (0, 1),
        }

        assert mode in op3_mode_mappings

        u_op_idx, v_op_idx = dims_dict[mode]

        if (
            len(operand_segment_modes) != 3
            or len(operand_segment_offsets) != 3
            or len(operand_segment_shapes) != 3
        ):
            raise ValueError("Expected 3 operands (3 inputs, 1 output)")

        if len(path_indices) != len(path_coefficients):
            msg = ""
            msg += (
                "path_coefficients and path_indices both have to be of length num_paths"
            )
            msg += f", got {len(path_coefficients)} & {len(path_indices)} respectively."
            raise ValueError(msg)

        operand_segment_strides = [
            [math.prod(segment) for segment in op] for op in operand_segment_shapes
        ]
        strides = [sum(op) for op in operand_segment_strides]

        path_offsets_and_dims = []
        self.connection_mode = mode_mappings_to_int[op3_mode_mappings[mode]]

        for indices in path_indices:
            u = (
                operand_segment_strides[u_op_idx][indices[u_op_idx]]
                if u_op_idx != -1
                else -1
            )
            v = (
                operand_segment_strides[v_op_idx][indices[v_op_idx]]
                if v_op_idx != -1
                else -1
            )
            path_offsets_and_dims.append(
                (
                    operand_segment_offsets[0][indices[0]],
                    operand_segment_offsets[1][indices[1]],
                    -1,
                    operand_segment_offsets[2][indices[2]],
                    u,
                    v,
                    -1,
                    -1,
                )
            )

        tp_infos = make_tensor_product_infos(
            strides, path_offsets_and_dims, path_coefficients, math_dtype
        )

        self.stride_out = strides[-1]
        self._tensor_product_info_fwd = TensorProductPathData(*tp_infos[0], math_dtype)
        self._tensor_product_info_bwd_dgrad_in0 = TensorProductPathData(
            *tp_infos[1], math_dtype
        )
        self._tensor_product_info_bwd_dgrad_in1 = TensorProductPathData(
            *tp_infos[2], math_dtype
        )

    def forward(
        self,
        in0: torch.Tensor,
        in1: torch.Tensor,
    ) -> torch.Tensor:
        dummy = torch.empty(
            (
                0,
                0,
            ),
            dtype=in0.dtype,
            device=in0.device,
        )
        out = fused_tensor_product(
            in0,
            in1,
            dummy,  # # not using None for ONNX/TRT exportability
            self._tensor_product_info_fwd.path_csr_offsets,
            self._tensor_product_info_bwd_dgrad_in0.path_csr_offsets,
            self._tensor_product_info_bwd_dgrad_in1.path_csr_offsets,
            self._tensor_product_info_bwd_dgrad_in1.path_csr_offsets,
            self._tensor_product_info_fwd.path_offsets,
            self._tensor_product_info_bwd_dgrad_in0.path_offsets,
            self._tensor_product_info_bwd_dgrad_in1.path_offsets,
            self._tensor_product_info_bwd_dgrad_in1.path_offsets,
            self._tensor_product_info_fwd.path_cg_values,
            self._tensor_product_info_bwd_dgrad_in0.path_cg_values,
            self._tensor_product_info_bwd_dgrad_in1.path_cg_values,
            self._tensor_product_info_bwd_dgrad_in1.path_cg_values,
            self.connection_mode,
            self.stride_out,
        )

        return out

    def _opcheck(self, in0: torch.Tensor, in1: torch.Tensor):
        dummy = torch.empty(
            (
                0,
                0,
            ),
            dtype=in0.dtype,
            device=in0.device,
        )
        torch.library.opcheck(
            torch.ops.cuequivariance.fused_tensor_product,
            (
                in0,
                in1,
                dummy,
                self._tensor_product_info_fwd.path_csr_offsets,
                self._tensor_product_info_bwd_dgrad_in0.path_csr_offsets,
                self._tensor_product_info_bwd_dgrad_in1.path_csr_offsets,
                self._tensor_product_info_bwd_dgrad_in1.path_csr_offsets,
                self._tensor_product_info_fwd.path_offsets,
                self._tensor_product_info_bwd_dgrad_in0.path_offsets,
                self._tensor_product_info_bwd_dgrad_in1.path_offsets,
                self._tensor_product_info_bwd_dgrad_in1.path_offsets,
                self._tensor_product_info_fwd.path_cg_values,
                self._tensor_product_info_bwd_dgrad_in0.path_cg_values,
                self._tensor_product_info_bwd_dgrad_in1.path_cg_values,
                self._tensor_product_info_bwd_dgrad_in1.path_cg_values,
                self.connection_mode,
                self.stride_out,
            ),
        )


__all__ = ["FusedTensorProductOp3", "FusedTensorProductOp4"]
