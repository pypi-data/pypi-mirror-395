# SPDX-FileCopyrightText: Copyright (c) 2024 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: LicenseRef-NvidiaProprietary
#
# NVIDIA CORPORATION, its affiliates and licensors retain all intellectual
# property and proprietary rights in and to this material, related
# documentation and any modifications thereto. Any use, reproduction,
# disclosure or distribution of this material and related documentation
# without an express license agreement from NVIDIA CORPORATION or
# its affiliates is strictly prohibited.
import ctypes
import importlib.metadata
import os
from enum import IntEnum

import jax.numpy as jnp
from jax import ffi

import cuequivariance_ops  # noqa: F401

# Load libcue_ops_jax.so
try:
    dist = importlib.metadata.distribution("cuequivariance_ops_jax")
    root = dist.locate_file("cuequivariance_ops_jax")
except Exception:
    # last resort, will fail with writeable install
    root = os.path.dirname(__file__)

path = os.path.join(root, "lib/libcue_ops_jax.so")
library = ctypes.cdll.LoadLibrary(path)

# Setup ctypes function signatures for needs_fp32_bias functions
library.needs_fp32_bias_fwd_ctypes.argtypes = [
    ctypes.c_int,
    ctypes.c_uint32,
    ctypes.c_uint32,
    ctypes.c_uint64,
]
library.needs_fp32_bias_fwd_ctypes.restype = ctypes.c_bool

library.needs_fp32_bias_bwd_ctypes.argtypes = [
    ctypes.c_int,
    ctypes.c_uint32,
    ctypes.c_bool,
    ctypes.c_uint64,
]
library.needs_fp32_bias_bwd_ctypes.restype = ctypes.c_bool

# Register the c++ functions with JAX
CUSTOM_FUNCS = [
    (
        "tensor_product_uniform_1d_jit",
        "tensor_product_uniform_1d_jit",
        "tensor_product_uniform_1d_cpu",
    ),
    ("indexed_linear_B", "indexed_linear_B", None),
    ("indexed_linear_C", "indexed_linear_C", None),
    ("triangle_attention_cuda_fwd", "triangle_attention_cuda_fwd", None),
    ("triangle_attention_cuda_bwd", "triangle_attention_cuda_bwd", None),
    ("noop", "noop_gpu", "noop_cpu"),
    ("sleep", "sleep_gpu", "sleep_cpu"),
    ("synchronize", "synchronize_gpu", "synchronize_cpu"),
    ("event_record", "event_record_gpu", "event_record_cpu"),
    ("event_elapsed", "event_elapsed_gpu", "event_elapsed_cpu"),
]

for name, cuda_fn, cpu_fn in CUSTOM_FUNCS:
    if cuda_fn is not None:
        ffi.register_ffi_target(
            name=name, fn=ffi.pycapsule(getattr(library, cuda_fn)), platform="CUDA"
        )
    if cpu_fn is not None:
        ffi.register_ffi_target(
            name=name, fn=ffi.pycapsule(getattr(library, cpu_fn)), platform="cpu"
        )


class DataType(IntEnum):
    FLOAT32 = 0
    FLOAT64 = 1
    FLOAT16 = 2
    BFLOAT16 = 3
    INT32 = 4
    INT64 = 5


def needs_fp32_bias_fwd(dtype: DataType, D: int, S_kv: int, stream_id: int = 0) -> bool:
    """Returns true if FP32 bias is needed for forward pass, false if same-dtype bias is used."""
    # Convert DataType enum to bits
    bits = 32  # Default to FP32
    if dtype == DataType.FLOAT16 or dtype == DataType.BFLOAT16:
        bits = 16
    elif dtype == DataType.FLOAT64:
        bits = 64
    return library.needs_fp32_bias_fwd_ctypes(bits, D, S_kv, stream_id)


def needs_fp32_bias_bwd(
    dtype: DataType, D: int, has_dbias_fp32_buf: bool, stream_id: int = 0
) -> bool:
    """Returns true if FP32 bias input is needed for backward pass, false if same-dtype bias is used."""
    # Convert DataType enum to bits
    bits = 32  # Default to FP32
    if dtype == DataType.FLOAT16 or dtype == DataType.BFLOAT16:
        bits = 16
    elif dtype == DataType.FLOAT64:
        bits = 64
    return library.needs_fp32_bias_bwd_ctypes(bits, D, has_dbias_fp32_buf, stream_id)


def _dtype(jax_dtype: jnp.dtype) -> DataType:
    try:
        return {
            jnp.float32: DataType.FLOAT32,
            jnp.float64: DataType.FLOAT64,
            jnp.float16: DataType.FLOAT16,
            jnp.bfloat16: DataType.BFLOAT16,
            jnp.int32: DataType.INT32,
            jnp.int64: DataType.INT64,
        }[jnp.dtype(jax_dtype).type]
    except KeyError:
        raise ValueError(f"Unsupported dtype: {jax_dtype}")
