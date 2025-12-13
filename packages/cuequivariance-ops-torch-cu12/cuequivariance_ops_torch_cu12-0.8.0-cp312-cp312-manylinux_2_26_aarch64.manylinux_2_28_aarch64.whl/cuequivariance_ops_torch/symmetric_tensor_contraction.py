# SPDX-FileCopyrightText: Copyright (c) 2024 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: LicenseRef-NvidiaProprietary
#
# NVIDIA CORPORATION, its affiliates and licensors retain all intellectual
# property and proprietary rights in and to this material, related
# documentation and any modifications thereto. Any use, reproduction,
# disclosure or distribution of this material and related documentation
# without an express license agreement from NVIDIA CORPORATION or
# its affiliates is strictly prohibited.

import warnings
from collections import defaultdict

import torch
import torch.nn as nn

from cuequivariance_ops_torch.tensor_product_uniform_1d_jit import (
    BATCH_DIM_AUTO,
    BATCH_DIM_BATCHED,
    BATCH_DIM_INDEXED,
)


class SymmetricTensorContractionJit(nn.Module):
    def __init__(
        self,
        path_segment_indices: list[list[int]],
        path_coefficients: list[float],
        num_in_segments: int,
        num_couplings: int,
        num_out_segments: int,
        correlation: int,
        math_dtype: torch.dtype,
    ):
        """
        Construct all the necessary attributes

        Parameters
        ---------------------------
        path_segment_indices: list[list[int]]
            list of integer lists to represent each path
        path_coefficients: list[float]
            list of scaling factors for each path
        num_in_segments: int
            number of segments in the first input tensor,
            the repeated operand with the maximum repetition, correlation
        num_couplings: int
            number of segments in the second input tensor,
            the weight tensor
        num_out_segments: int
            number of segments in the output tensor
        correlation: int
            correlation length for the symmetric tensor contraction
        math_dtype: torch.dtype
            data type for computation

        Example
        ---------------------------
        # path_segment_indices[i][-1] < num_out_segments
        # path_segment_indices[i][-2] < num_couplings
        # path_segment_indices[i][0:-2] < num_in_segments
        path_segment_indices = [[0, 1, 1], [0, 1, 1, 2], [1, 1, 16, 8]]
        path_coefficients = [0.1, 0.2, -0.1]
        batch_size = 100
        num_in_segments = 9
        num_couplings = 17
        num_out_segments = 9
        num_embeddings = 3
        correlation = 2
        math_dtype = torch.float32
        sym_tc = SymmetricTensorContraction(path_segment_indices, path_coefficients, \
        num_in_segments, num_couplings, num_out_segments, correlation, math_dtype)

        sym_tc.to('cuda')

        # Number of repetition for segments of tensors.
        # tensor_a, tensor_w and tensor_out must have the same num_features.
        num_features = 128

        dtype = torch.float32

        tensor_a = torch.randn(
        (batch_size, num_in_segments, num_features),
        dtype=dtype,
        requires_grad=True,
        device='cuda',
        )
        tensor_w = torch.randn(
        (num_embeddings, num_couplings, num_features),
        dtype=dtype,
        requires_grad=True,
        device='cuda',
        )
        y = (
        torch.nn.functional.one_hot(
            torch.arange(0, batch_size) % num_embeddings, num_classes=num_embeddings
        )
        )
        tensor_w_id = (
        torch.nonzero(y)[:, 1]
        .contiguous()
        .to(dtype=torch.int32, device='cuda')
        .requires_grad_(False)
        )

        tensor_out = sym_tc.forward(tensor_a, tensor_w, tensor_w_id)
        """
        super().__init__()

        warnings.warn(
            "SymmetricTensorContraction is deprecated and will be removed in a future version.\n"
            "Please use SegmentedPolynomial from the frontend with the appropriate method."
        )

        if not torch.cuda.is_available():
            raise AssertionError("No Nvidia GPU is detected")

        if len(path_segment_indices) != len(path_coefficients):
            raise AssertionError(
                "Number of the path coefficients and of the path segment indices \
                 are different."
            )

        self.math_dtype = math_dtype
        self.operand_num_segments = [num_in_segments, num_couplings, num_out_segments]

        self.batch_dim_auto = BATCH_DIM_AUTO
        self.batch_dim_batched = BATCH_DIM_BATCHED
        self.batch_dim_indexed = BATCH_DIM_INDEXED

        path_coefficients_by_path_length = defaultdict(list)
        path_indices_by_path_length = defaultdict(list)

        for coeff, indices in zip(path_coefficients, path_segment_indices):
            path_coefficients_by_path_length[len(indices)].append(coeff)
            path_indices_by_path_length[len(indices)].append(indices)

        self.num_operations = 0
        self.num_operands = []
        self.operations_flat = []
        self.num_paths = []
        self.path_indices_start = []
        self.path_coefficients_start = []
        self.path_indices_flat = []
        self.path_coefficients_flat = []

        for path_length in sorted(path_coefficients_by_path_length.keys()):
            self.num_operations += 1
            self.num_operands.append(path_length)
            self.operations_flat.extend([0] * (path_length - 2))
            self.operations_flat.extend([1, 2])
            self.path_indices_start.append(len(self.path_indices_flat))
            self.path_coefficients_start.append(len(self.path_coefficients_flat))
            self.path_indices_flat.extend(
                [e for p in path_indices_by_path_length[path_length] for e in p]
            )
            self.num_paths.append(len(path_coefficients_by_path_length[path_length]))
            self.path_coefficients_flat.extend(
                path_coefficients_by_path_length[path_length]
            )

    def forward(self, tensor_a, tensor_w, tensor_w_id):
        """
        Forward funciton call

        Parameters
        ---------------------------
        tensor_a: torch.Tensor
            The input tensor with shape [num_batches, num_in_segments, num_features]
        tensor_w: torch.Tensor
            The input tensor with shape [num_embeddings, num_couplings, num_features]
        tensor_w_id:
            The weight ID with shape [num_batches] with 0-base, i.e. each element has the
            value smaller than num_embeddings

        Return
        ---------------------------
        Torch.tensor with shape [num_batches, num_out_segments, num_features]
        """

        operand_extent = tensor_a.shape[-1]
        tensor_a = tensor_a.reshape(
            tensor_a.shape[0], tensor_a.shape[1] * tensor_a.shape[2]
        )
        tensor_w = tensor_w.reshape(
            tensor_w.shape[0], tensor_w.shape[1] * tensor_w.shape[2]
        )
        result = torch.ops.cuequivariance.tensor_product_uniform_1d_jit(
            "symmetric_kernel_fwd",
            self.math_dtype,
            operand_extent,
            2,
            1,
            1,
            [1, 1, 1],
            self.operand_num_segments,
            [self.batch_dim_batched, self.batch_dim_indexed, self.batch_dim_batched],
            [-1, 0, -1, tensor_w.shape[0]],
            [0, 1, 0],
            self.num_operations,
            self.num_operands,
            self.operations_flat,
            self.num_paths,
            self.path_indices_start,
            self.path_coefficients_start,
            self.path_indices_flat,
            self.path_coefficients_flat,
            self.batch_dim_auto,
            [tensor_a, tensor_w, tensor_w_id],
        )[0]
        return result.reshape(
            result.shape[0], self.operand_num_segments[-1], operand_extent
        )


SymmetricTensorContraction = SymmetricTensorContractionJit

__all__ = ["SymmetricTensorContraction"]
