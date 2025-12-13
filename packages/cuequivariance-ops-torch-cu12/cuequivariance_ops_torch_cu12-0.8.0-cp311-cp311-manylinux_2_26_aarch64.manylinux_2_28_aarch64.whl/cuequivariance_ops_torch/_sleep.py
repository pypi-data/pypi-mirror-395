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


@torch.library.custom_op("cuequivariance::sleep", mutates_args=())
def _(
    seconds: torch.Tensor, input_tensor: torch.Tensor
) -> tuple[torch.Tensor, torch.Tensor]:
    seconds = seconds.detach().contiguous().to(torch.float32)
    input_tensor = input_tensor.detach().contiguous()
    elapsed_ticks = torch.empty((), dtype=torch.int64, device=seconds.device)

    if input_tensor.is_cuda:
        ops.sleep.run_gpu(
            seconds,
            elapsed_ticks,
            input_tensor,
            torch.cuda.current_stream().cuda_stream,
        )
    else:
        ops.sleep.run_cpu(seconds, elapsed_ticks, input_tensor)

    return elapsed_ticks, input_tensor.clone()


@torch.library.register_fake("cuequivariance::sleep")
def _(
    seconds: torch.Tensor, input_tensor: torch.Tensor
) -> tuple[torch.Tensor, torch.Tensor]:
    return torch.empty((), dtype=torch.int64, device=seconds.device), torch.empty_like(
        input_tensor
    )


torch.library.register_autograd(
    "cuequivariance::sleep",
    lambda ctx, grad_elapsed, grad_input: (None, grad_input),
)


def sleep(
    seconds: torch.Tensor, input_tensor: torch.Tensor
) -> tuple[torch.Tensor, torch.Tensor]:
    """Sleep for specified seconds, return (elapsed_ticks, input_tensor)."""
    return torch.ops.cuequivariance.sleep(seconds, input_tensor)


__all__ = ["sleep"]
