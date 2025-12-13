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

from functools import partial

import jax
import jax.numpy as jnp
from jax import ffi

import cuequivariance_ops  # noqa: F401

from ._common import _dtype, needs_fp32_bias_bwd, needs_fp32_bias_fwd


def use_tf32(precision: jax.lax.Precision | None, dtype) -> bool:
    # Type check: ensure precision is a jax.lax.Precision enum value or None
    if precision is not None:
        assert isinstance(precision, jax.lax.Precision), (
            f"precision must be jax.lax.Precision or None, got {type(precision).__name__}: {precision}"
        )

    if dtype != jnp.float32:
        return False

    precision = precision or jax.config.jax_default_matmul_precision

    if precision is None:
        return False

    match precision:
        case jax.lax.Precision.DEFAULT:
            return True
        case jax.lax.Precision.HIGH:
            return True
        case jax.lax.Precision.HIGHEST:
            return False


@partial(jax.jit, static_argnames=("scale", "precision"))
def triangle_attention_jax_fwd(
    q: jax.Array,  # [B, N, H, S_qo, D]
    k: jax.Array,  # [B, N, H, S_kv, D]
    v: jax.Array,  # [B, N, H, S_kv, D]
    mask: jax.Array,  # [B, N, 1, 1, S_kv] boolean
    bias: jax.Array,  # [B, 1, H, S_qo, S_kv]
    scale: float,
    precision: jax.lax.Precision | None = None,
) -> jax.Array:  # [B, N, H, S_qo, D]
    r"""JAX reference implementation for triangle attention.

    Args:
        q: Query tensor of shape [B, N, H, S_qo, D].
        k: Key tensor of shape [B, N, H, S_kv, D].
        v: Value tensor of shape [B, N, H, S_kv, D].
        mask: Mask tensor of shape [B, N, 1, 1, S_kv] (boolean, True means valid).
        bias: Bias tensor of shape [B, 1, H, S_qo, S_kv].
        scale: Scaling factor for the dot product.
        precision: Precision for the computation (default is None).

    Returns:
        A tuple containing the attention output, log-sum-exp, and maximum value.

    .. math::

        \text{Attention}_a(Q, K, V, M, T) = \sum_b \text{softmax}_b(M_b ? -10^9 : (Q_a K_b + T_{ab})) V_b

    where :math:`Q`, :math:`K`, and :math:`V` are the query, key, and value tensors,
    :math:`M` is the mask bias, and :math:`T` is the triangle bias.
    """
    dtype = q.dtype
    assert k.dtype == dtype and v.dtype == dtype

    q = scale * q
    a = jnp.einsum("...ai,...bi->...ab", q, k, precision=precision)
    a = a + bias
    a = jnp.where(mask, a, -1e9)

    a = a.astype(jnp.float32)  # [B, N, H, S_qo, S_kv]
    amax = jnp.max(a, axis=-1, keepdims=True)
    lse = jax.scipy.special.logsumexp(a - amax, axis=-1, keepdims=True)
    a = jnp.exp(a - amax - lse)

    a = a.astype(dtype)
    a = jnp.einsum(
        "...ab, ...bi -> ...ai", a, v, precision=precision
    )  # [B, N, H, S_qo, D]

    return a, lse, amax


def triangle_attention_cuda_fwd(
    q: jax.Array,  # [B, N, H, S_qo, D]
    k: jax.Array,  # [B, N, H, S_kv, D]
    v: jax.Array,  # [B, N, H, S_kv, D]
    mask: jax.Array,  # [B, N, 1, 1, S_kv] boolean
    bias: jax.Array,  # [B, 1, H, S_qo, S_kv]
    scale: float,
    precision: jax.lax.Precision | None = None,
) -> tuple[jax.Array, jax.Array, jax.Array]:
    """CUDA implementation for the forward pass of triangle attention."""
    (B, N, H, S_qo, D) = q.shape
    assert k.shape[3] == v.shape[3], "Key and value sequence lengths must match"
    S_kv = k.shape[3]

    dtype = q.dtype

    assert q.shape == (B, N, H, S_qo, D)
    assert q.dtype == dtype

    assert k.shape == (B, N, H, S_kv, D)
    assert k.dtype == dtype

    assert v.shape == (B, N, H, S_kv, D)
    assert v.dtype == dtype

    assert mask.shape == (B, N, 1, 1, S_kv)
    assert mask.dtype == jnp.bool_

    assert bias.shape == (B, 1, H, S_qo, S_kv)

    # Determine if FP32 bias is needed using needs_fp32_bias_fwd
    # Pass stream_id=0 (nullptr) - the function will check device capability
    needs_fp32 = needs_fp32_bias_fwd(_dtype(dtype), D, S_kv, 0)

    # Convert bias to the expected dtype
    if needs_fp32:
        bias_converted = bias.astype(jnp.float32)
    else:
        bias_converted = bias.astype(dtype)

    sm = jax.ShapeDtypeStruct((B, N, H, S_qo, 1), jnp.float32)
    actual_s_kv = jax.ShapeDtypeStruct((B, N), jnp.int32)

    call = ffi.ffi_call("triangle_attention_cuda_fwd", (q, sm, sm, actual_s_kv))

    o, softmax_lse, softmax_max, _ = call(
        q,
        k,
        v,
        mask.astype(jnp.uint8),
        bias_converted,
        scale=scale,
        use_tf32=use_tf32(precision, dtype),
        bias_is_fp32=needs_fp32,
    )
    return o, softmax_lse, softmax_max


def triangle_attention_cuda_bwd(
    do: jax.Array,  # [B, N, H, S_qo, D] gradient of output
    o: jax.Array,  # [B, N, H, S_qo, D] output
    softmax_lse: jax.Array,  # [B, N, H, S_qo, 1] log-sum-exp
    q: jax.Array,  # [B, N, H, S_qo, D]
    k: jax.Array,  # [B, N, H, S_kv, D]
    v: jax.Array,  # [B, N, H, S_kv, D]
    mask: jax.Array,  # [B, N, 1, 1, S_kv] boolean
    bias: jax.Array,  # [B, 1, H, S_qo, S_kv]
    scale: float,
    precision: jax.lax.Precision | None = None,
) -> tuple[jax.Array, jax.Array, jax.Array, jax.Array]:
    """CUDA implementation for the backward pass of triangle attention."""
    dtype = q.dtype
    (B, N, H, S_qo, D) = q.shape
    assert k.shape[3] == v.shape[3], "Key and value sequence lengths must match"
    S_kv = k.shape[3]

    assert do.shape == (B, N, H, S_qo, D)
    assert do.dtype == dtype

    assert o.shape == (B, N, H, S_qo, D)
    assert o.dtype == dtype

    assert softmax_lse.shape == (B, N, H, S_qo, 1)
    assert softmax_lse.dtype == jnp.float32

    assert q.shape == (B, N, H, S_qo, D)
    assert q.dtype == dtype

    assert k.shape == (B, N, H, S_kv, D)
    assert k.dtype == dtype

    assert v.shape == (B, N, H, S_kv, D)
    assert v.dtype == dtype

    assert mask.shape == (B, N, 1, 1, S_kv)
    assert mask.dtype == jnp.bool_

    assert bias.shape == (B, 1, H, S_qo, S_kv)

    # Determine if FP32 bias is needed using needs_fp32_bias_bwd
    # Pass stream_id=0 (nullptr) - the function will check device capability
    # has_dbias_fp32_buf=True because we always provide dbias_fp32_buf workspace buffer
    needs_fp32 = needs_fp32_bias_bwd(_dtype(dtype), D, True, 0)

    # Convert bias to the expected dtype
    if needs_fp32:
        bias_converted = bias.astype(jnp.float32)
    else:
        bias_converted = bias.astype(dtype)

    dq = jax.ShapeDtypeStruct((B, N, H, S_qo, D), q.dtype)
    dk = jax.ShapeDtypeStruct((B, N, H, S_kv, D), k.dtype)
    dv = jax.ShapeDtypeStruct((B, N, H, S_kv, D), v.dtype)
    # Create single dbias buffer with appropriate dtype based on needs_fp32
    dbias_dtype = jnp.float32 if needs_fp32 else dtype
    dbias = jax.ShapeDtypeStruct((B, 1, H, S_qo, S_kv), dbias_dtype)
    do_o_dot = jax.ShapeDtypeStruct((B, N, H, S_qo, 1), jnp.float32)
    if dq.dtype == jnp.float32:
        dq_fp32_buf = jax.ShapeDtypeStruct((0,), jnp.float32)
    else:
        dq_fp32_buf = jax.ShapeDtypeStruct(dq.shape, jnp.float32)

    # dbias_fp32_buf is workspace buffer for SM100 kernel (padded sizes)
    # tile_n = 64, tile_m = 128
    tile_n = 64
    tile_m = 128
    padded_s_q = ((S_qo + tile_n - 1) // tile_n) * tile_n
    padded_s_kv = ((S_kv + tile_m - 1) // tile_m) * tile_m
    dbias_fp32_buf = jax.ShapeDtypeStruct(
        (B, 1, H, padded_s_q, padded_s_kv), jnp.float32
    )

    call = ffi.ffi_call(
        "triangle_attention_cuda_bwd",
        (
            dq,
            dk,
            dv,
            dbias,
            do_o_dot,
            dq_fp32_buf,
            dbias_fp32_buf,
        ),
    )
    dq, dk, dv, dbias, _, _, _ = call(
        do,
        o,
        softmax_lse,
        q,
        k,
        v,
        mask.astype(jnp.uint8),
        bias_converted,
        scale=scale,
        use_tf32=use_tf32(precision, dtype),
        bias_is_fp32=needs_fp32,
    )

    return dq, dk, dv, dbias
