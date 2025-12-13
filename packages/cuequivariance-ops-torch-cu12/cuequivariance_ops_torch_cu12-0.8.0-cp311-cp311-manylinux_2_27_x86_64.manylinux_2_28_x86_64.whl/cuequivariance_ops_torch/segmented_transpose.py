# SPDX-FileCopyrightText: Copyright (c) 2024 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: LicenseRef-NvidiaProprietary
#
# NVIDIA CORPORATION, its affiliates and licensors retain all intellectual
# property and proprietary rights in and to this material, related
# documentation and any modifications thereto. Any use, reproduction,
# disclosure or distribution of this material and related documentation
# without an express license agreement from NVIDIA CORPORATION or
# its affiliates is strictly prohibited.

import torch

import cuequivariance_ops_torch._ext as ops


@torch.library.custom_op(
    "cuequivariance::segmented_transpose",
    mutates_args=(),
    device_types="cuda",
)
def _(
    tensor: torch.Tensor, segment_info: torch.Tensor, input_contiguous_as_info: bool
) -> torch.Tensor:
    segment_info = segment_info.detach().contiguous()
    tensor_transpose = torch.empty_like(tensor)
    stream = torch.cuda.current_stream().cuda_stream

    ops.segmented_transpose(
        tensor_transpose,
        tensor.detach().contiguous(),
        segment_info,
        input_contiguous_as_info,
        stream,
    )

    return tensor_transpose


@torch.library.register_fake("cuequivariance::segmented_transpose")
def _(
    tensor: torch.Tensor, segment_info: torch.Tensor, input_contiguous_as_info: bool
) -> torch.Tensor:
    return torch.empty_like(tensor)


def transpose_segment_setup_context(ctx, inputs, output):
    _, segment_info, input_contiguous_as_info = inputs
    ctx.input_contiguous_as_info = input_contiguous_as_info
    ctx.save_for_backward(segment_info)


def segmented_transpose_bwd(ctx, grad_output):
    (segment_info,) = ctx.saved_tensors
    grad_tensor = torch.ops.cuequivariance.segmented_transpose(
        grad_output, segment_info, (not ctx.input_contiguous_as_info)
    )
    return grad_tensor, None, None


torch.library.register_autograd(
    "cuequivariance::segmented_transpose",
    segmented_transpose_bwd,
    setup_context=transpose_segment_setup_context,
)


def segmented_transpose(
    tensor: torch.Tensor,
    segment_info: torch.Tensor,
    input_contiguous_as_info: bool,
) -> torch.Tensor:
    return torch.ops.cuequivariance.segmented_transpose(
        tensor, segment_info, input_contiguous_as_info
    )


__all__ = ["segmented_transpose"]
