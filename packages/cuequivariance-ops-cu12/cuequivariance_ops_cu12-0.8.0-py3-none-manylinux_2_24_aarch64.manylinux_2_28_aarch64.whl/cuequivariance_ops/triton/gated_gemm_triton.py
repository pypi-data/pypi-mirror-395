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

from cuequivariance_ops.triton.utils import cvt_tf32_rn


@triton.jit
def fused_sigmoid_gated_dual_gemm_forward_kernel(
    # inputs
    x1_ptr,
    x2_ptr,
    w1_ptr,
    w2_ptr,
    b1_ptr,
    b2_ptr,
    mask_ptr,
    M,
    N,
    K,
    # outputs
    o_ptr,
    TILE_M: tl.constexpr,
    TILE_N: tl.constexpr,
    TILE_K: tl.constexpr,
    PRECISION: tl.constexpr,
    APPLY_MASK: tl.constexpr,
    TRANSPOSE_OUT: tl.constexpr,
    TWO_INPUTS: tl.constexpr,
    HAS_B1: tl.constexpr,
    HAS_B2: tl.constexpr,
    NEEDS_INT64: tl.constexpr = True,
):
    # fully gated GEMM kernel with optional mask at the end
    pid_m = tl.program_id(axis=0)
    pid_n = tl.program_id(axis=1)

    if NEEDS_INT64:
        pid_m = tl.cast(pid_m, tl.int64)
        pid_n = tl.cast(pid_n, tl.int64)
        M = tl.cast(M, tl.int64)
        N = tl.cast(N, tl.int64)

    start_m = pid_m * TILE_M
    start_n = pid_n * TILE_N

    offs_xm = start_m + tl.arange(0, TILE_M)
    offs_wn = start_n + tl.arange(0, TILE_N)
    offs_k = tl.arange(0, TILE_K)

    x1_ptrs = x1_ptr + (offs_xm[:, None] * K + offs_k[None, :])
    if TWO_INPUTS:
        x2_ptrs = x2_ptr + (offs_xm[:, None] * K + offs_k[None, :])

    w_tile_offs = offs_wn[None, :] * K + offs_k[:, None]

    acc_1 = tl.zeros((TILE_M, TILE_N), dtype=tl.float32)
    acc_2 = tl.zeros((TILE_M, TILE_N), dtype=tl.float32)

    mask_m = offs_xm < M

    if TWO_INPUTS:
        for _ in range(0, tl.cdiv(K, TILE_K)):
            x1 = tl.load(x1_ptrs, mask=mask_m[:, None], other=0.0).to(
                w1_ptr.type.element_ty
            )
            w1_ptrs = w1_ptr + w_tile_offs
            w1 = tl.load(w1_ptrs)
            if PRECISION == 0:
                acc_1 = tl.dot(x1, w1, acc_1)
            elif PRECISION == 1:
                x1 = cvt_tf32_rn(x1)
                w1 = cvt_tf32_rn(w1)
                acc_1 = tl.dot(x1, w1, acc_1, input_precision="tf32")
            elif PRECISION == 2:
                acc_1 = tl.dot(x1, w1, acc_1, input_precision="tf32x3")
            elif PRECISION == 3:
                acc_1 = tl.dot(x1, w1, acc_1, input_precision="ieee")
            else:
                tl.static_assert(
                    False,
                    "PRECISION must be 0 (default), 1 (tf32), 2 (tf32x3) or 3 (ieee)",
                )

            x1_ptrs += TILE_K
            w1_ptr += TILE_K

        for _ in range(0, tl.cdiv(K, TILE_K)):
            x2 = tl.load(x2_ptrs, mask=mask_m[:, None], other=0.0).to(
                w2_ptr.type.element_ty
            )
            w2_ptrs = w2_ptr + w_tile_offs
            w2 = tl.load(w2_ptrs)
            if PRECISION == 0:
                acc_2 = tl.dot(x2, w2, acc_2)
            elif PRECISION == 1:
                x2 = cvt_tf32_rn(x2)
                w2 = cvt_tf32_rn(w2)
                acc_2 = tl.dot(x2, w2, acc_2, input_precision="tf32")
            elif PRECISION == 2:
                acc_2 = tl.dot(x2, w2, acc_2, input_precision="tf32x3")
            elif PRECISION == 3:
                acc_2 = tl.dot(x2, w2, acc_2, input_precision="ieee")
            else:
                tl.static_assert(
                    False,
                    "PRECISION must be 0 (default), 1 (tf32), 2 (tf32x3) or 3 (ieee)",
                )

            x2_ptrs += TILE_K
            w2_ptr += TILE_K

    else:
        for _ in range(0, tl.cdiv(K, TILE_K)):
            x = tl.load(x1_ptrs, mask=mask_m[:, None], other=0.0).to(
                w1_ptr.type.element_ty
            )

            w1_ptrs = w1_ptr + w_tile_offs
            w1 = tl.load(w1_ptrs)
            if PRECISION == 0:
                acc_1 = tl.dot(x, w1, acc_1)
            elif PRECISION == 1:
                x = cvt_tf32_rn(x)
                w1 = cvt_tf32_rn(w1)
                acc_1 = tl.dot(x, w1, acc_1, input_precision="tf32")
            elif PRECISION == 2:
                acc_1 = tl.dot(x, w1, acc_1, input_precision="tf32x3")
            elif PRECISION == 3:
                acc_1 = tl.dot(x, w1, acc_1, input_precision="ieee")
            else:
                tl.static_assert(
                    False,
                    "PRECISION must be 0 (default), 1 (tf32), 2 (tf32x3) or 3 (ieee)",
                )

            w2_ptrs = w2_ptr + w_tile_offs
            w2 = tl.load(w2_ptrs)
            if PRECISION == 0:
                acc_2 = tl.dot(x, w2, acc_2)
            elif PRECISION == 1:
                x = cvt_tf32_rn(x)
                w2 = cvt_tf32_rn(w2)
                acc_2 = tl.dot(x, w2, acc_2, input_precision="tf32")
            elif PRECISION == 2:
                acc_2 = tl.dot(x, w2, acc_2, input_precision="tf32x3")
            elif PRECISION == 3:
                acc_2 = tl.dot(x, w2, acc_2, input_precision="ieee")
            else:
                tl.static_assert(
                    False,
                    "PRECISION must be 0 (default), 1 (tf32), 2 (tf32x3) or 3 (ieee)",
                )

            x1_ptrs += TILE_K
            w1_ptr += TILE_K
            w2_ptr += TILE_K

    offs_om = pid_m * TILE_M + tl.arange(0, TILE_M)
    offs_on = pid_n * TILE_N + tl.arange(0, TILE_N)

    if HAS_B1:
        b1_ptrs = b1_ptr + offs_on
        b1_tile = tl.load(b1_ptrs).to(tl.float32)
        acc_1 += b1_tile

    if HAS_B2:
        b2_ptrs = b2_ptr + offs_on
        b2_tile = tl.load(b2_ptrs).to(tl.float32)
        acc_2 += b2_tile

    acc_1 = 1.0 / (1.0 + tl.exp(-acc_1))
    acc_gated = acc_1 * acc_2

    if APPLY_MASK:
        mask = tl.load(mask_ptr + offs_om, mask=mask_m, other=0.0).to(tl.float32)
        acc_gated = acc_gated * mask[:, None]

    if TRANSPOSE_OUT:
        o_ptrs = o_ptr + offs_on[None, :] * M + offs_om[:, None]
    else:
        o_ptrs = o_ptr + offs_om[:, None] * N + offs_on[None, :]

    o_mask = offs_om[:, None] < M
    tl.store(o_ptrs, acc_gated, mask=o_mask)


@triton.jit
def fused_sigmoid_gated_dual_gemm_backward_pregemm_kernel(
    # inputs
    grad_o_ptr,
    x1_ptr,
    x2_ptr,
    w1_ptr,
    w2_ptr,
    b1_ptr,
    b2_ptr,
    mask_ptr,
    M,
    N,
    K,
    # outputs
    grad_xw1_ptr,
    grad_xw2_ptr,
    grad_mask_ptr,
    TILE_M: tl.constexpr,
    TILE_N: tl.constexpr,
    TILE_K: tl.constexpr,
    PRECISION: tl.constexpr,
    APPLY_MASK: tl.constexpr,
    TRANSPOSE_OUT: tl.constexpr,
    TWO_INPUTS: tl.constexpr,
    HAS_B1: tl.constexpr,
    HAS_B2: tl.constexpr,
    NEEDS_INT64: tl.constexpr = True,
):
    # fully gated GEMM kernel with optional mask at the end
    pid_m = tl.program_id(axis=0)
    pid_n = tl.program_id(axis=1)

    if NEEDS_INT64:
        pid_m = tl.cast(pid_m, tl.int64)
        pid_n = tl.cast(pid_n, tl.int64)
        M = tl.cast(M, tl.int64)
        N = tl.cast(N, tl.int64)

    start_m = pid_m * TILE_M
    start_n = pid_n * TILE_N

    offs_xm = start_m + tl.arange(0, TILE_M)
    offs_wn = start_n + tl.arange(0, TILE_N)
    offs_k = tl.arange(0, TILE_K)

    x1_ptrs = x1_ptr + (offs_xm[:, None] * K + offs_k[None, :])
    if TWO_INPUTS:
        x2_ptrs = x2_ptr + (offs_xm[:, None] * K + offs_k[None, :])
    w_tile_offs = offs_wn[None, :] * K + offs_k[:, None]

    acc_1 = tl.zeros((TILE_M, TILE_N), dtype=tl.float32)
    acc_2 = tl.zeros((TILE_M, TILE_N), dtype=tl.float32)

    mask_m = offs_xm < M

    if TWO_INPUTS:
        # recompute acc1 and acc2
        for _ in range(0, tl.cdiv(K, TILE_K)):
            x1 = tl.load(x1_ptrs, mask=mask_m[:, None], other=0.0).to(
                w1_ptr.type.element_ty
            )
            w1_ptrs = w1_ptr + w_tile_offs
            w1 = tl.load(w1_ptrs)

            if PRECISION == 0:
                acc_1 = tl.dot(x1, w1, acc_1)
            elif PRECISION == 1:
                x1 = cvt_tf32_rn(x1)
                w1 = cvt_tf32_rn(w1)
                acc_1 = tl.dot(x1, w1, acc_1, input_precision="tf32")
            elif PRECISION == 2:
                acc_1 = tl.dot(x1, w1, acc_1, input_precision="tf32x3")
            elif PRECISION == 3:
                acc_1 = tl.dot(x1, w1, acc_1, input_precision="ieee")
            else:
                tl.static_assert(
                    False,
                    "PRECISION must be 0 (default), 1 (tf32), 2 (tf32x3) or 3 (ieee)",
                )

            x1_ptrs += TILE_K
            w1_ptr += TILE_K

        for _ in range(0, tl.cdiv(K, TILE_K)):
            x2 = tl.load(x2_ptrs, mask=mask_m[:, None], other=0.0).to(
                w2_ptr.type.element_ty
            )
            w2_ptrs = w2_ptr + w_tile_offs
            w2 = tl.load(w2_ptrs)

            if PRECISION == 0:
                acc_2 = tl.dot(x2, w2, acc_2)
            elif PRECISION == 1:
                x2 = cvt_tf32_rn(x2)
                w2 = cvt_tf32_rn(w2)
                acc_2 = tl.dot(x2, w2, acc_2, input_precision="tf32")
            elif PRECISION == 2:
                acc_2 = tl.dot(x2, w2, acc_2, input_precision="tf32x3")
            elif PRECISION == 3:
                acc_2 = tl.dot(x2, w2, acc_2, input_precision="ieee")
            else:
                tl.static_assert(
                    False,
                    "PRECISION must be 0 (default), 1 (tf32), 2 (tf32x3) or 3 (ieee)",
                )

            x2_ptrs += TILE_K
            w2_ptr += TILE_K

    else:
        # recompute acc1 and acc2
        for _ in range(0, tl.cdiv(K, TILE_K)):
            x = tl.load(x1_ptrs, mask=mask_m[:, None], other=0.0).to(
                w1_ptr.type.element_ty
            )

            w1_ptrs = w1_ptr + w_tile_offs
            w1 = tl.load(w1_ptrs)
            if PRECISION == 0:
                acc_1 = tl.dot(x, w1, acc_1)
            elif PRECISION == 1:
                x = cvt_tf32_rn(x)
                w1 = cvt_tf32_rn(w1)
                acc_1 = tl.dot(x, w1, acc_1, input_precision="tf32")
            elif PRECISION == 2:
                acc_1 = tl.dot(x, w1, acc_1, input_precision="tf32x3")
            elif PRECISION == 3:
                acc_1 = tl.dot(x, w1, acc_1, input_precision="ieee")
            else:
                tl.static_assert(
                    False,
                    "PRECISION must be 0 (default), 1 (tf32), 2 (tf32x3) or 3 (ieee)",
                )

            w2_ptrs = w2_ptr + w_tile_offs
            w2 = tl.load(w2_ptrs)
            if PRECISION == 0:
                acc_2 = tl.dot(x, w2, acc_2)
            elif PRECISION == 1:
                x = cvt_tf32_rn(x)
                w2 = cvt_tf32_rn(w2)
                acc_2 = tl.dot(x, w2, acc_2, input_precision="tf32")
            elif PRECISION == 2:
                acc_2 = tl.dot(x, w2, acc_2, input_precision="tf32x3")
            elif PRECISION == 3:
                acc_2 = tl.dot(x, w2, acc_2, input_precision="ieee")
            else:
                tl.static_assert(
                    False,
                    "PRECISION must be 0 (default), 1 (tf32), 2 (tf32x3) or 3 (ieee)",
                )

            x1_ptrs += TILE_K
            w1_ptr += TILE_K
            w2_ptr += TILE_K

    offs_om = pid_m * TILE_M + tl.arange(0, TILE_M)
    offs_on = pid_n * TILE_N + tl.arange(0, TILE_N)

    if HAS_B1:
        b1_ptrs = b1_ptr + offs_on
        b1_tile = tl.load(b1_ptrs).to(tl.float32)
        acc_1 += b1_tile

    if HAS_B2:
        b2_ptrs = b2_ptr + offs_on
        b2_tile = tl.load(b2_ptrs).to(tl.float32)
        acc_2 += b2_tile

    if TRANSPOSE_OUT:
        grad_o_ptrs = grad_o_ptr + offs_on[None, :] * M + offs_om[:, None]
    else:
        grad_o_ptrs = grad_o_ptr + offs_om[:, None] * N + offs_on[None, :]

    grad_o = tl.load(grad_o_ptrs, mask=mask_m[:, None], other=0.0).to(tl.float32)

    acc_sig = 1.0 / (1.0 + tl.exp(-acc_1))

    if APPLY_MASK:
        tmp = acc_sig * acc_2
        grad_mask = grad_o * tmp
        grad_mask = tl.sum(grad_mask, axis=1)
        grad_mask_ptrs = grad_mask_ptr + pid_n * M + offs_om
        tl.store(grad_mask_ptrs, grad_mask, mask=mask_m)

        mask = tl.load(mask_ptr + offs_om, mask=mask_m, other=0.0).to(tl.float32)
        grad_o = grad_o * mask[:, None]

    grad_xw2 = grad_o * acc_sig
    grad_xw2_ptrs = grad_xw2_ptr + offs_om[:, None] * N + offs_on[None, :]
    tl.store(grad_xw2_ptrs, grad_xw2, mask=mask_m[:, None])

    tmp = (1.0 - acc_sig) * acc_sig
    grad_xw1 = grad_o * acc_2 * tmp
    grad_xw1_ptrs = grad_xw1_ptr + offs_om[:, None] * N + offs_on[None, :]
    tl.store(grad_xw1_ptrs, grad_xw1, mask=mask_m[:, None])
