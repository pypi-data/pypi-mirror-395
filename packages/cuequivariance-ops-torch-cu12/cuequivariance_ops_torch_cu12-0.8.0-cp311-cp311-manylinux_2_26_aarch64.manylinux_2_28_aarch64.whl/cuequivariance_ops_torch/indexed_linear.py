# SPDX-FileCopyrightText: Copyright (c) 2024 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: LicenseRef-NvidiaProprietary
#
# NVIDIA CORPORATION, its affiliates and licensors retain all intellectual
# property and proprietary rights in and to this material, related
# documentation and any modifications thereto. Any use, reproduction,
# disclosure or distribution of this material and related documentation
# without an express license agreement from NVIDIA CORPORATION or
# its affiliates is strictly prohibited.

from typing import Optional

import torch

import cuequivariance_ops_torch._ext.cuequivariance_ops_torch_ext as ops


def _get_workspace(counts: torch.Tensor, device: torch.device) -> torch.Tensor:
    """Calculate and create workspace tensor for indexed linear operations"""
    temp_storage_bytes_cub_ExclusiveSum = 1024
    workspace_size = (
        counts.numel() * 4 * torch.tensor([], dtype=torch.int64).element_size()
        + temp_storage_bytes_cub_ExclusiveSum
    )
    return torch.empty((workspace_size,), dtype=torch.uint8, device=device)


def indexed_linear_B(
    ptr_A: torch.Tensor,
    ptr_B: torch.Tensor,
    counts: torch.Tensor,
    transpose_B: bool,
    Z: int,
    C: int,
    u: int,
    v: int,
    coefficient: float,
    workspace: Optional[torch.Tensor] = None,
) -> torch.Tensor:
    """
    Indexed linear operation B: (Zu, Cuv/Cvu) -> Zv

    Parameters
    ----------
    ptr_A : torch.Tensor
        Input tensor A with shape (Z, u)
    ptr_B : torch.Tensor
        Input tensor B with shape (C, u, v) or (C, v, u) depending on transpose_B
    counts : torch.Tensor
        Integer tensor with shape (C,) containing counts
    transpose_B : bool
        Whether to transpose the B tensor
    Z : int
        Batch dimension
    C : int
        Number of segments
    u : int
        First dimension
    v : int
        Second dimension
    coefficient : float
        Scaling coefficient
    workspace : torch.Tensor, optional
        Workspace tensor for temporary storage

    Returns
    -------
    torch.Tensor
        Output tensor with shape (Z, v)
    """
    workspace = workspace or _get_workspace(counts, ptr_A.device)
    out = torch.zeros((Z, v), dtype=ptr_A.dtype, device=ptr_A.device)

    torch._assert(ptr_A.ndim == 2, "ptr_A must be a 2D tensor with shape [Z, u]")
    torch._assert(
        ptr_B.ndim == 3, "ptr_B must be a 3D tensor with shape [C, u, v] or [C, v, u]"
    )
    torch._assert(counts.ndim == 1, "counts must be a 1D tensor with shape [C]")
    torch._assert(out.ndim == 2, "out must be a 2D tensor with shape [Z, v]")

    # Call raw C++ operation with detached tensors - gradients are handled
    # separately by the autograd registration for the custom ops
    ops.indexed_linear_B(
        out,
        ptr_A.detach().contiguous(),
        ptr_B.detach().contiguous(),
        counts.contiguous(),
        workspace,
        transpose_B,
        Z,
        C,
        u,
        v,
        coefficient,
        torch.cuda.current_stream().cuda_stream,
    )

    return out


def indexed_linear_C(
    ptr_A: torch.Tensor,
    ptr_B: torch.Tensor,
    counts: torch.Tensor,
    Z: int,
    C: int,
    u: int,
    v: int,
    coefficient: float,
    workspace: Optional[torch.Tensor] = None,
) -> torch.Tensor:
    """
    Indexed linear operation C: (Zu, Zv) -> Cuv

    Parameters
    ----------
    ptr_A : torch.Tensor
        Input tensor A with shape (Z, u)
    ptr_B : torch.Tensor
        Input tensor B with shape (Z, v)
    counts : torch.Tensor
        Integer tensor with shape (C,) containing counts
    Z : int
        Batch dimension
    C : int
        Number of segments
    u : int
        First dimension
    v : int
        Second dimension
    coefficient : float
        Scaling coefficient
    workspace : torch.Tensor, optional
        Workspace tensor for temporary storage

    Returns
    -------
    torch.Tensor
        Output tensor with shape (C, u, v)
    """
    workspace = workspace or _get_workspace(counts, ptr_A.device)
    out = torch.zeros((C, u, v), dtype=ptr_A.dtype, device=ptr_A.device)

    torch._assert(ptr_A.ndim == 2, "ptr_A must be a 2D tensor with shape [Z, u]")
    torch._assert(ptr_B.ndim == 2, "ptr_B must be a 2D tensor with shape [Z, v]")
    torch._assert(counts.ndim == 1, "counts must be a 1D tensor with shape [C]")
    torch._assert(out.ndim == 3, "out must be a 3D tensor with shape [C, u, v]")

    # Call raw C++ operation with detached tensors - gradients are handled
    # separately by the autograd registration for the custom ops
    ops.indexed_linear_C(
        out,
        ptr_A.detach().contiguous(),
        ptr_B.detach().contiguous(),
        counts.contiguous(),
        workspace,
        Z,
        C,
        u,
        v,
        coefficient,
        torch.cuda.current_stream().cuda_stream,
    )

    return out


@torch.library.custom_op(
    "cuequivariance::indexed_linear_B",
    mutates_args=(),
    device_types="cuda",
)
def _(
    ptr_A: torch.Tensor,
    ptr_B: torch.Tensor,
    counts: torch.Tensor,
    transpose_B: bool,
    Z: int,
    C: int,
    u: int,
    v: int,
    coefficient: float,
) -> torch.Tensor:
    """Custom Torch operation for indexed_linear_B"""
    return indexed_linear_B(ptr_A, ptr_B, counts, transpose_B, Z, C, u, v, coefficient)


@torch.library.custom_op(
    "cuequivariance::indexed_linear_C",
    mutates_args=(),
    device_types="cuda",
)
def _(
    ptr_A: torch.Tensor,
    ptr_B: torch.Tensor,
    counts: torch.Tensor,
    Z: int,
    C: int,
    u: int,
    v: int,
    coefficient: float,
) -> torch.Tensor:
    """Custom Torch operation for indexed_linear_C"""
    return indexed_linear_C(ptr_A, ptr_B, counts, Z, C, u, v, coefficient)


def indexed_linear(
    A: torch.Tensor,
    B: torch.Tensor,
    counts: torch.Tensor,
    u: int,
    v: int,
    C: int,
    Z: int,
    subscripts: tuple[str, str, str],
    coefficient: float,
) -> torch.Tensor:
    """
    Indexed linear operation with automatic subscript handling

    This function mimics the JAX implementation and automatically determines
    which kernel to call based on the subscripts.

    Parameters
    ----------
    A : torch.Tensor
        First input tensor
    B : torch.Tensor
        Second input tensor
    counts : torch.Tensor
        Integer tensor with shape (C,) containing counts
    u : int
        First dimension
    v : int
        Second dimension
    C : int
        Number of segments
    Z : int
        Batch dimension
    subscripts : tuple[str, str, str]
        Subscript notation for the operation
    coefficient : float
        Scaling coefficient

    Returns
    -------
    torch.Tensor
        Output tensor with appropriate shape based on subscripts
    """
    original_subscripts = subscripts

    # Handle subscript transformations
    swap_A_B = subscripts in [
        ("u", "v", "vu"),
        ("uv", "v", "u"),
        ("vu", "v", "u"),
        ("v", "u", "uv"),
        ("uv", "u", "v"),
        ("vu", "u", "v"),
    ]
    swap_u_v = subscripts in [
        ("u", "v", "vu"),
        ("uv", "v", "u"),
        ("vu", "v", "u"),
        ("v", "uv", "u"),
        ("v", "vu", "u"),
        ("v", "u", "vu"),
    ]

    if swap_u_v:
        subscripts = tuple(s.translate(str.maketrans("uv", "vu")) for s in subscripts)
        u, v = v, u

    if swap_A_B:
        subscripts = (subscripts[1], subscripts[0], subscripts[2])
        A, B = B, A

    # Ensure tensors are contiguous
    A, B, counts = A.contiguous(), B.contiguous(), counts.contiguous()

    if subscripts == ("u", "v", "uv"):
        return torch.ops.cuequivariance.indexed_linear_C(
            A, B, counts, Z, C, u, v, coefficient
        )
    elif subscripts in [("u", "uv", "v"), ("u", "vu", "v")]:
        transpose_B = subscripts == ("u", "vu", "v")
        return torch.ops.cuequivariance.indexed_linear_B(
            A, B, counts, transpose_B, Z, C, u, v, coefficient
        )
    else:
        raise ValueError(f"Invalid subscripts: {original_subscripts}.")


# Autograd implementations
def _setup_context_base(ctx, inputs, needs_grad_indices):
    """Base setup context function for autograd"""
    ctx.saved_tensors_and_args = inputs
    ctx.needs_input_grad = [
        inputs[i].requires_grad if i < needs_grad_indices else False
        for i in range(len(inputs))
    ]


def indexed_linear_B_backward(ctx, grad_output):
    """Backward pass for indexed_linear_B"""
    ptr_A, ptr_B, counts, transpose_B, Z, C, u, v, coefficient = (
        ctx.saved_tensors_and_args
    )
    grad_A = grad_B = None

    if ctx.needs_input_grad[0]:  # grad wrt A
        # Forward: C[Zv] = A[Zu] @ B[Cuv] (or B[Cvu] if transpose_B=True)
        # Backward: dA[Zu] = dC[Zv] @ B[Cuv]^T (or B[Cvu] if transpose_B=True)
        grad_A = torch.ops.cuequivariance.indexed_linear_B(
            grad_output, ptr_B, counts, not transpose_B, Z, C, v, u, coefficient
        )

    if ctx.needs_input_grad[1]:  # grad wrt B
        # Forward: C[Zv] = A[Zu] @ B[Cuv] (or B[Cvu] if transpose_B=True)
        # Backward: dB[Cuv] = A[Zu]^T @ dC[Zv] (or dB[Cvu] if transpose_B=True)
        if transpose_B:
            # B was (C, v, u), so grad_B should also be (C, v, u)
            # dB[Cvu] = dC[Zv]^T @ A[Zu] = indexed_linear_C(dC[Zv], A[Zu])
            grad_B = torch.ops.cuequivariance.indexed_linear_C(
                grad_output, ptr_A, counts, Z, C, v, u, coefficient
            )
        else:
            # B was (C, u, v), so grad_B should also be (C, u, v)
            # dB[Cuv] = A[Zu]^T @ dC[Zv] = indexed_linear_C(A[Zu], dC[Zv])
            grad_B = torch.ops.cuequivariance.indexed_linear_C(
                ptr_A, grad_output, counts, Z, C, u, v, coefficient
            )

    return grad_A, grad_B, None, None, None, None, None, None, None


def indexed_linear_B_setup_context(ctx, inputs, output):
    """Setup context for indexed_linear_B backward pass"""
    _setup_context_base(ctx, inputs, 2)


def indexed_linear_C_backward(ctx, grad_output):
    """Backward pass for indexed_linear_C"""
    ptr_A, ptr_B, counts, Z, C, u, v, coefficient = ctx.saved_tensors_and_args
    grad_A = grad_B = None

    if ctx.needs_input_grad[0]:  # grad wrt A
        # Forward: D[Cuv] = indexed_linear_C(A[Zu], B[Zv])
        # Backward: dA[Zu] = indexed_linear_B(B[Zv], dD[Cuv], transpose_B=True)
        grad_A = torch.ops.cuequivariance.indexed_linear_B(
            ptr_B, grad_output, counts, True, Z, C, v, u, coefficient
        )

    if ctx.needs_input_grad[1]:  # grad wrt B
        # Forward: D[Cuv] = indexed_linear_C(A[Zu], B[Zv])
        # Backward: dB[Zv] = indexed_linear_B(A[Zu], dD[Cuv], transpose_B=False)
        grad_B = torch.ops.cuequivariance.indexed_linear_B(
            ptr_A, grad_output, counts, False, Z, C, u, v, coefficient
        )

    return grad_A, grad_B, None, None, None, None, None, None


def indexed_linear_C_setup_context(ctx, inputs, output):
    """Setup context for indexed_linear_C backward pass"""
    _setup_context_base(ctx, inputs, 2)


# Register autograd functions
torch.library.register_autograd(
    "cuequivariance::indexed_linear_B",
    indexed_linear_B_backward,
    setup_context=indexed_linear_B_setup_context,
)

torch.library.register_autograd(
    "cuequivariance::indexed_linear_C",
    indexed_linear_C_backward,
    setup_context=indexed_linear_C_setup_context,
)
