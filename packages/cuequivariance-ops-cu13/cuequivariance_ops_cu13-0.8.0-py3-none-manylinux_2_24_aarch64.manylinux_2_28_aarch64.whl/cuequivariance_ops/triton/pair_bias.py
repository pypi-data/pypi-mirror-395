# SPDX-FileCopyrightText: Copyright (c) 2024 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: LicenseRef-NvidiaProprietary
#
# NVIDIA CORPORATION, its affiliates and licensors retain all intellectual
# property and proprietary rights in and to this material, related
# documentation and any modifications thereto. Any use, reproduction,
# disclosure or distribution of this material and related documentation
# without an express license agreement from NVIDIA CORPORATION or
# its affiliates is strictly prohibited.

import triton
import triton.language as tl


@triton.jit
def pair_bias_norm_linear_mask_forward_kernel(
    z_ptr,
    mask_ptr,
    w_proj_z_ptr,
    b_proj_z_ptr,
    w_ln_ptr,
    b_ln_ptr,
    U,
    V,
    multiplicity,
    out_mask_ptr,
    z_norm_ptr,
    z_proj_ptr,
    mean_ptr,
    rstd_ptr,
    TILE_V: tl.constexpr,
    TILE_K: tl.constexpr,
    NUM_HEADS: tl.constexpr,
    NUM_HEADS_PER_BLK: tl.constexpr,
    DIM_Z: tl.constexpr,
    INF: tl.constexpr,
    EPS: tl.constexpr,
    ELEMENTWISE_AFFINE: tl.constexpr,
    IS_TRAINING: tl.constexpr,
    HAS_BIAS: tl.constexpr,
    MASK_WITH_MULTIPLICITY: tl.constexpr,
    CACHE_Z_PROJ: tl.constexpr = False,
    NEEDS_INT64: tl.constexpr = True,
):
    # prepare single mask
    # z: B x U x V x D -> z' B x H x U x V
    # mask: B x V
    # out_mask = z' + (1 - mask) * inf

    pid_v = tl.program_id(0)
    pid_u = tl.program_id(1)

    if NEEDS_INT64:
        pid_u = tl.cast(pid_u, tl.int64)
        pid_v = tl.cast(pid_v, tl.int64)
        U = tl.cast(U, tl.int64)
        V = tl.cast(V, tl.int64)

    head_batch_idx = tl.program_id(2)
    NUM_HEAD_BLKS = tl.cdiv(NUM_HEADS, NUM_HEADS_PER_BLK)
    batch_idx = head_batch_idx // NUM_HEAD_BLKS
    head_idx = head_batch_idx % NUM_HEAD_BLKS

    stride_vz = V * DIM_Z
    stride_uv = U * V
    stride_uvz = U * V * DIM_Z

    offs_u = pid_u
    offs_v = pid_v * TILE_V + tl.arange(0, TILE_V)
    offs_k = tl.arange(0, TILE_K)
    offs_z = tl.arange(0, DIM_Z)
    mask_v = offs_v < V
    offs_head = head_idx * NUM_HEADS_PER_BLK + tl.arange(0, NUM_HEADS_PER_BLK)
    mask_head = offs_head < NUM_HEADS

    z_ptrs = z_ptr + batch_idx * stride_uvz + offs_u * stride_vz
    z_ptrs += offs_v[:, None] * DIM_Z + offs_z[None, :]

    z_tile_full = tl.load(z_ptrs, mask=mask_v[:, None], other=0.0).to(tl.float32)

    mean = tl.sum(z_tile_full, axis=1) / DIM_Z
    rstd = z_tile_full - mean[:, None]
    rstd = rstd * rstd
    rstd = tl.sum(rstd, axis=1) / DIM_Z
    rstd = tl.rsqrt(rstd + EPS)

    if IS_TRAINING:
        mean_ptrs = mean_ptr + batch_idx * stride_uv
        mean_ptrs += offs_u * V + offs_v
        tl.store(mean_ptrs, mean, mask=mask_v)

        rstd_ptrs = rstd_ptr + batch_idx * stride_uv
        rstd_ptrs += offs_u * V + offs_v
        tl.store(rstd_ptrs, rstd, mask=mask_v)

    z_ptrs = z_ptr + batch_idx * stride_uvz + offs_u * stride_vz
    z_ptrs += offs_v[:, None] * DIM_Z + offs_k[None, :]
    w_ln_ptrs = w_ln_ptr + offs_k
    b_ln_ptrs = b_ln_ptr + offs_k
    w_proj_ptrs = w_proj_z_ptr + (offs_head[None, :] * DIM_Z + offs_k[:, None])

    if IS_TRAINING:
        z_norm_ptrs = z_norm_ptr + batch_idx * stride_uvz + offs_u * stride_vz
        z_norm_ptrs += offs_v[:, None] * DIM_Z + offs_k[None, :]

    num_tiles_k = DIM_Z // TILE_K
    acc = tl.zeros((TILE_V, NUM_HEADS_PER_BLK), dtype=tl.float32)

    for _ in range(0, num_tiles_k):
        z_tile = tl.load(z_ptrs, mask=mask_v[:, None], other=0.0).to(tl.float32)
        z_tile = (z_tile - mean[:, None]) * rstd[:, None]

        if ELEMENTWISE_AFFINE:
            w_ln_tile = tl.load(w_ln_ptrs).to(tl.float32)
            b_ln_tile = tl.load(b_ln_ptrs).to(tl.float32)
            z_tile = z_tile * w_ln_tile + b_ln_tile

        if IS_TRAINING:
            tl.store(z_norm_ptrs, z_tile, mask=mask_v[:, None])

        w_tile = tl.load(w_proj_ptrs, mask=mask_head[None, :], other=0.0).to(tl.float32)

        acc = tl.dot(z_tile, w_tile, acc, input_precision="tf32x3")

        z_ptrs += TILE_K
        w_proj_ptrs += TILE_K
        if ELEMENTWISE_AFFINE:
            w_ln_ptrs += TILE_K
            b_ln_ptrs += TILE_K
        if IS_TRAINING:
            z_norm_ptrs += TILE_K

    if HAS_BIAS:
        b_proj_ptrs = b_proj_z_ptr + offs_head
        b_proj_tile = tl.load(b_proj_ptrs, mask=mask_head, other=0.0).to(tl.float32)
        acc += b_proj_tile[None, :]

    offs_v = pid_v * TILE_V + tl.arange(0, TILE_V)
    mask_v = offs_v < V
    offs_head = head_idx * NUM_HEADS_PER_BLK + tl.arange(0, NUM_HEADS_PER_BLK)
    mask_head = offs_head < NUM_HEADS

    if CACHE_Z_PROJ:
        z_proj_ptrs = z_proj_ptr + batch_idx * NUM_HEADS * stride_uv
        z_proj_ptrs += offs_u * V
        z_proj_ptrs += offs_head[None, :] * stride_uv + offs_v[:, None]
        mask_z = mask_head[None, :] & mask_v[:, None]
        tl.store(z_proj_ptrs, acc, mask=mask_z)

    out_mask_ptrs = out_mask_ptr + batch_idx * multiplicity * NUM_HEADS * stride_uv
    out_mask_ptrs += offs_u * V
    out_mask_ptrs += offs_head[None, :] * stride_uv + offs_v[:, None]
    mask_o = mask_head[None, :] & mask_v[:, None]

    if MASK_WITH_MULTIPLICITY:
        mask_ptrs = mask_ptr + batch_idx * multiplicity * V + offs_v

        for _ in range(multiplicity):
            mask_tile = tl.load(mask_ptrs, mask=mask_v, other=0.0).to(tl.float32)
            out_tile = acc + (1.0 - mask_tile[:, None]) * (-INF)
            tl.store(out_mask_ptrs, out_tile, mask=mask_o)

            out_mask_ptrs += NUM_HEADS * stride_uv
            mask_ptrs += V

    else:
        mask_ptrs = mask_ptr + batch_idx * V + offs_v
        mask_tile = tl.load(mask_ptrs, mask=mask_v, other=0.0).to(tl.float32)

        for _ in range(multiplicity):
            out_tile = acc + (1.0 - mask_tile[:, None]) * (-INF)
            tl.store(out_mask_ptrs, out_tile, mask=mask_o)

            out_mask_ptrs += NUM_HEADS * stride_uv
            mask_ptrs += V


@triton.jit
def pair_bias_linear_mask_forward_kernel(
    z_ptr,
    mask_ptr,
    w_proj_z_ptr,
    b_proj_z_ptr,
    U,
    V,
    multiplicity,
    out_mask_ptr,
    z_proj_ptr,
    TILE_V: tl.constexpr,
    TILE_K: tl.constexpr,
    NUM_HEADS: tl.constexpr,
    NUM_HEADS_PER_BLK: tl.constexpr,
    DIM_Z: tl.constexpr,
    INF: tl.constexpr,
    HAS_BIAS: tl.constexpr,
    MASK_WITH_MULTIPLICITY: tl.constexpr,
    CACHE_Z_PROJ: tl.constexpr = False,
    NEEDS_INT64: tl.constexpr = True,
):
    # prepare single mask
    # z: B x U x V x D -> z' B x H x U x V
    # mask: B x V
    # out_mask = z' + (1 - mask) * inf

    pid_v = tl.program_id(0)
    pid_u = tl.program_id(1)

    if NEEDS_INT64:
        pid_u = tl.cast(pid_u, tl.int64)
        pid_v = tl.cast(pid_v, tl.int64)
        U = tl.cast(U, tl.int64)
        V = tl.cast(V, tl.int64)

    head_batch_idx = tl.program_id(2)
    NUM_HEAD_BLKS = tl.cdiv(NUM_HEADS, NUM_HEADS_PER_BLK)
    batch_idx = head_batch_idx // NUM_HEAD_BLKS
    head_idx = head_batch_idx % NUM_HEAD_BLKS

    stride_vz = V * DIM_Z
    stride_uv = U * V
    stride_uvz = U * V * DIM_Z

    offs_u = pid_u
    offs_v = pid_v * TILE_V + tl.arange(0, TILE_V)
    offs_k = tl.arange(0, TILE_K)
    mask_v = offs_v < V
    offs_head = head_idx * NUM_HEADS_PER_BLK + tl.arange(0, NUM_HEADS_PER_BLK)
    mask_head = offs_head < NUM_HEADS

    z_ptrs = z_ptr + batch_idx * stride_uvz + offs_u * stride_vz
    z_ptrs += offs_v[:, None] * DIM_Z + offs_k[None, :]

    w_ptrs = w_proj_z_ptr + (offs_head[None, :] * DIM_Z + offs_k[:, None])

    acc = tl.zeros((TILE_V, NUM_HEADS_PER_BLK), dtype=tl.float32)

    for _ in range(0, DIM_Z // TILE_K):
        z_tile = tl.load(z_ptrs, mask=mask_v[:, None], other=0.0).to(tl.float32)
        w_tile = tl.load(w_ptrs, mask=mask_head[None, :], other=0.0).to(tl.float32)

        acc = tl.dot(z_tile, w_tile, acc, input_precision="tf32x3")

        z_ptrs += TILE_K
        w_ptrs += TILE_K

    if HAS_BIAS:
        b_proj_ptrs = b_proj_z_ptr + offs_head
        b_proj_tile = tl.load(b_proj_ptrs, mask=mask_head, other=0.0)
        acc += b_proj_tile[None, :]

    offs_v = pid_v * TILE_V + tl.arange(0, TILE_V)
    mask_v = offs_v < V
    offs_head = head_idx * NUM_HEADS_PER_BLK + tl.arange(0, NUM_HEADS_PER_BLK)
    mask_head = offs_head < NUM_HEADS

    if CACHE_Z_PROJ:
        z_proj_ptrs = z_proj_ptr + batch_idx * NUM_HEADS * stride_uv
        z_proj_ptrs += offs_u * V
        z_proj_ptrs += offs_head[None, :] * stride_uv + offs_v[:, None]
        mask_z = mask_head[None, :] & mask_v[:, None]
        tl.store(z_proj_ptrs, acc, mask=mask_z)

    out_mask_ptrs = out_mask_ptr + batch_idx * multiplicity * NUM_HEADS * stride_uv
    out_mask_ptrs += offs_u * V
    out_mask_ptrs += offs_head[None, :] * stride_uv + offs_v[:, None]
    mask_o = mask_head[None, :] & mask_v[:, None]

    if MASK_WITH_MULTIPLICITY:
        mask_ptrs = mask_ptr + batch_idx * multiplicity * V + offs_v

        for _ in range(multiplicity):
            mask_tile = tl.load(mask_ptrs, mask=mask_v, other=0.0).to(tl.float32)
            out_tile = acc + (1.0 - mask_tile[:, None]) * (-INF)
            tl.store(out_mask_ptrs, out_tile, mask=mask_o)

            out_mask_ptrs += NUM_HEADS * stride_uv
            mask_ptrs += V

    else:
        mask_ptrs = mask_ptr + batch_idx * V + offs_v
        mask_tile = tl.load(mask_ptrs, mask=mask_v, other=0.0).to(tl.float32)

        for _ in range(multiplicity):
            out_tile = acc + (1.0 - mask_tile[:, None]) * (-INF)
            tl.store(out_mask_ptrs, out_tile, mask=mask_o)

            out_mask_ptrs += NUM_HEADS * stride_uv
            mask_ptrs += V


@triton.jit
def pair_bias_mask_forward_kernel(
    z_proj_ptr,
    mask_ptr,
    U,
    V,
    multiplicity,
    out_mask_ptr,
    TILE_V: tl.constexpr,
    NUM_HEADS: tl.constexpr,
    NUM_HEADS_PER_BLK: tl.constexpr,
    INF: tl.constexpr,
    MASK_WITH_MULTIPLICITY: tl.constexpr,
    NEEDS_INT64: tl.constexpr = True,
):
    # prepare single mask
    # z: z' B x H x U x V
    # mask: B x V
    # out_mask = z' + (1 - mask) * inf

    pid_v = tl.program_id(0)
    pid_u = tl.program_id(1)

    if NEEDS_INT64:
        pid_u = tl.cast(pid_u, tl.int64)
        pid_v = tl.cast(pid_v, tl.int64)
        U = tl.cast(U, tl.int64)
        V = tl.cast(V, tl.int64)

    head_batch_idx = tl.program_id(2)
    NUM_HEAD_BLKS = tl.cdiv(NUM_HEADS, NUM_HEADS_PER_BLK)
    batch_idx = head_batch_idx // NUM_HEAD_BLKS
    head_idx = head_batch_idx % NUM_HEAD_BLKS

    stride_uv = U * V
    stride_uvh = U * V * NUM_HEADS

    offs_u = pid_u
    offs_v = pid_v * TILE_V + tl.arange(0, TILE_V)
    mask_v = offs_v < V
    offs_head = head_idx * NUM_HEADS_PER_BLK + tl.arange(0, NUM_HEADS_PER_BLK)
    mask_head = offs_head < NUM_HEADS

    z_proj_ptrs = z_proj_ptr + batch_idx * stride_uvh + offs_u * V
    z_proj_ptrs += offs_head[:, None] * stride_uv + offs_v[None, :]

    mask_zo = mask_v[None, :] & mask_head[:, None]

    z_proj_tile = tl.load(z_proj_ptrs, mask=mask_zo, other=0.0).to(tl.float32)

    out_mask_ptrs = out_mask_ptr + batch_idx * multiplicity * NUM_HEADS * stride_uv
    out_mask_ptrs += offs_u * V
    out_mask_ptrs += offs_head[:, None] * stride_uv + offs_v[None, :]

    if MASK_WITH_MULTIPLICITY:
        mask_ptrs = mask_ptr + batch_idx * multiplicity * V + offs_v

        for _ in range(multiplicity):
            mask_tile = tl.load(mask_ptrs, mask=mask_v, other=0.0).to(tl.float32)
            out_tile = z_proj_tile + (1.0 - mask_tile[None, :]) * (-INF)
            tl.store(out_mask_ptrs, out_tile, mask=mask_zo)

            out_mask_ptrs += NUM_HEADS * stride_uv
            mask_ptrs += V

    else:
        mask_ptrs = mask_ptr + batch_idx * V + offs_v
        mask_tile = tl.load(mask_ptrs, mask=mask_v, other=0.0).to(tl.float32)

        for _ in range(multiplicity):
            out_tile = z_proj_tile + (1.0 - mask_tile[None, :]) * (-INF)
            tl.store(out_mask_ptrs, out_tile, mask=mask_zo)

            out_mask_ptrs += NUM_HEADS * stride_uv
            mask_ptrs += V
