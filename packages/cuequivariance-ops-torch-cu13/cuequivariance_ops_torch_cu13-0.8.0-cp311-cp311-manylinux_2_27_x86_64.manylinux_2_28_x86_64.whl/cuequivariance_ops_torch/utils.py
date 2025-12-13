# SPDX-FileCopyrightText: Copyright (c) 2024 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: LicenseRef-NvidiaProprietary
#
# NVIDIA CORPORATION, its affiliates and licensors retain all intellectual
# property and proprietary rights in and to this material, related
# documentation and any modifications thereto. Any use, reproduction,
# disclosure or distribution of this material and related documentation
# without an express license agreement from NVIDIA CORPORATION or
# its affiliates is strictly prohibited.

import enum
from typing import Any, Dict, List, Optional, Tuple, Union

import torch

# Flag to disable NVTX ranges in the code if desired.
ALLOW_NVTX = True

INT_TO_DTYPE = {0: torch.float64, 1: torch.float32, 2: torch.float16, 3: torch.bfloat16}
DTYPE_TO_INT = {torch.float64: 0, torch.float32: 1, torch.float16: 2, torch.bfloat16: 3}


def is_in_export_mode():
    if torch.jit.is_scripting():
        return False
    else:
        return (
            # TODO: this may become nontrivial if we want to support Torch-TensorRT
            torch.onnx.is_in_onnx_export()  # or is_fx_tracing()
        )


def maybe_to(arg, dtype):
    return arg if arg is None or arg.dtype == dtype else arg.to(dtype=dtype)


@torch.library.custom_op(
    "cuequivariance::identity_2",
    mutates_args=(),
    device_types="cuda",
)
def _(
    s: torch.Tensor,
    z: torch.Tensor,
) -> Tuple[torch.Tensor, torch.Tensor]:
    return s, z


@torch.library.register_fake("cuequivariance::identity_2")
def _(s: torch.Tensor, z: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor]:
    return torch.empty_like(s), torch.empty_like(z)


def identity_2(s, z):
    # WAR to break Myelin chain and prevent context memory from growing
    if is_in_export_mode():
        return torch.ops.cuequivariance.identity_2(s, z)
    else:
        return s, z


def nvtx_range_push(name: str):
    if not torch.compiler.is_compiling() and ALLOW_NVTX:
        torch.cuda.nvtx.range_push(name)


def nvtx_range_pop():
    if not torch.compiler.is_compiling() and ALLOW_NVTX:
        torch.cuda.nvtx.range_pop()


def get_operator_from_module(module, operator_base_str, dtypes):
    def _get_dtype(dtype):
        if dtype is torch.float64:
            return "fp64"
        if dtype is torch.float32:
            return "fp32"
        if dtype is torch.float16:
            return "fp16"
        if dtype is torch.bfloat16:
            return "bf16"
        if dtype is torch.float64:
            return "fp64"
        if dtype is torch.int16:
            return "int16"
        if dtype is torch.int8:
            return "int8"
        if dtype is torch.int32:
            return "int32"
        if dtype is torch.int64:
            return "int64"
        else:
            raise Exception("Unreconginzied torch data type.")

    dtypes = [_get_dtype(dt) for dt in dtypes]
    return getattr(module, operator_base_str + "_" + "_".join(dtypes))


def get_tensor_meta_data(tensor: Optional[torch.Tensor]) -> Dict[str, Any]:
    if tensor is None:
        return {"size": None, "dtype": None, "device": None}
    return {"size": tensor.size(), "dtype": tensor.dtype, "device": tensor.device}


def maybe_detach(tensor: torch.Tensor) -> Optional[torch.Tensor]:
    return None if tensor is None else tensor.detach().contiguous()


def maybe_size(tensor: torch.Tensor, dim: int = -1) -> int:
    return tensor.size(dim) if tensor is not None else 0


# The following functions are intended for usages where a gradient is only
# initialized if we have the corresponding ctx.needs_input_grads


def maybe_empty_like(
    input: torch.Tensor, create_tensor: bool = True, **kwargs
) -> Optional[torch.Tensor]:
    return torch.empty_like(input, **kwargs) if create_tensor else None


def maybe_empty(
    size: Union[List[int], Tuple[int], torch.Size],
    device: torch.device,
    dtype: torch.dtype,
    create_tensor: bool = True,
) -> Optional[torch.Tensor]:
    return torch.empty(size, device=device, dtype=dtype) if create_tensor else None


def maybe_zeros_like(
    input: torch.Tensor, create_tensor: bool = True
) -> Optional[torch.Tensor]:
    return torch.zeros_like(input) if create_tensor else None


def maybe_zeros(
    size: Union[List[int], Tuple[int], torch.Size],
    device: torch.device,
    dtype: torch.dtype,
    create_tensor: bool = True,
) -> Optional[torch.Tensor]:
    return torch.zeros(size, device=device, dtype=dtype) if create_tensor else None


class BenchmarkMode(enum.Enum):
    FLUSH_CACHE = 0
    FLUSH_CACHE_PEAK_PROXY = 1
    ROT_BUFFER = 2
    ROT_BUFFER_PEAK_PROXY = 3


def run_decoy(f, input_dict):
    _ = f(**input_dict)
    torch.cuda.synchronize()


def run_bench(
    f, input_dict, warmup_iter=250, run_iter=250, bench_mode=BenchmarkMode.ROT_BUFFER
):
    _ = f(**input_dict)

    if bench_mode in (BenchmarkMode.ROT_BUFFER, BenchmarkMode.ROT_BUFFER_PEAK_PROXY):
        len_rot = 4
        inputs_rot = [None] * len_rot
        for r in range(len_rot):
            r_inputs = []
            for key, value in input_dict.items():
                if isinstance(value, torch.Tensor):
                    if bench_mode == BenchmarkMode.ROT_BUFFER_PEAK_PROXY:
                        r_inputs.append(
                            (
                                key,
                                torch.ones_like(
                                    value, requires_grad=value.requires_grad
                                ),
                            )
                        )
                    else:
                        r_inputs.append(
                            (
                                key,
                                torch.randn_like(
                                    value, requires_grad=value.requires_grad
                                ),
                            )
                        )
                else:
                    r_inputs.append((key, value))
            r_inputs = dict(r_inputs)
            inputs_rot[r] = r_inputs

        for it in range(warmup_iter):
            _ = f(**inputs_rot[it % len_rot])

        start = torch.cuda.Event(enable_timing=True)
        end = torch.cuda.Event(enable_timing=True)
        start.record()
        for it in range(run_iter):
            _ = f(**inputs_rot[it % len_rot])
        end.record()
        torch.cuda.synchronize()
        elapsed = start.elapsed_time(end)

    elif bench_mode in (
        BenchmarkMode.FLUSH_CACHE,
        BenchmarkMode.FLUSH_CACHE_PEAK_PROXY,
    ):
        cache_filler = torch.empty(1024 * 1024 * 256, dtype=torch.int8, device="cuda")

        if bench_mode == BenchmarkMode.FLUSH_CACHE_PEAK_PROXY:
            _inputs = {}
            for key, value in input_dict.items():
                if isinstance(value, torch.Tensor):
                    _inputs.append(
                        (key, torch.ones_like(value, requires_grad=value.requires_grad))
                    )
                else:
                    _inputs.append((key, value))
            input_dict = _inputs

        for _ in range(warmup_iter):
            cache_filler.zero_()
            _ = f(**input_dict)

        starts = [torch.cuda.Event(enable_timing=True) for _ in range(run_iter)]
        ends = [torch.cuda.Event(enable_timing=True) for _ in range(run_iter)]
        for i in range(run_iter):
            cache_filler.zero_()
            starts[i].record()
            _ = f(**input_dict)
            ends[i].record()
        torch.cuda.synchronize()
        elapsed = sum(s.elapsed_time(e) for s, e in zip(starts, ends))

    return elapsed / run_iter
