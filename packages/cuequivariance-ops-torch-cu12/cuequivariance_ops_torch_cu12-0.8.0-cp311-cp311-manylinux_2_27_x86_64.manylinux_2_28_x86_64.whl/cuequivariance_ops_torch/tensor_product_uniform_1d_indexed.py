# SPDX-FileCopyrightText: Copyright (c) 2024 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: LicenseRef-NvidiaProprietary
#
# NVIDIA CORPORATION, its affiliates and licensors retain all intellectual
# property and proprietary rights in and to this material, related
# documentation and any modifications thereto. Any use, reproduction,
# disclosure or distribution of this material and related documentation
# without an express license agreement from NVIDIA CORPORATION or
# its affiliates is strictly prohibited.


from typing import List, Optional

import torch

from cuequivariance_ops_torch.tensor_product_uniform_1d import TensorProductUniform1dJit


class TensorProductUniform4x1dIndexedJit(TensorProductUniform1dJit):
    def forward(
        self,
        in0: torch.Tensor,
        in1: torch.Tensor,
        in2: torch.Tensor,
        idx_in0: Optional[torch.Tensor],
        idx_in1: Optional[torch.Tensor],
        idx_in2: Optional[torch.Tensor],
        idx_out: Optional[torch.Tensor],
        num_rows_out: int,
    ) -> torch.Tensor:
        num_index_tensor = 0
        ins: List[torch.Tensor] = [in0, in1, in2]
        batch_dim_0 = self.batch_dim_auto
        index_tensor_0 = -1
        index_dims: List[int] = []
        if idx_in0 is not None and idx_in0.numel() > 0:
            ins = ins + [idx_in0]
            batch_dim_0 = self.batch_dim_indexed
            index_tensor_0 = num_index_tensor
            num_index_tensor += 1
            index_dims += [in0.shape[0]]

        batch_dim_1 = self.batch_dim_auto
        index_tensor_1 = -1
        if idx_in1 is not None and idx_in1.numel() > 0:
            ins = ins + [idx_in1]
            batch_dim_1 = self.batch_dim_indexed
            index_tensor_1 = num_index_tensor
            num_index_tensor += 1
            index_dims += [in1.shape[0]]

        batch_dim_2 = self.batch_dim_auto
        index_tensor_2 = -1
        if idx_in2 is not None and idx_in2.numel() > 0:
            ins = ins + [idx_in2]
            batch_dim_2 = self.batch_dim_indexed
            index_tensor_2 = num_index_tensor
            num_index_tensor += 1
            index_dims += [in2.shape[0]]

        batch_dim_out = self.batch_dim_auto
        index_tensor_out = -1
        if idx_out is not None and idx_out.numel() > 0:
            ins = ins + [idx_out]
            batch_dim_out = self.batch_dim_indexed
            index_tensor_out = num_index_tensor
            num_index_tensor += 1
            index_dims += [num_rows_out]

        return torch.ops.cuequivariance.tensor_product_uniform_1d_jit(
            "channelwise_kernel_fwd",
            self.math_dtype,
            self.operand_extent,
            len(self.operand_dim) - 1,
            1,
            num_index_tensor,
            self.operand_dim,
            self.operand_num_segments,
            [batch_dim_0, batch_dim_1, batch_dim_2, batch_dim_out],
            [index_tensor_0, index_tensor_1, index_tensor_2, index_tensor_out]
            + index_dims,
            list(range(len(self.operand_dim) - 1)) + [0],
            1,
            [len(self.operand_dim)],
            list(range(len(self.operand_dim))),
            [len(self.path_coefficients)],
            [0],
            [0],
            self.path_indices_flat,
            self.path_coefficients,
            self.batch_dim_auto,
            ins,
        )[0]


class TensorProductUniform3x1dIndexedJit(TensorProductUniform1dJit):
    def forward(
        self,
        in0: torch.Tensor,
        in1: torch.Tensor,
        idx_in0: Optional[torch.Tensor] = None,
        idx_in1: Optional[torch.Tensor] = None,
        idx_out: Optional[torch.Tensor] = None,
        num_rows_out: int = 1,
    ) -> torch.Tensor:
        num_index_tensor = 0
        ins: List[torch.Tensor] = [in0, in1]
        batch_dim_0 = self.batch_dim_auto
        index_tensor_0 = -1
        index_dims: List[int] = []
        if idx_in0 is not None and idx_in0.numel() > 0:
            ins = ins + [idx_in0]
            batch_dim_0 = self.batch_dim_indexed
            index_tensor_0 = num_index_tensor
            num_index_tensor += 1
            index_dims += [in0.shape[0]]

        batch_dim_1 = self.batch_dim_auto
        index_tensor_1 = -1
        if idx_in1 is not None and idx_in1.numel() > 0:
            ins = ins + [idx_in1]
            batch_dim_1 = self.batch_dim_indexed
            index_tensor_1 = num_index_tensor
            num_index_tensor += 1
            index_dims += [in1.shape[0]]

        batch_dim_out = self.batch_dim_auto
        index_tensor_out = -1
        if idx_out is not None and idx_out.numel() > 0:
            ins = ins + [idx_out]
            batch_dim_out = self.batch_dim_indexed
            index_tensor_out = num_index_tensor
            num_index_tensor += 1
            index_dims += [num_rows_out]

        return torch.ops.cuequivariance.tensor_product_uniform_1d_jit(
            "channelwise_kernel_fwd",
            self.math_dtype,
            self.operand_extent,
            len(self.operand_dim) - 1,
            1,
            num_index_tensor,
            self.operand_dim,
            self.operand_num_segments,
            [batch_dim_0, batch_dim_1, batch_dim_out],
            [index_tensor_0, index_tensor_1, index_tensor_out] + index_dims,
            list(range(len(self.operand_dim) - 1)) + [0],
            1,
            [len(self.operand_dim)],
            list(range(len(self.operand_dim))),
            [len(self.path_coefficients)],
            [0],
            [0],
            self.path_indices_flat,
            self.path_coefficients,
            self.batch_dim_auto,
            ins,
        )[0]


TensorProductUniform4x1dIndexed = TensorProductUniform4x1dIndexedJit
TensorProductUniform3x1dIndexed = TensorProductUniform3x1dIndexedJit

__all__ = ["TensorProductUniform4x1dIndexed", "TensorProductUniform3x1dIndexed"]
