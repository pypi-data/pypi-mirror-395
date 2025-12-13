# SPDX-FileCopyrightText: Copyright (c) 2024 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: LicenseRef-NvidiaProprietary
#
# NVIDIA CORPORATION, its affiliates and licensors retain all intellectual
# property and proprietary rights in and to this material, related
# documentation and any modifications thereto. Any use, reproduction,
# disclosure or distribution of this material and related documentation
# without an express license agreement from NVIDIA CORPORATION or
# its affiliates is strictly prohibited.

from typing import Optional, Tuple

import torch
import triton

from cuequivariance_ops.triton import (
    autotune_aot,
    fused_sigmoid_gated_dual_gemm_backward_pregemm_kernel,
    fused_sigmoid_gated_dual_gemm_forward_kernel,
)
from cuequivariance_ops.triton.utils import Precision
from cuequivariance_ops_torch.utils import (
    maybe_to,
    nvtx_range_pop,
    nvtx_range_push,
    run_bench,
    run_decoy,
)


def forward_kernel_input_generator(
    M: int,
    N: int,
    K: int,
    dtype_input: torch.dtype,
    two_inputs: bool,
    precision: bool,
):
    # TODO check if biases would need different configuration and thus different input generation
    x1 = torch.randn((M, K), dtype=dtype_input, device="cuda", requires_grad=True)
    x2 = (
        torch.randn((M, K), dtype=dtype_input, device="cuda", requires_grad=True)
        if two_inputs
        else None
    )
    w1 = torch.randn((N, K), dtype=dtype_input, device="cuda", requires_grad=True)
    w2 = torch.randn((N, K), dtype=dtype_input, device="cuda", requires_grad=True)
    mask = torch.randn((M), dtype=dtype_input, device="cuda", requires_grad=True)

    return {
        "x1": x1,
        "x2": x2,
        "w1": w1,
        "w2": w2,
        "b1": None,
        "b2": None,
        "mask": mask,
        "TRANSPOSE_OUT": False,
        "precision": precision,
    }


def forward_kernel_input_to_key(x1, x2, w1, w2, mask, precision, **unused_kwargs):
    # TODO check if biases would need different configuration
    M = x1.shape[0]
    K = x1.shape[1]
    N = w1.shape[0]

    TWO_INPUTS = True if x2 is not None else False

    input_type_x1 = x1.dtype if x1.dtype != torch.bfloat16 else torch.float16
    if x2 is not None:
        input_type_x2 = x2.dtype if x2.dtype != torch.bfloat16 else torch.float16
    else:
        input_type_x2 = None
    input_type_w1 = w1.dtype if w1.dtype != torch.bfloat16 else torch.float16
    input_type_w2 = w2.dtype if w2.dtype != torch.bfloat16 else torch.float16
    if mask is not None:
        input_type_mask = mask.dtype if mask.dtype != torch.bfloat16 else torch.float16
    else:
        input_type_mask = input_type_x1

    if M < 1024:
        kernel_key_m = triton.cdiv(M, 32) * 32
    elif M < 8192:
        kernel_key_m = triton.cdiv(M, 64) * 64
    elif M < 8192 * 2:
        kernel_key_m = triton.cdiv(M, 128) * 128
    elif M < 8192 * 4:
        kernel_key_m = triton.cdiv(M, 256) * 256
    elif M < 8192 * 8:
        kernel_key_m = triton.cdiv(M, 512) * 512
    elif M < 8192 * 16:
        kernel_key_m = triton.cdiv(M, 1024) * 1024
    elif M < 8192 * 32:
        kernel_key_m = triton.cdiv(M, 2048) * 2048
    else:
        kernel_key_m = 8192 * 32

    kernel_key_n = triton.cdiv(N, 16) * 16
    kernel_key_k = triton.cdiv(K, 16) * 16

    if input_type_x1 == torch.float32:
        if precision == Precision.TF32.value:
            precision_key = "tf32"
        else:
            precision_key = "tf32x3"
    else:
        precision_key = "default"

    return f"{kernel_key_m}_{kernel_key_n}_{kernel_key_k}_{input_type_x1}_{input_type_x2}_{input_type_w1}_{input_type_w2}_{input_type_mask}_{TWO_INPUTS}_False_False_{precision_key}"


@autotune_aot(
    input_generator=forward_kernel_input_generator,
    input_to_key=forward_kernel_input_to_key,
    input_configs=[
        {
            "M": m,
            "N": n,
            "K": 128,
            "dtype_input": torch.bfloat16,
            "two_inputs": two_inputs,
            "precision": Precision.DEFAULT.value,
        }
        for n in (128, 256)
        for two_inputs in (True, False)
        for m in range(32, 2048 * 2048 + 1, 32)
    ]
    + [
        {
            "M": m,
            "N": n,
            "K": 128,
            "dtype_input": torch.float32,
            "two_inputs": two_inputs,
            "precision": precision.value,
        }
        for n in (128, 256)
        for two_inputs in (True, False)
        for m in range(32, 2048 * 2048 + 1, 32)
        for precision in (Precision.TF32, Precision.TF32x3)
    ],
    tunable_configs=[
        {
            "TILE_M": tm,
            "TILE_N": tn,
            "TILE_K": tk,
            "num_stages": ns,
            "num_warps": nw,
        }
        for tm in (64, 128)
        for tn in (32, 64, 128)
        for tk in (16, 32, 64)
        for ns in (3, 4)
        for nw in (4, 8)
    ],
    prune_configs_fn=None,
    run_decoy=run_decoy,
    run_bench=run_bench,
)
def fused_sigmoid_gated_dual_gemm_forward_kernel_wrapper(
    x1,
    x2,
    w1,
    w2,
    b1,
    b2,
    mask,
    TRANSPOSE_OUT,
    TILE_M=64,
    TILE_N=32,
    TILE_K=32,
    num_stages=4,
    num_warps=4,
    precision=Precision.TF32x3.value,
):
    nvtx_range_push("fused_sigmoid_gated_dual_gemm_forward_kernel_wrapper")

    M = x1.shape[0]
    K = x1.shape[1]
    N = w1.shape[0]

    TWO_INPUTS = True if x2 is not None else False
    APPLY_MASK = True if mask is not None else False

    x1 = x1.contiguous()
    if x2 is not None:
        x2 = x2.contiguous()

    w1 = w1.contiguous()
    w2 = w2.contiguous()
    if b1 is not None:
        b1 = b1.contiguous()
    if b2 is not None:
        b2 = b2.contiguous()

    if mask is not None:
        mask = mask.contiguous()
        mask = mask.view(-1)
        assert mask.size(0) == M

    out = x1.new_empty((N, M) if TRANSPOSE_OUT else (M, N))

    def grid(META):
        assert N % META["TILE_N"] == 0
        assert K % META["TILE_K"] == 0
        return (triton.cdiv(M, META["TILE_M"]), N // META["TILE_N"], 1)

    NEEDS_INT64 = (M * K >= 2**31 - 1) or (M * N >= 2**31 - 1)

    fused_sigmoid_gated_dual_gemm_forward_kernel[grid](
        x1,
        x2,
        w1,
        w2,
        b1,
        b2,
        mask,
        M,
        N,
        K,
        out,
        TILE_M=TILE_M,
        TILE_N=TILE_N,
        TILE_K=TILE_K,
        PRECISION=precision,
        APPLY_MASK=APPLY_MASK,
        TRANSPOSE_OUT=TRANSPOSE_OUT,
        TWO_INPUTS=TWO_INPUTS,
        HAS_B1=b1 is not None,
        HAS_B2=b2 is not None,
        NEEDS_INT64=NEEDS_INT64,
        num_stages=num_stages,
        num_warps=num_warps,
    )
    nvtx_range_pop()
    return out


def backward_kernel_input_to_key(grad_out, x1, x2, w1, w2, mask, **unused_kwargs):
    # TODO check if biases would need different configuration
    M = x1.shape[0]
    K = x1.shape[1]
    N = w1.shape[0]

    TWO_INPUTS = True if x2 is not None else False

    input_type_x1 = x1.dtype if x1.dtype != torch.bfloat16 else torch.float16
    if x2 is not None:
        input_type_x2 = x2.dtype if x2.dtype != torch.bfloat16 else torch.float16
    else:
        input_type_x2 = None
    input_type_w1 = w1.dtype if w1.dtype != torch.bfloat16 else torch.float16
    input_type_w2 = w2.dtype if w2.dtype != torch.bfloat16 else torch.float16
    if mask is not None:
        input_type_mask = mask.dtype if mask.dtype != torch.bfloat16 else torch.float16
    else:
        input_type_mask = input_type_x1
    grad_out_type = (
        grad_out.dtype if grad_out.dtype != torch.bfloat16 else torch.float16
    )

    if M < 1024:
        kernel_key_m = triton.cdiv(M, 32) * 32
    elif M < 8192:
        kernel_key_m = triton.cdiv(M, 64) * 64
    elif M < 8192 * 2:
        kernel_key_m = triton.cdiv(M, 128) * 128
    elif M < 8192 * 4:
        kernel_key_m = triton.cdiv(M, 256) * 256
    elif M < 8192 * 8:
        kernel_key_m = triton.cdiv(M, 512) * 512
    elif M < 8192 * 16:
        kernel_key_m = triton.cdiv(M, 1024) * 1024
    elif M < 8192 * 32:
        kernel_key_m = triton.cdiv(M, 2048) * 2048
    else:
        kernel_key_m = 8192 * 32

    kernel_key_n = triton.cdiv(N, 16) * 16
    kernel_key_k = triton.cdiv(K, 16) * 16

    return f"{kernel_key_m}_{kernel_key_n}_{kernel_key_k}_{grad_out_type}_{input_type_x1}_{input_type_x2}_{input_type_w1}_{input_type_w2}_{input_type_mask}_{TWO_INPUTS}_False_False_tf32x3"


def backard_kernel_input_generator(
    M: int,
    N: int,
    K: int,
    dtype_input: torch.dtype,
    two_inputs: bool,
):
    # TODO check if biases would need different configuration and thus different input generation
    grad_out = torch.randn((M, N), dtype=dtype_input, device="cuda", requires_grad=True)
    x1 = torch.randn((M, K), dtype=dtype_input, device="cuda", requires_grad=True)
    x2 = (
        torch.randn((M, K), dtype=dtype_input, device="cuda", requires_grad=True)
        if two_inputs
        else None
    )
    w1 = torch.randn((N, K), dtype=dtype_input, device="cuda", requires_grad=True)
    w2 = torch.randn((N, K), dtype=dtype_input, device="cuda", requires_grad=True)
    mask = torch.randn((M), dtype=dtype_input, device="cuda", requires_grad=True)

    return {
        "grad_out": grad_out,
        "x1": x1,
        "x2": x2,
        "w1": w1,
        "w2": w2,
        "b1": None,
        "b2": None,
        "mask": mask,
        "TRANSPOSE_OUT": False,
    }


@autotune_aot(
    input_generator=backard_kernel_input_generator,
    input_to_key=backward_kernel_input_to_key,
    input_configs=[
        {
            "M": m,
            "N": n,
            "K": 128,
            "dtype_input": torch.bfloat16,
            "two_inputs": two_inputs,
        }
        for n in (128, 256)
        for two_inputs in (True, False)
        for m in range(32, 2048 * 2048 + 1, 32)
    ]
    + [
        {
            "M": m,
            "N": n,
            "K": 128,
            "dtype_input": torch.float32,
            "two_inputs": two_inputs,
        }
        for n in (128, 256)
        for two_inputs in (True, False)
        for m in range(32, 2048 * 2048 + 1, 32)
    ],
    tunable_configs=[
        {
            "TILE_M": tm,
            "TILE_N": tn,
            "TILE_K": tk,
            "num_stages": ns,
            "num_warps": nw,
        }
        for tm in (64, 128)
        for tn in (32, 64, 128)
        for tk in (16, 32, 64)
        for ns in (3, 4)
        for nw in (4, 8)
    ],
    prune_configs_fn=None,
    run_decoy=run_decoy,
    run_bench=run_bench,
)
def fused_sigmoid_gated_dual_gemm_backward_pregemm_kernel_wrapper(
    grad_out,
    x1,
    x2,
    w1,
    w2,
    b1,
    b2,
    mask,
    TRANSPOSE_OUT,
    TILE_M=64,
    TILE_N=32,
    TILE_K=32,
    num_stages=4,
    num_warps=4,
    precision=Precision.TF32x3.value,
):
    M = x1.shape[0]
    K = x1.shape[1]
    N = w1.shape[0]

    APPLY_MASK = True if mask is not None else False
    TWO_INPUTS = True if x2 is not None else False

    grad_xw1 = torch.empty((M, N), dtype=x1.dtype, device=x1.device)
    grad_xw2 = torch.empty((M, N), dtype=x1.dtype, device=x1.device)

    if APPLY_MASK:
        tiles_n_max = triton.cdiv(N, 32)
        tiles_n_actual = tiles_n_max
        grad_mask = torch.empty((tiles_n_max, M), dtype=torch.float32, device=x1.device)
    else:
        grad_mask = None

    def grid(META):
        assert N % META["TILE_N"] == 0
        assert K % META["TILE_K"] == 0
        nonlocal tiles_n_actual
        if APPLY_MASK:
            tiles_n_actual = triton.cdiv(N, META["TILE_N"])
        grid = (triton.cdiv(M, META["TILE_M"]), N // META["TILE_N"], 1)
        return grid

    NEEDS_INT64 = (M * K >= 2**31 - 1) or (M * N >= 2**31 - 1)

    fused_sigmoid_gated_dual_gemm_backward_pregemm_kernel[grid](
        grad_out,
        x1,
        x2,
        w1,
        w2,
        b1,
        b2,
        mask,
        M,
        N,
        K,
        grad_xw1,
        grad_xw2,
        grad_mask,
        TILE_M=TILE_M,
        TILE_N=TILE_N,
        TILE_K=TILE_K,
        APPLY_MASK=APPLY_MASK,
        TRANSPOSE_OUT=TRANSPOSE_OUT,
        PRECISION=precision,
        TWO_INPUTS=TWO_INPUTS,
        num_stages=num_stages,
        num_warps=num_warps,
        HAS_B1=b1 is not None,
        HAS_B2=b2 is not None,
        NEEDS_INT64=NEEDS_INT64,
    )

    if APPLY_MASK:
        grad_mask = grad_mask[0:tiles_n_actual, :].sum(dim=0).to(mask.dtype)

    return grad_xw1, grad_xw2, grad_mask


# TODO: figire how to add out arg here w/o breaking autotune
def _fused_gated_dual_gemm(
    x1: torch.Tensor,
    x2: Optional[torch.Tensor],
    w1: torch.Tensor,
    w2: torch.Tensor,
    b1: Optional[torch.Tensor] = None,
    b2: Optional[torch.Tensor] = None,
    mask: Optional[torch.Tensor] = None,
    transpose_out: bool = False,
    precision: int = Precision.DEFAULT.value,
) -> torch.Tensor:
    return fused_sigmoid_gated_dual_gemm_forward_kernel_wrapper(
        x1,
        x2,
        w1,
        w2,
        b1,
        b2,
        mask,
        TRANSPOSE_OUT=transpose_out,
        precision=precision,
    )


@torch.library.custom_op("cuequivariance::fused_gated_dual_gemm", mutates_args=())
def _(
    x1: torch.Tensor,
    x2: Optional[torch.Tensor],
    w1: torch.Tensor,
    w2: torch.Tensor,
    b1: Optional[torch.Tensor] = None,
    b2: Optional[torch.Tensor] = None,
    mask: Optional[torch.Tensor] = None,
    transpose_out: bool = False,
    precision: int = Precision.DEFAULT.value,
) -> torch.Tensor:
    return _fused_gated_dual_gemm(
        x1,
        x2,
        w1,
        w2,
        b1,
        b2,
        mask,
        transpose_out=transpose_out,
        precision=precision,
    )


@torch.library.register_fake("cuequivariance::fused_gated_dual_gemm")
def _(
    x1: torch.Tensor,
    x2: Optional[torch.Tensor],
    w1: torch.Tensor,
    w2: torch.Tensor,
    b1: Optional[torch.Tensor] = None,
    b2: Optional[torch.Tensor] = None,
    mask: Optional[torch.Tensor] = None,
    transpose_out: bool = False,
    precision: int = Precision.DEFAULT.value,
) -> torch.Tensor:
    N = w1.shape[0]
    M = x1.shape[0]
    return x1.new_empty((N, M) if transpose_out else (M, N))


def _dual_gemm_setup_context(ctx, inputs, output):
    x1, x2, w1, w2, b1, b2, mask, transpose_out, precision = inputs
    ctx.save_for_backward(x1, x2, w1, w2, b1, b2, mask)
    ctx.transpose_out = transpose_out
    ctx.precision = precision


@torch.library.custom_op(
    "cuequivariance::fused_gated_dual_gemm_backward", mutates_args=()
)
def _(
    grad_out: torch.Tensor,
    x1: torch.Tensor,
    x2: Optional[torch.Tensor],
    w1: torch.Tensor,
    w2: torch.Tensor,
    b1: Optional[torch.Tensor],
    b2: Optional[torch.Tensor],
    mask: Optional[torch.Tensor],
    transpose_out: bool,
    precision: int,
) -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
    grad_xw1, grad_xw2, grad_mask = (
        fused_sigmoid_gated_dual_gemm_backward_pregemm_kernel_wrapper(
            grad_out,
            x1,
            x2,
            w1,
            w2,
            b1,
            b2,
            mask,
            TRANSPOSE_OUT=transpose_out,
            precision=precision,
        )
    )
    return grad_xw1, grad_xw2, grad_mask


@torch.library.register_fake("cuequivariance::fused_gated_dual_gemm_backward")
def _(
    grad_out: torch.Tensor,
    x1: torch.Tensor,
    x2: Optional[torch.Tensor],
    w1: torch.Tensor,
    w2: torch.Tensor,
    b1: Optional[torch.Tensor],
    b2: Optional[torch.Tensor],
    mask: Optional[torch.Tensor],
    transpose_out: bool,
    precision: int,
) -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
    M = x1.shape[0]
    N = w1.shape[0]
    if mask is not None:
        grad_mask = torch.empty((M), dtype=torch.float32, device=x1.device)
    else:
        grad_mask = None
    grad_xw1 = torch.empty((M, N), dtype=x1.dtype, device=x1.device)
    grad_xw2 = torch.empty((M, N), dtype=x1.dtype, device=x1.device)
    return grad_xw1, grad_xw2, grad_mask


def _dual_gemm_backward(ctx, grad_out: torch.Tensor, *inputs):
    x1, x2, w1, w2, b1, b2, mask = ctx.saved_tensors
    grad_out = grad_out.contiguous()
    grad_out = grad_out.view(-1, w1.shape[0])

    nvtx_range_push("_dual_gemm_backward")

    grad_xw1, grad_xw2, grad_mask = (
        torch.ops.cuequivariance.fused_gated_dual_gemm_backward(
            grad_out,
            x1,
            x2,
            w1,
            w2,
            b1,
            b2,
            mask,
            transpose_out=ctx.transpose_out,
            precision=ctx.precision,
        )
    )

    grad_b1 = None
    grad_b2 = None

    if x2 is None:
        grad_w1 = grad_xw1.T @ x1
        grad_w2 = grad_xw2.T @ x1
        grad_x1 = grad_xw1 @ w1 + grad_xw2 @ w2
        grad_x2 = None
    else:
        grad_w1 = grad_xw1.T @ x1
        grad_w2 = grad_xw2.T @ x2
        grad_x1 = grad_xw1 @ w1
        grad_x2 = grad_xw2 @ w2

    if b1 is not None:
        grad_b1 = grad_xw1.sum(dim=0)
    if b2 is not None:
        grad_b2 = grad_xw2.sum(dim=0)
    nvtx_range_pop()
    return (
        grad_x1,
        grad_x2,
        grad_w1,
        grad_w2,
        grad_b1,
        grad_b2,
        grad_mask,
        None,
        None,
        None,
        None,
    )


torch.library.register_autograd(
    "cuequivariance::fused_gated_dual_gemm",
    _dual_gemm_backward,
    setup_context=_dual_gemm_setup_context,
)


def fused_sigmoid_gated_dual_gemm(
    x,
    w1,
    w2,
    mask=None,
    transpose_out=False,
    precision=None,
    b1=None,
    b2=None,
):
    """Apply fused sigmoid-gated dual GEMM operation.

    This function performs a dual matrix multiplication with sigmoid gating. The operation consists of:
    1. First matrix multiplication: x @ w1
    2. Second matrix multiplication: x @ w2
    3. Apply sigmoid to the first result
    4. Element-wise multiplication of sigmoid output with second result
    5. Optional masking of the final output

    Args:
        x (torch.Tensor): Input tensor. The last dimension must be K. Will be reshaped to (-1, K)
            for the operation. Original shape is preserved in the output.
        w1 (torch.Tensor): First weight matrix of shape (N, K) for the main projection.
        w2 (torch.Tensor): Second weight matrix of shape (N, K) for the gating projection.
        mask (torch.Tensor, optional): Optional mask tensor for element-wise multiplication with the output.
            If provided, must be compatible with the output shape through broadcasting.
            Defaults to None.
        transpose_out (bool, optional): Whether to transpose the output. If True,
            the last dimension becomes N and the other dimensions are preserved.
            Defaults to False.
        precision (Precision, optional): Precision mode for matrix multiplication.
            Can be None or IEEE. If None, automatically uses
            TF32 if torch.backends.cuda.matmul.allow_tf32 is True, otherwise TF32x3. If IEEE is provided,
            the precision will be set to IEEE-754 (standard fp32) for all weights.
            Defaults to None.
        b1 (torch.Tensor, optional): Optional bias tensor for the first MatMul. If provided, must have shape (N,).
        b2 (torch.Tensor, optional): Optional bias tensor for the second MatMul. If provided, must have shape (N,).

    Returns:
        torch.Tensor: Output tensor with shape (*x.shape[:-1], N) if transpose_out is False,
            or (N, *x.shape[:-1]) if transpose_out is True.

    Example:
        >>> x = torch.randn(1, 575, 575, 128, device="cuda", dtype=torch.float, requires_grad=True)  # (B, N, N, K)
        >>> w1 = torch.randn(128, 128, device="cuda", dtype=torch.float, requires_grad=True)          # (N, K)
        >>> w2 = torch.randn(128, 128, device="cuda", dtype=torch.float, requires_grad=True)          # (N, K)
        >>> out = fused_sigmoid_gated_dual_gemm(x, w1, w2)  # (B, N, N, K)
    """
    return fused_sigmoid_gated_dual_gemm_dual_x(
        x, None, w1, w2, mask, transpose_out, precision, b1, b2
    )


def fused_sigmoid_gated_dual_gemm_dual_x(
    x1,
    x2,
    w1,
    w2,
    mask=None,
    transpose_out=False,
    precision=None,
    b1=None,
    b2=None,
):
    """Apply fused sigmoid-gated dual GEMM operation with two input tensors.

    This function performs a dual matrix multiplication with sigmoid gating, using
    two separate input tensors. The operation consists of:
    1. First matrix multiplication: x1 @ w1
    2. Second matrix multiplication: x2 @ w2
    3. Apply sigmoid to the first result
    4. Element-wise multiplication of sigmoid output with second result
    5. Optional masking of the final output

    Args:
        x1 (torch.Tensor): First input tensor. The last dimension must be K. Will be reshaped
            to (-1, K) for the operation. Original shape is preserved in the output.
        x2 (torch.Tensor): Second input tensor. Must have the same shape as x1.
        w1 (torch.Tensor): First weight matrix of shape (N, K) for the main projection.
        w2 (torch.Tensor): Second weight matrix of shape (N, K) for the gating projection.
        mask (torch.Tensor, optional): Optional mask tensor for element-wise multiplication with the output.
            If provided, must be compatible with the output shape through broadcasting.
            Defaults to None.
        transpose_out (bool, optional): Whether to transpose the output. If True,
            the last dimension becomes N and the other dimensions are preserved.
            Defaults to False.
        precision (Precision, optional): Precision mode for matrix multiplication.
            Can be None, or IEEE. If None, automatically uses
            TF32 if torch.backends.cuda.matmul.allow_tf32 is True, otherwise TF32x3. If IEEE is provided,
            the precision will be set to IEEE-754 (standard fp32) for all weights.
            Defaults to None.
        b1 (torch.Tensor): Optional bias tensor for the first MatMul. If provided, must have shape (N,).
        b2 (torch.Tensor): Optional bias tensor for the second MatMul. If provided, must have shape (N,).

    Returns:
        torch.Tensor: Output tensor with shape (*x1.shape[:-1], N) if transpose_out is False,
            or (N, *x1.shape[:-1]) if transpose_out is True. For the example case with input shape
            (B, N, N, K), the output shape will be (B, N, N, K) if transpose_out is False.

    Example:
        >>> x1 = torch.randn(1, 575, 575, 128, device="cuda", dtype=torch.float, requires_grad=True)  # (B, N, N, K)
        >>> x2 = torch.randn(1, 575, 575, 128, device="cuda", dtype=torch.float, requires_grad=True)  # (B, N, N, K)
        >>> w1 = torch.randn(128, 128, device="cuda", dtype=torch.float, requires_grad=True)          # (N, K)
        >>> w2 = torch.randn(128, 128, device="cuda", dtype=torch.float, requires_grad=True)          # (N, K)
        >>> out = fused_sigmoid_gated_dual_gemm_dual_x(x1, x2, w1, w2)  # (B, N, N, K)
    """
    # Handle autocast conversion
    if torch.is_autocast_enabled():
        autocast_dtype = torch.get_autocast_dtype("cuda")
        x1 = maybe_to(x1, autocast_dtype)
        x2 = maybe_to(x2, autocast_dtype)
        w1 = maybe_to(w1, autocast_dtype)
        w2 = maybe_to(w2, autocast_dtype)
        b1 = maybe_to(b1, autocast_dtype)
        b2 = maybe_to(b2, autocast_dtype)

    if (
        x1.dtype.itemsize < 4
        or (w1.dtype != torch.float32)
        or (w2.dtype != torch.float32)
    ):
        precision = Precision.DEFAULT.value

    if precision == Precision.NONE.value:
        precision = (
            Precision.TF32.value
            if torch.backends.cuda.matmul.allow_tf32
            else Precision.TF32x3.value
        )

    x_shape = x1.shape

    K = x1.size(-1)
    N, KW = w1.shape
    N, KW = w2.shape

    assert KW == K

    if transpose_out:
        out_shape = torch.Size((N, *x_shape[:-1]))
    else:
        out_shape = torch.Size((*x_shape[:-1], N))

    x1 = x1.view(-1, K)
    if x2 is not None:
        assert x2.shape == x_shape
        x2 = x2.view(-1, K)

    out = torch.ops.cuequivariance.fused_gated_dual_gemm(
        x1, x2, w1, w2, b1, b2, mask, transpose_out, precision
    )

    return out.view(*out_shape)
