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

from enum import IntEnum
from typing import NamedTuple

import jax
import jax.numpy as jnp
import numpy as np
from jax import ffi

from ._common import _dtype


class BatchDimension(IntEnum):
    BATCHED = 0
    SHARED = 1
    INDEXED = 2


class SegmentDimension(IntEnum):
    SCALAR = 0
    VECTOR = 1


def _batch_dim(idx: int, size: int, batch_size: int) -> BatchDimension:
    if idx < 0:
        if size == batch_size:
            return BatchDimension.BATCHED
        else:
            return BatchDimension.SHARED
    else:
        return BatchDimension.INDEXED


def _seg_dim(buffer: jax.ShapeDtypeStruct, operand_extent: int) -> SegmentDimension:
    if buffer.shape[-1] == operand_extent:
        return SegmentDimension.VECTOR
    else:
        return SegmentDimension.SCALAR


class Operation(NamedTuple):
    buffers: list[int]
    start_path: int
    num_paths: int


class Path(NamedTuple):
    indices: list[int]
    coefficient: float


def _batch_size(sizes: list[int]) -> int:
    batch_size = 1
    for size in sizes:
        if size != 1:
            assert batch_size in {1, size}
            batch_size = size
    return batch_size


def _operand_extent(
    buffers: list[jax.ShapeDtypeStruct],
):
    operand_extent = max(x.shape[-1] for x in buffers)
    for x in buffers:
        assert x.shape[-1] in {1, operand_extent}, x.shape[-1]
    return operand_extent


def _operation_start_indices(
    paths: list[Path], operation_start_paths: np.ndarray
) -> np.ndarray:
    path_num_operands = np.array([len(path.indices) for path in paths], dtype=np.int32)
    start_indices = np.append(0, np.cumsum(path_num_operands))
    return start_indices[operation_start_paths].astype(np.int64)


def tensor_product_uniform_1d_jit(
    input_buffers: list[jax.Array],  # ndim = num_batch_axes + 2
    output_buffers_shape_dtype: list[jax.ShapeDtypeStruct],  # ndim = num_batch_axes + 2
    index_buffers: list[jax.Array],  # ndim = num_batch_axes
    buffer_index: list[list[int]],  # -1 if not indexed
    *,
    operations: list[Operation],
    paths: list[Path],
    math_dtype: jnp.dtype,
    name: str = "untitled",
) -> list[jax.Array]:
    """JIT-compiled CUDA implementation of tensor_product_uniform_1d."""
    input_buffers = list(input_buffers)
    output_buffers_shape_dtype = list(output_buffers_shape_dtype)
    index_buffers = list(index_buffers)
    buffer_index = np.array(buffer_index, dtype=np.int32)
    operations, paths = list(operations), list(paths)

    io_buffers = input_buffers + output_buffers_shape_dtype
    buffers = io_buffers + index_buffers
    assert buffer_index.shape[0] == len(buffers)

    # trick: ensure all outputs are "used" by adding dummy operations for unused outputs
    # this ensures that the kernel writes zeros to unused outputs (as expected by the XLA bindings)
    for i in range(len(input_buffers), len(io_buffers)):
        if not any(i in op.buffers for op in operations):
            operations.append(Operation([i], 0, 0))

    num_batch_axes = buffer_index.shape[1]
    for x in io_buffers:
        assert x.ndim == num_batch_axes + 2
    for i in index_buffers:
        assert i.ndim == num_batch_axes
        assert i.dtype.type in {jnp.int32, jnp.int64}

    batch_sizes = [
        _batch_size(
            [x.shape[i] for x, idx in zip(buffers, buffer_index[:, i]) if idx < 0],
        )
        for i in range(num_batch_axes)
    ]

    buffer_batch_dim = np.array(
        [
            [
                _batch_dim(idx, size, batch_size)
                for idx, size, batch_size in zip(idxs, x.shape, batch_sizes)
            ]
            for x, idxs in zip(buffers, buffer_index)
        ]
    )

    index_extent = [set() for _ in range(len(index_buffers))]
    for x, idxs in zip(buffers, buffer_index):
        for size, idx in zip(x.shape, idxs):
            if idx >= 0:
                index_extent[idx].add(size)
    assert all(len(x) == 1 for x in index_extent), index_extent
    index_extent = [x.pop() for x in index_extent]

    operand_extent = _operand_extent(io_buffers)

    math_dtype = jnp.dtype(math_dtype)
    assert math_dtype.type in {jnp.float32, jnp.float64, jnp.float16, jnp.bfloat16}

    # Check for unsupported cross-type conversions between fp16/bf16
    has_fp16_buffer = any(buf.dtype == jnp.float16 for buf in io_buffers)
    has_bf16_buffer = any(buf.dtype == jnp.bfloat16 for buf in io_buffers)

    assert not (has_fp16_buffer and math_dtype == jnp.bfloat16), (
        "fp16 input/output buffers with bf16 math_dtype are not supported (no fp16->bf16 conversion)"
    )
    assert not (has_bf16_buffer and math_dtype == jnp.float16), (
        "bf16 input/output buffers with fp16 math_dtype are not supported (no bf16->fp16 conversion)"
    )

    def ii(items):
        return np.array([i for i in items], dtype=np.int64)

    buffer_batch_dim = ii(buffer_batch_dim.flatten())
    buffer_num_segments = ii(x.shape[-2] for x in io_buffers)
    buffer_segments_dim = ii(_seg_dim(x, operand_extent) for x in io_buffers)
    buffer_index = ii(buffer_index.flatten())
    index_extent = ii(index_extent)
    buffer_dtype = ii(_dtype(x.dtype) for x in io_buffers + index_buffers)
    operation_num_operands = ii(len(op.buffers) for op in operations)
    operation_buffers = ii(b for op in operations for b in op.buffers)
    operation_num_paths = ii(op.num_paths for op in operations)
    operation_start_coeffs = ii(op.start_path for op in operations)
    operation_start_indices = _operation_start_indices(paths, operation_start_coeffs)
    path_indices = ii(i for path in paths for i in path.indices)
    path_coefficients = np.array([path.coefficient for path in paths], dtype=np.float64)
    batch_sizes = ii(batch_sizes)

    # print(f"{operand_extent=}")
    # print(f"num_indices={len(index_buffers)}")
    # print(f"{buffer_batch_dim=}")
    # print(f"{buffer_num_segments=}")
    # print(f"{buffer_segments_dim=}")
    # print(f"{buffer_index=}")
    # print(f"{index_extent=}")
    # print(f"{buffer_dtype=}")
    # print(f"{operation_num_operands=}")
    # print(f"{operation_buffers=}")
    # print(f"{operation_num_paths=}")
    # print(f"{operation_start_indices=}")
    # print(f"{operation_start_coeffs=}")
    # print(f"{path_indices=}")
    # print(f"{path_coefficients=}")
    # print(f"{batch_sizes=}", flush=True)

    call = ffi.ffi_call("tensor_product_uniform_1d_jit", output_buffers_shape_dtype)
    return call(
        *input_buffers,
        *index_buffers,
        name=name,
        math_dtype=_dtype(math_dtype),
        operand_extent=operand_extent,
        num_indices=len(index_buffers),
        buffer_batch_dim=buffer_batch_dim,
        buffer_num_segments=buffer_num_segments,
        buffer_segments_dim=buffer_segments_dim,
        buffer_index=buffer_index,
        index_extent=index_extent,
        buffer_dtype=buffer_dtype,
        operation_num_operands=operation_num_operands,
        operation_buffers=operation_buffers,
        operation_num_paths=operation_num_paths,
        operation_start_indices=operation_start_indices,
        operation_start_coeffs=operation_start_coeffs,
        path_indices=path_indices,
        path_coefficients=path_coefficients.view(np.int64),
        batch_sizes=batch_sizes,
    )
