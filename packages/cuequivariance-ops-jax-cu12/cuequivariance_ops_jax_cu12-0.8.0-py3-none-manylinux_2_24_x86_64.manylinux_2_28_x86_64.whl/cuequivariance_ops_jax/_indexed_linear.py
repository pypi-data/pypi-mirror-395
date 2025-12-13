# SPDX-FileCopyrightText: Copyright (c) 2024 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: LicenseRef-NvidiaProprietary
#
# NVIDIA CORPORATION, its affiliates and licensors retain all intellectual
# property and proprietary rights in and to this material, related
# documentation and any modifications thereto. Any use, reproduction,
# disclosure or distribution of this material and related documentation
# without an express license agreement from NVIDIA CORPORATION or
# its affiliates is strictly prohibited.
from __future__ import annotations

import jax
import jax.numpy as jnp
from jax import ffi

from ._common import _dtype
from ._cublas_enums import cublas_compute_types


def indexed_linear(
    A: jax.Array,
    B: jax.Array,
    D: jax.ShapeDtypeStruct,
    counts: jax.Array,
    u: int,
    v: int,
    C: int,
    Z: int,
    subscripts: tuple[str, str, str],
    coefficient: float,
    math_dtype: str | None = None,
) -> jax.Array:
    """
    Performance benchmarks for compatible dtype + math_dtype combinations
    (Problem size: u=512, v=512, Z=10,000):

    | Rank | Dtype + Math Dtype                    | Time (ms) | Speedup vs float64 |
    |------|---------------------------------------|-----------|-------------------|
    | 🥇   | bfloat16 + CUBLAS_COMPUTE_32F         | 0.0891    | 83.9x            |
    | 🥈   | float16 + CUBLAS_COMPUTE_32F          | 0.0911    | 82.1x            |
    | 🥉   | float32 + CUBLAS_COMPUTE_32F_FAST_TF32| 0.1403    | 53.3x            |
    | 4th  | float32 + CUBLAS_COMPUTE_32F_PEDANTIC | 0.1987    | 37.6x            |
    | 5th  | float32 + CUBLAS_COMPUTE_32F          | 0.2038    | 36.7x            |
    | 6th  | float64 + CUBLAS_COMPUTE_64F          | 7.4742    | 1.0x (baseline)  |
    """
    subscripts = tuple(subscripts)
    original_subscripts = subscripts
    assert len(subscripts) == 3
    swap_u_v = False
    swap_A_B = False

    dtype = jnp.dtype(A.dtype)
    assert dtype == B.dtype
    assert dtype == D.dtype

    if math_dtype is None:
        dtype_to_compute_type = {
            jnp.bfloat16: cublas_compute_types.CUBLAS_COMPUTE_32F,  # Use 32F compute type for bf16
            jnp.float16: cublas_compute_types.CUBLAS_COMPUTE_32F,  # Use 32F compute type for fp16
            jnp.float32: cublas_compute_types.CUBLAS_COMPUTE_32F,
            jnp.float64: cublas_compute_types.CUBLAS_COMPUTE_64F,
        }
        if dtype.type not in dtype_to_compute_type:
            raise ValueError(
                f"For dtype '{dtype}', please specify math_dtype manually and check CUBLAS documentation "
                f"for compatible compute types."
            )
        compute_type = dtype_to_compute_type[dtype.type]
    else:
        if not hasattr(cublas_compute_types, math_dtype):
            supported_types = [
                attr
                for attr in dir(cublas_compute_types)
                if attr.startswith("CUBLAS_COMPUTE_")
            ]
            raise ValueError(
                f"Unsupported math_dtype '{math_dtype}'. "
                f"The supported compute types are: {supported_types}. "
                f"Be careful as they are not compatible with all I/O dtype combinations. "
                f"Have a look at the CUBLAS documentation for compatibility details."
            )
        compute_type = getattr(cublas_compute_types, math_dtype)

    if subscripts in [("u", "v", "vu"), ("uv", "v", "u"), ("vu", "v", "u")]:
        swap_A_B = True
        swap_u_v = True
    if subscripts in [("v", "uv", "u"), ("v", "vu", "u"), ("v", "u", "vu")]:
        swap_u_v = True
    if subscripts in [("v", "u", "uv"), ("uv", "u", "v"), ("vu", "u", "v")]:
        swap_A_B = True

    if swap_u_v:
        subscripts = tuple(
            x.replace("u", "q").replace("v", "u").replace("q", "v") for x in subscripts
        )
        u, v = v, u

    if swap_A_B:
        subscripts = (subscripts[1], subscripts[0], subscripts[2])
        A, B = B, A

    temp_storage_bytes_cub_ExclusiveSum = 1024  # TODO this seems to be sufficient but we never know if it's enough for all use cases and GPUs
    workspace_size = (
        counts.size * (3 + 1) * jnp.dtype(jnp.int64).itemsize
        + temp_storage_bytes_cub_ExclusiveSum
    )
    workspace = jnp.empty((workspace_size,), dtype=jnp.int8)

    if subscripts == ("u", "v", "uv"):
        (D, _) = ffi.ffi_call("indexed_linear_C", (D, workspace))(
            A,
            B,
            counts,
            compute_type=compute_type,
            u=u,
            v=v,
            C=C,
            Z=Z,
            coefficient=coefficient,
            dtype_A=_dtype(A.dtype),
            dtype_B=_dtype(B.dtype),
            dtype_D=_dtype(D.dtype),
        )
        return D

    if subscripts == ("u", "uv", "v"):
        transpose_B = False
    elif subscripts == ("u", "vu", "v"):
        transpose_B = True
    else:
        raise ValueError(f"Invalid subscripts: {original_subscripts}.")

    (D, _) = ffi.ffi_call("indexed_linear_B", (D, workspace))(
        A,
        B,
        counts,
        compute_type=compute_type,
        u=u,
        v=v,
        C=C,
        Z=Z,
        transpose_B=transpose_B,
        coefficient=coefficient,
        dtype_A=_dtype(A.dtype),
        dtype_B=_dtype(B.dtype),
        dtype_D=_dtype(D.dtype),
    )
    return D
