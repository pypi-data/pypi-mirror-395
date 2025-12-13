# SPDX-FileCopyrightText: Copyright (c) 2024 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: LicenseRef-NvidiaProprietary
#
# NVIDIA CORPORATION, its affiliates and licensors retain all intellectual
# property and proprietary rights in and to this material, related
# documentation and any modifications thereto. Any use, reproduction,
# disclosure or distribution of this material and related documentation
# without an express license agreement from NVIDIA CORPORATION or
# its affiliates is strictly prohibited.


import logging
import warnings
from typing import Optional

import torch
import torch.nn as nn

from cuequivariance_ops_torch.tensor_product_uniform_1d_jit import (
    BATCH_DIM_AUTO,
    BATCH_DIM_BATCHED,
    BATCH_DIM_INDEXED,
)

logger = logging.getLogger(__name__)


class TensorProductUniform1dJit(nn.Module):
    SUPPORTED_DIMS = [3, 4]
    SUPPORTED_EXTENT_MULTIPLE = 32
    SUPPORTED_TOTAL_SEGMENTS = 256

    @classmethod
    def is_supported(
        cls,
        operand_dim: list[int],
        operand_extent: int,
        operand_num_segments: list[int],
    ):
        """
        Check if the kernel supports operations with the given parameters.

        See ``__init__`` for a description of the paramters.
        """
        num_operands = len(operand_num_segments)
        try:
            assert num_operands in cls.SUPPORTED_DIMS
            assert len(operand_dim) == num_operands
            # assert operand_extent % cls.SUPPORTED_EXTENT_MULTIPLE == 0
            # assert sum(operand_num_segments) <= cls.SUPPORTED_TOTAL_SEGMENTS
        except AssertionError:
            return False
        return True

    def __init__(
        self,
        operand_dim: list[int],
        operand_extent: int,
        operand_num_segments: list[int],
        path_indices: list[list[int]],
        path_coefficients: list[float],
        math_dtype: torch.dtype = torch.float32,
    ):
        """
        A tensor product implementation for scalar and vector operands where
        all vectors have the same length.

        Parameters
        ----------
        operand_dim: list[int]
            ``operand_dim[i]`` may be either 0 or 1, and indicates whether that
            operand ``i`` has scalar (0-dimensional) or vector (1-dimensional)
            segments.
        operand_extent: int
            The extent (number of elements) of each vector operand segment. Must
            be a multiple of ``SUPPORTED_EXTENT_MULTIPLE``.
        operand_num_segments: list[int]
            The number of segments for each operand.
        path_indices: list[list[int]]
            Each element of this list is a single computation, i.e. which input
            operands get multiplied together and then and added to which output
            segment.
        path_coefficients: list[float]
            The scaling factor for each entry in ``path_indices``.
        math_dtype: torch.dtype
            The data type used for internal computation. May be FP32 or FP64.
            All inputs will be cast to this type, and all multiplications and
            additions will be performed at this precision (except for atomic
            output accumulation, which occurs at input precision).

        Example
        -------
        For this example, let's say that we use this kernel to implement
        complex-complex multiplication, i.e. two inputs, one output
        (three operands total) and two segments each (real and imaginary).
        Then, this would encode the multiplication rule:

        >>> m = TensorProductUniform1d(
        ...        [1, 1, 1], 32, [2, 2, 2],
        ...        [[0, 0, 0], [1, 1, 0], [1, 0, 1], [0, 1, 1]],
        ...        [1.0, -1.0, 1.0, 1.0])

        This encodes the following operation with plain torch:

        >>> input_0_segment_0 = torch.randn((batch, 32,))
        >>> input_0_segment_1 = torch.randn((batch, 32,))
        >>> input_1_segment_0 = torch.randn((batch, 32,))
        >>> input_1_segment_1 = torch.randn((batch, 32,))
        >>> output_segment_0 = input_0_segment_0 * input_1_segment_0 - \
        ...     input_0_segment_1 * input_1_segment_1
        >>> output_segment_1 = input_0_segment_0 * input_1_segment_1 + \
        ...     input_0_segment_1 * input_1_segment_0

        Or, using our kernel:

        >>> input_0 = torch.randn((batch, 2*32), device='cuda')
        >>> input_1 = torch.randn((batch, 2*32), device='cuda')
        >>> m = m.to('cuda')
        >>> output = m(input_0, input_1)

        """
        assert self.is_supported(operand_dim, operand_extent, operand_num_segments)
        assert len(path_indices) == len(path_coefficients)
        assert len(path_coefficients) > 0
        self.num_operands = len(operand_num_segments)
        assert all(
            len(path_indices[i]) == self.num_operands
            for i, _ in enumerate(path_indices)
        )
        logger.debug(
            "TensorProductUniform4x1d.__init__("
            + f"operand_dim={operand_dim}, operand_extent={operand_extent}, "
            + f"operand_num_segments={operand_num_segments}, path_indices=..., "
            + f"path_coefficients=..., math_dtype={math_dtype})"
        )
        logger.debug(
            f"TensorProductUniform4x1d.__init__(path_indices={path_indices}, "
            + f"path_coefficients={path_coefficients})"
        )

        super().__init__()

        warnings.warn(
            "TensorProductUniform1d is deprecated and will be removed in a future version.\n"
            "Please use SegmentedPolynomial from the frontend with the appropriate method."
        )

        self.number_of_output_segments = operand_num_segments[-1]
        self.number_of_paths = len(path_indices)
        self.math_dtype = math_dtype

        self.operand_dim = operand_dim
        self.operand_extent = operand_extent
        self.operand_num_segments = operand_num_segments
        self.path_indices = path_indices
        self.path_indices_flat = [pi for p in path_indices for pi in p]
        self.path_coefficients = path_coefficients

        self.batch_dim_auto = BATCH_DIM_AUTO
        self.batch_dim_batched = BATCH_DIM_BATCHED
        self.batch_dim_indexed = BATCH_DIM_INDEXED

    def forward(
        # Torch FX strongly dislikes *args usage here
        self,
        in0: torch.Tensor,
        in1: torch.Tensor,
        in2: Optional[torch.Tensor] = None,
    ) -> torch.Tensor:
        """
        Execute the TensorProductUniform1d kernel.

        For an example, see ``__init__``.

        Each operand is a torch tensor with one or two dimensions. If it is two-
        dimensional, the first dimension is the batch dimension and must match
        across all input tensors that have a batch dimension. It will also be
        the first dimension of the returned tensor.
        Generally, a sufficiently large batch dimension is required for good
        performance. The last tensor dimension contains all the segments of the
        operand packed together, so it is of size
        ``operand_num_segments[i] * operand_extent`` for vector operands (i.e.,
        where ``operand_dim[i] == 1``) or just ``operand_num_segments[i]`` for
        scalar operands.

        Parameters
        ----------
        in0: torch.Tensor
            The first operand of the tensor product.
        in1: torch.Tensor
            The second operand of the tensor product.
        in2: torch.Tensor
            The third operand of the tensor product. Required for 4-dimensional
            tensor products, ignored for 3-dimensional tensor products.

        Returns
        -------
        torch.Tensor
            The last (output) operand of the tensor product.
        """

        if in2 is not None:
            ins = [in0, in1, in2]
            torch._assert(len(self.operand_dim) == 4, "Must pass three tensors")
        else:
            ins = [in0, in1]
            torch._assert(len(self.operand_dim) == 3, "Must pass two tensors")
        return torch.ops.cuequivariance.tensor_product_uniform_1d_jit(
            "channelwise_kernel_fwd",
            self.math_dtype,
            self.operand_extent,
            len(self.operand_dim) - 1,
            1,
            0,
            self.operand_dim,
            self.operand_num_segments,
            [self.batch_dim_auto] * len(self.operand_dim),
            [-1] * len(self.operand_dim),
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


TensorProductUniform4x1d = TensorProductUniform1dJit
TensorProductUniform1d = TensorProductUniform1dJit

__all__ = ["TensorProductUniform4x1d", "TensorProductUniform1d"]
