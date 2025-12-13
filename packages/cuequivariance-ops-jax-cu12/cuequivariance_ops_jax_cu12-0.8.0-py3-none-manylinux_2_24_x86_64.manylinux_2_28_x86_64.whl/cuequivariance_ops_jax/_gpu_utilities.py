# SPDX-FileCopyrightText: Copyright (c) 2024 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: LicenseRef-NvidiaProprietary
#
# NVIDIA CORPORATION, its affiliates and licensors retain all intellectual
# property and proprietary rights in and to this material, related
# documentation and any modifications thereto. Any use, reproduction,
# disclosure or distribution of this material and related documentation
# without an express license agreement from NVIDIA CORPORATION or
# its affiliates is strictly prohibited.
"""GPU utility functions including no-op, sleep, synchronize, and GPU events.

GPU Events Implementation Attribution:
The GPU events functionality (event_record, event_elapsed) has been adapted from
JAX's GPU events implementation that was removed in version 0.7.2.

Original source: https://github.com/jax-ml/jax/
License: Apache License 2.0

JAX Copyright 2018 The JAX Authors.
Licensed under the Apache License, Version 2.0.
"""

from typing import Any

import jax
import jax.numpy as jnp
from jax import ffi


def _flatten(pytree: Any):
    """Helper to apply FFI function to JAX arrays in a pytree."""
    leaves, treedef = jax.tree.flatten(pytree)
    arrays = [(i, leaf) for i, leaf in enumerate(leaves) if isinstance(leaf, jax.Array)]
    _, values = zip(*arrays)

    def unflatten(outputs):
        for idx, (leaf_idx, _) in enumerate(arrays):
            leaves[leaf_idx] = outputs[idx]
        return jax.tree.unflatten(treedef, leaves)

    return values, unflatten


def noop(pytree: Any) -> Any:
    """
    No-op function that returns input pytree unchanged through FFI.

    Args:
        pytree: Any pytree structure containing JAX arrays

    Returns:
        The same pytree structure with arrays passed through FFI
    """
    vals, unflatten = _flatten(pytree)

    vals = ffi.ffi_call(
        "noop",
        [jax.ShapeDtypeStruct(arr.shape, arr.dtype) for arr in vals],
        input_output_aliases={i: i for i in range(len(vals))},
    )(*vals)

    return unflatten(vals)


def sleep(seconds: jax.Array, pytree: Any) -> tuple[jax.Array, Any]:
    """
    Sleep for the specified number of seconds and return input pytree unchanged.

    Args:
        seconds: Number of seconds to sleep (as a JAX array)
        pytree: Any pytree structure containing JAX arrays

    Returns:
        A tuple of (elapsed_ticks, pytree) where elapsed_ticks is the number of
        clock ticks that elapsed during the sleep operation
    """
    seconds = jnp.asarray(seconds, dtype=jnp.float32)
    vals, unflatten = _flatten(pytree)

    outputs = ffi.ffi_call(
        "sleep",
        [jax.ShapeDtypeStruct((), jnp.int64)]
        + [jax.ShapeDtypeStruct(arr.shape, arr.dtype) for arr in vals],
        input_output_aliases={i: i for i in range(1, len(vals) + 1)},
    )(seconds, *vals)
    elapsed_ticks, vals = outputs[0], outputs[1:]

    return elapsed_ticks, unflatten(vals)


def synchronize(pytree: Any) -> tuple[jax.Array, Any]:
    """
    Synchronize the current CUDA stream and return input pytree unchanged.

    Args:
        pytree: Any pytree structure containing JAX arrays

    Returns:
        A tuple of (elapsed_seconds, pytree) where elapsed_seconds is the time
        in seconds it took to synchronize the CUDA stream
    """
    vals, unflatten = _flatten(pytree)

    outputs = ffi.ffi_call(
        "synchronize",
        [jax.ShapeDtypeStruct((), jnp.float32)]
        + [jax.ShapeDtypeStruct(arr.shape, arr.dtype) for arr in vals],
        input_output_aliases={i: i + 1 for i in range(len(vals))},
    )(*vals)
    elapsed_seconds, vals = outputs[0], outputs[1:]

    return elapsed_seconds, unflatten(vals)


def event_record(pytree: Any, *, copy_before: bool = False) -> tuple[jax.Array, Any]:
    """
    Record a GPU event on the current CUDA stream and return the event handle.

    Args:
        pytree: Any pytree structure containing JAX arrays
        copy_before: If True, copy event handle to device before recording.
                    If False, copy after recording (default).

    Returns:
        A tuple of (event_handle, pytree) where event_handle is a uint64
        representing the CUDA event, and pytree is passed through unchanged.
    """
    vals, unflatten = _flatten(pytree)

    outputs = ffi.ffi_call(
        "event_record",
        [jax.ShapeDtypeStruct((), jnp.uint64)]  # event_handle
        + [jax.ShapeDtypeStruct(arr.shape, arr.dtype) for arr in vals],
        input_output_aliases={i: i + 1 for i in range(len(vals))},
    )(*vals, copy_before=copy_before)
    event_handle, vals = outputs[0], outputs[1:]

    return event_handle, unflatten(vals)


def event_elapsed(start_event: jax.Array, end_event: jax.Array) -> jax.Array:
    """
    Calculate elapsed time between two GPU events.

    Args:
        start_event: uint64 event handle from event_record()
        end_event: uint64 event handle from event_record()

    Returns:
        Elapsed time in milliseconds as a float32 scalar.
    """
    elapsed_ms = ffi.ffi_call(
        "event_elapsed",
        jax.ShapeDtypeStruct((), jnp.float32),
    )(start_event, end_event)

    return elapsed_ms
