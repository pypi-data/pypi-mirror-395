# SPDX-FileCopyrightText: Copyright (c) 2024 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: LicenseRef-NvidiaProprietary
#
# NVIDIA CORPORATION, its affiliates and licensors retain all intellectual
# property and proprietary rights in and to this material, related
# documentation and any modifications thereto. Any use, reproduction,
# disclosure or distribution of this material and related documentation
# without an express license agreement from NVIDIA CORPORATION or
# its affiliates is strictly prohibited.


from typing import List

import torch

import cuequivariance_ops_torch._ext as ext

# batch_dim: 0 shared, 1 batched, -1 indexed
BATCH_DIM_SHARED = 0
BATCH_DIM_BATCHED = 1
BATCH_DIM_INDEXED = -1
BATCH_DIM_AUTO = -2


def _setup_context(ctx, inputs, output):
    ctx.inputs = inputs[:-1]
    ctx.save_for_backward(*inputs[-1])


def _handle_batch_dim_auto(batch_size, batch_dim, tensors, index_tensors):
    new_batch_size = batch_size
    for t in index_tensors:
        if new_batch_size == BATCH_DIM_AUTO:
            new_batch_size = t.shape[0]
        else:
            torch._assert(new_batch_size == t.shape[0], "batch dim mismatch")
    new_batch_dim = list(batch_dim)
    for idx, (bd, t) in enumerate(zip(batch_dim, tensors)):
        if bd == BATCH_DIM_SHARED:
            torch._assert(t.shape[0] == 1, "shared batch dim must be 1")
        elif bd == BATCH_DIM_INDEXED:
            continue
        elif bd == BATCH_DIM_BATCHED:
            if new_batch_size == BATCH_DIM_AUTO:
                new_batch_size = t.shape[0]
            else:
                torch._assert(new_batch_size == t.shape[0], "batch dim mismatch")
        elif bd == BATCH_DIM_AUTO:
            if t.shape[0] == 1:
                new_batch_dim[idx] = BATCH_DIM_SHARED
            else:
                if new_batch_size == BATCH_DIM_AUTO:
                    new_batch_size = t.shape[0]
                else:
                    torch._assert(new_batch_size == t.shape[0], "batch dim mismatch")
                new_batch_dim[idx] = BATCH_DIM_BATCHED
        else:
            raise ValueError(f"Unknown batch dim kind {bd}")

    # Handle outputs
    for idx in range(len(tensors), len(batch_dim)):
        bd = batch_dim[idx]
        if bd == BATCH_DIM_AUTO:
            new_batch_dim[idx] = BATCH_DIM_BATCHED

    if new_batch_size == BATCH_DIM_AUTO:
        new_batch_size = 1

    if new_batch_size == 1:
        for idx in range(len(new_batch_dim)):
            if new_batch_dim[idx] == BATCH_DIM_SHARED:
                new_batch_dim[idx] = BATCH_DIM_BATCHED

    assert new_batch_size != BATCH_DIM_AUTO
    assert all(bs != BATCH_DIM_AUTO for bs in new_batch_dim)
    return new_batch_size, new_batch_dim


# dtypes: determines from which dtype to take that output buffer's dtype
# may be -1, which is the math_dtype
# index_buffer: the index buffer to use for the given tensor. ignored for non-indexed tensors. for index buffers, it contains the max value + 1, i.e. the size that is needed from the tensor
@torch.library.custom_op(
    "cuequivariance::tensor_product_uniform_1d_jit",
    mutates_args=(),
)
def _(
    name: str,
    math_dtype: torch.dtype,
    operand_extent: int,
    num_inputs: int,
    num_outputs: int,
    num_index: int,
    buffer_dim: List[int],
    buffer_num_segments: List[int],
    batch_dim: List[int],
    index_buffer: List[int],
    dtypes: List[int],
    num_operations: int,
    num_operands: List[int],
    operations: List[int],
    num_paths: List[int],
    path_indices_start: List[int],
    path_coefficients_start: List[int],
    path_indices: List[int],
    path_coefficients: List[float],
    batch_size: int,
    tensors: List[torch.Tensor],
) -> List[torch.Tensor]:
    batch_size, batch_dim = _handle_batch_dim_auto(
        batch_size, batch_dim, tensors[:num_inputs], tensors[num_inputs:]
    )
    outputs = []
    for i in range(num_inputs, num_inputs + num_outputs):
        if batch_dim[i] == BATCH_DIM_SHARED:
            size_0 = 1
        elif batch_dim[i] == BATCH_DIM_BATCHED:
            size_0 = batch_size
        elif batch_dim[i] == BATCH_DIM_INDEXED:
            size_0 = index_buffer[index_buffer[i] + num_inputs + num_outputs]
        if buffer_dim[i] == 0:
            size_1 = buffer_num_segments[i]
        if buffer_dim[i] == 1:
            size_1 = operand_extent * buffer_num_segments[i]
        if dtypes[i] == -1:
            dtype = math_dtype
        else:
            dtype = tensors[dtypes[i]].dtype
        outputs.append(
            torch.empty((size_0, size_1), dtype=dtype, device=tensors[0].device)
        )

    for i in range(num_inputs, num_inputs + num_outputs):
        if batch_dim[i] == BATCH_DIM_SHARED or batch_dim[i] == BATCH_DIM_INDEXED:
            outputs[i - num_inputs].zero_()

    jit = ext.tensor_product_uniform_1d_jit

    def map_dtype(t):
        if t == torch.float64:
            return jit.Datatype.kFloat64
        if t == torch.float32:
            return jit.Datatype.kFloat32
        if t == torch.float16:
            return jit.Datatype.kFloat16
        if t == torch.bfloat16:
            return jit.Datatype.kBFloat16
        if t == torch.int32:
            return jit.Datatype.kInt32
        if t == torch.int64:
            return jit.Datatype.kInt64

    def map_buffer_dim(o):
        if o == 0:
            return jit.Dimension.kScalar
        if o == 1:
            return jit.Dimension.kOneDimensional
        raise ValueError(f"Unknown dimension {o}")

    def map_batch_dim(o):
        if o == BATCH_DIM_BATCHED:
            return jit.BatchDimension.kBatched
        if o == BATCH_DIM_SHARED:
            return jit.BatchDimension.kShared
        if o == BATCH_DIM_INDEXED:
            return jit.BatchDimension.kIndexed
        raise ValueError(f"Unknown batch dimension {o}")

    operation_index = 0
    ops = []
    for i in range(num_operations):
        ops.append(operations[operation_index : operation_index + num_operands[i]])
        operation_index += num_operands[i]

    tensors = [t.contiguous() for t in tensors]
    # this unwraps torch.Parameters into torch.Tensor
    tensors = [t.reshape(t.shape) for t in tensors]
    tensors = tensors[:num_inputs] + outputs + tensors[num_inputs:]

    jit.run(
        name,
        map_dtype(math_dtype),
        operand_extent,
        num_inputs,
        num_outputs,
        num_index,
        [map_buffer_dim(b) for b in buffer_dim],
        buffer_num_segments,
        [map_batch_dim(b) for b in batch_dim],
        index_buffer[: num_inputs + num_outputs],
        [map_dtype(t.dtype) for t in tensors],
        ops,
        num_paths,
        path_indices_start,
        path_coefficients_start,
        path_indices,
        path_coefficients,
        batch_size,
        tensors,
        torch.cuda.current_stream().cuda_stream,
    )
    return outputs


@torch.library.register_fake(
    "cuequivariance::tensor_product_uniform_1d_jit",
)
def _(
    name: str,
    math_dtype: torch.dtype,
    operand_extent: int,
    num_inputs: int,
    num_outputs: int,
    num_index: int,
    buffer_dim: List[int],
    buffer_num_segments: List[int],
    batch_dim: List[int],
    index_buffer: List[int],
    dtypes: List[int],
    num_operations: int,
    num_operands: List[int],
    operations: List[int],
    num_paths: List[int],
    path_indices_start: List[int],
    path_coefficients_start: List[int],
    path_indices: List[int],
    path_coefficients: List[float],
    batch_size: int,
    tensors: List[torch.Tensor],
) -> List[torch.Tensor]:
    batch_size, batch_dim = _handle_batch_dim_auto(
        batch_size, batch_dim, tensors[:num_inputs], tensors[num_inputs:]
    )
    outputs = []
    for i in range(num_inputs, num_inputs + num_outputs):
        if batch_dim[i] == BATCH_DIM_SHARED:
            size_0 = 1
        elif batch_dim[i] == BATCH_DIM_BATCHED:
            size_0 = batch_size
        elif batch_dim[i] == BATCH_DIM_INDEXED:
            size_0 = index_buffer[index_buffer[i] + num_inputs + num_outputs]
        if buffer_dim[i] == 0:
            size_1 = buffer_num_segments[i]
        if buffer_dim[i] == 1:
            size_1 = operand_extent * buffer_num_segments[i]
        if dtypes[i] == -1:
            dtype = math_dtype
        else:
            dtype = tensors[dtypes[i]].dtype
        outputs.append(
            torch.empty((size_0, size_1), dtype=dtype, device=tensors[0].device)
        )
    return outputs


def _do_bwd_jit(ctx, grad):
    (
        orig_name,
        orig_math_dtype,
        orig_operand_extent,
        orig_num_inputs,
        orig_num_outputs,
        orig_num_index,
        orig_buffer_dim,
        orig_buffer_num_segments,
        orig_batch_dim,
        orig_index_buffer,
        orig_dtypes,
        orig_num_operations,
        orig_num_operands,
        orig_operations,
        orig_num_paths,
        orig_path_indices_start,
        orig_path_coefficients_start,
        orig_path_indices,
        orig_path_coefficients,
        orig_batch_size,
    ) = ctx.inputs

    orig_tensors = ctx.saved_tensors

    orig_batch_size, orig_batch_dim = _handle_batch_dim_auto(
        orig_batch_size,
        orig_batch_dim,
        orig_tensors[:orig_num_inputs],
        orig_tensors[orig_num_inputs:],
    )

    if "_fwd" in orig_name:
        # last arg to replace() is maxreplace
        bwd_name = orig_name.replace("_fwd", "_bwd", 1)
    elif "_bwd" in orig_name:
        bwd_name = orig_name.replace("_bwd", "_bwd_bwd", 1)
    else:
        bwd_name = orig_name + "_bwd"

    bwd_math_dtype = orig_math_dtype
    bwd_operand_extent = orig_operand_extent
    bwd_num_inputs = orig_num_inputs + orig_num_outputs
    bwd_num_outputs = sum(1 if ng else 0 for ng in ctx.needs_input_grad[-1])
    bwd_num_index = orig_num_index
    bwd_buffer_dim = orig_buffer_dim + [
        orig_buffer_dim[idx] for idx, ng in enumerate(ctx.needs_input_grad[-1]) if ng
    ]
    bwd_buffer_num_segments = orig_buffer_num_segments + [
        orig_buffer_num_segments[idx]
        for idx, ng in enumerate(ctx.needs_input_grad[-1])
        if ng
    ]
    bwd_batch_dim = orig_batch_dim + [
        orig_batch_dim[idx] for idx, ng in enumerate(ctx.needs_input_grad[-1]) if ng
    ]
    bwd_index_buffer = (
        orig_index_buffer[: orig_num_inputs + orig_num_outputs]
        + [
            orig_index_buffer[idx]
            for idx, ng in enumerate(ctx.needs_input_grad[-1])
            if ng
        ]
        + orig_index_buffer[orig_num_inputs + orig_num_outputs :]
    )
    bwd_dtypes = orig_dtypes + [
        orig_dtypes[idx] for idx, ng in enumerate(ctx.needs_input_grad[-1]) if ng
    ]

    operation_index = 0
    orig_ops = []
    for i in range(orig_num_operations):
        orig_ops.append(
            orig_operations[operation_index : operation_index + orig_num_operands[i]]
        )
        operation_index += orig_num_operands[i]

    bwd_ops = []
    bwd_num_paths = []
    bwd_path_indices_start = []
    bwd_path_coefficients_start = []
    output_idx = bwd_num_inputs
    for ng_idx, ng in enumerate(ctx.needs_input_grad[-1]):
        if not ng:
            continue
        # we want the derivative of input operand "idx"
        # and store it into output operand bwd_num_input_operands + output_idx
        # we have the gradients of the previous outputs in buffers orig_num_inputs ... orig_num_inputs + orig_num_outputs
        #   i.e. we can keep them as is!
        for ops_idx, op in enumerate(orig_ops):
            # for a given operation, if it uses "idx" at a position k:
            #   we replace "idx" at that position k with the output operand
            #   we replace the output operand with its gradient
            #   we add that to the list of operations
            #   we also have to replicate num_paths, num_indices_start, num_coefficients_start
            for op_idx, k in enumerate(op):
                if k == ng_idx:
                    bwd_op = list(op)
                    bwd_op[op_idx] = output_idx
                    bwd_ops.append(bwd_op)
                    bwd_num_paths.append(orig_num_paths[ops_idx])
                    bwd_path_indices_start.append(orig_path_indices_start[ops_idx])
                    bwd_path_coefficients_start.append(
                        orig_path_coefficients_start[ops_idx]
                    )

        output_idx += 1

    bwd_num_operations = len(bwd_ops)
    bwd_num_operands = [len(o) for o in bwd_ops]
    bwd_operations = [e for o in bwd_ops for e in o]

    bwd_path_indices = orig_path_indices
    bwd_path_coefficients = orig_path_coefficients
    bwd_batch_size = orig_batch_size

    bwd_tensors = (
        list(orig_tensors[:orig_num_inputs])
        + list(grad)
        + list(orig_tensors[orig_num_inputs:])
    )

    bwd_output = torch.ops.cuequivariance.tensor_product_uniform_1d_jit(
        bwd_name,
        bwd_math_dtype,
        bwd_operand_extent,
        bwd_num_inputs,
        bwd_num_outputs,
        bwd_num_index,
        bwd_buffer_dim,
        bwd_buffer_num_segments,
        bwd_batch_dim,
        bwd_index_buffer,
        bwd_dtypes,
        bwd_num_operations,
        bwd_num_operands,
        bwd_operations,
        bwd_num_paths,
        bwd_path_indices_start,
        bwd_path_coefficients_start,
        bwd_path_indices,
        bwd_path_coefficients,
        bwd_batch_size,
        bwd_tensors,
    )

    grad_list = []
    output_idx = 0
    for ng_idx, ng in enumerate(ctx.needs_input_grad[-1]):
        if not ng:
            grad_list.append(None)
        else:
            grad_list.append(bwd_output[output_idx])
            output_idx += 1

    grad_input = [None] * len(ctx.inputs)
    return *grad_input, grad_list


torch.library.register_autograd(
    "cuequivariance::tensor_product_uniform_1d_jit",
    _do_bwd_jit,
    setup_context=_setup_context,
)
