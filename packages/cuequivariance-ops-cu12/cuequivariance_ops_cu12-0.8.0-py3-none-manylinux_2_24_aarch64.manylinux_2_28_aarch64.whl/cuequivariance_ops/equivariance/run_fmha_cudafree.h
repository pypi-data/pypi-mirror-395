/*
 * SPDX-FileCopyrightText: Copyright (c) 2025 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
 * SPDX-License-Identifier: LicenseRef-NvidiaProprietary
 *
 * NVIDIA CORPORATION, its affiliates and licensors retain all intellectual
 * property and proprietary rights in and to this material, related
 * documentation and any modifications thereto. Any use, reproduction,
 * disclosure or distribution of this material and related documentation
 * without an express license agreement from NVIDIA CORPORATION or
 * its affiliates is strictly prohibited.
 */
#ifndef CUDNN_FMHA_RUN_FMHA_CUDAFREE_H
#define CUDNN_FMHA_RUN_FMHA_CUDAFREE_H

#include <cstdint>  // for uint32_t
#include <optional>

namespace cudnn_fmha {
using DType = void;

enum class Datatype : uint32_t {
  kFloat32  = 0,
  kFloat64  = 1,
  kFloat16  = 2,
  kBFloat16 = 3,
  kInt32    = 4,
  kInt64    = 5
};

__attribute__((visibility("default"))) void run_fmha_for_dtype(
  Datatype dtype,
  DType* q_ptr,              // [B, N, H, S_qo, D]
  DType* k_ptr,              // [B, N, H, S_kv, D]
  DType* v_ptr,              // [B, N, H, S_kv, D]
  DType* o_ptr,              // [B, N, H, S_qo, D] output
  bool* mask_bias_ptr,       // [B, N, 1, 1, S_kv]
  float* triangle_bias_ptr,  // [B, 1, H, S_qo, S_kv]
  float* softmax_lse_ptr,    // [B, N, H, S_qo, 1] output
  float* softmax_max_ptr,    // [B, N, H, S_qo, 1] output
  const uint32_t B,
  const uint32_t I,
  const uint32_t H,
  const uint32_t S_qo,
  const uint32_t S_kv,
  const uint32_t D,
  const float bmm_scale,
  bool use_tf32,
  void* stream = nullptr);

__attribute__((visibility("default"))) void run_fmha_bwd_for_dtype(
  Datatype dtype,
  DType* do_ptr,              // [B, N, H, S_qo, D]
  DType* o_ptr,               // [B, N, H, S_qo, D]
  float* softmax_lse_ptr,     // [B, N, H, S_qo, 1]
  DType* q_ptr,               // [B, N, H, S_qo, D]
  DType* k_ptr,               // [B, N, H, S_kv, D]
  DType* v_ptr,               // [B, N, H, S_kv, D]
  bool* mask_bias_ptr,        // [B, N, 1, 1, S_kv]
  float* triangle_bias_ptr,   // [B, 1, H, S_qo, S_kv]
  DType* dq_ptr,              // [B, N, H, S_qo, D] output
  DType* dk_ptr,              // [B, N, H, S_kv, D] output
  DType* dv_ptr,              // [B, N, H, S_kv, D] output
  float* triangle_dbias_ptr,  // [B, 1, H, S_qo, S_kv] output
  float* do_o_dot_ptr,        // [B, N, H, S_qo, 1] worspace
  float* dq_fp32_buf_ptr,     // [B, N, H, S_qo, D] workspace
  const uint32_t B,
  const uint32_t I,
  const uint32_t H,
  const uint32_t S_qo,
  const uint32_t S_kv,
  const uint32_t D,
  const float bmm_scale,
  bool use_tf32,
  void* stream,
  bool zero_init_dbias_dq_buf = true);

// Shared sanity checking functions for kernel requirements
// These can be called from bindings before invoking kernel functions
__attribute__((visibility("default"))) void validate_fmha_fwd_params(
  int bits,        // Bit width of dtype (16 for FP16/BF16, 32 for FP32, 64 for FP64)
  uint32_t D,      // Head dimension
  bool use_tf32);  // Whether TF32 is requested

__attribute__((visibility("default"))) void validate_fmha_bwd_params(
  int bits,        // Bit width of dtype (16 for FP16/BF16, 32 for FP32, 64 for FP64)
  bool use_tf32);  // Whether TF32 is requested

// Shared kernel selection helpers
// Determine whether to use SM100 kernels based on conditions
__attribute__((visibility("default"))) bool should_use_sm100f_fwd(
  int bits,  // Bit width of dtype (16 for FP16/BF16, 32 for FP32, 64 for FP64)
  bool has_triangle_bias_same_type,  // Whether triangle_bias has same dtype as q/k/v
  uint32_t D,                        // Head dimension
  uint32_t S_kv,                     // Key/value sequence length
  bool mask_consistent,  // Whether mask_bias_ptr and actual_s_kv_ptr are both null or both non-null
  void* stream,          // CUDA stream (for device capability check)
  const std::optional<std::vector<int>> device_cc =
    std::nullopt);  // Device capability (compute capability version)

__attribute__((visibility("default"))) bool should_use_sm100f_bwd(
  int bits,  // Bit width of dtype (16 for FP16/BF16, 32 for FP32, 64 for FP64)
  bool has_triangle_bias_same_type,  // Whether triangle_bias has same dtype as q/k/v
  uint32_t D,                        // Head dimension
  bool has_dbias_fp32_buf,           // Whether dbias_fp32_buf_ptr is provided
  void* stream,                      // CUDA stream (for device capability check)
  const std::optional<std::vector<int>> device_cc =
    std::nullopt);  // Device capability (compute capability version)

// CUDA-free wrappers for SM100 kernels (can be called from non-CUDA code)
__attribute__((visibility("default"))) void run_fmha_sm100_for_dtype(
  Datatype dtype,
  void* q_ptr,              // [B, N, H, S_qo, D]
  void* k_ptr,              // [B, N, H, S_kv, D]
  void* v_ptr,              // [B, N, H, S_kv, D]
  void* o_ptr,              // [B, N, H, S_qo, D] output
  bool* mask_bias_ptr,      // [B, N, 1, 1, S_kv] (can be nullptr)
  int* actual_s_kv_ptr,     // [B, N] (can be nullptr, must match mask_bias_ptr)
  void* triangle_bias_ptr,  // [B, 1, H, S_qo, S_kv] (same dtype as q/k/v)
  float* softmax_lse_ptr,   // [B, N, H, S_qo, 1] output
  float* softmax_max_ptr,   // [B, N, H, S_qo, 1] output
  uint32_t B,
  uint32_t I,
  uint32_t H,
  uint32_t S_qo,
  uint32_t S_kv,
  uint32_t D,
  float bmm_scale,
  void* stream);

__attribute__((visibility("default"))) void run_fmha_bwd_sm100_for_dtype(
  Datatype dtype,
  void* q_ptr,                // [B, N, H, S_qo, D]
  void* k_ptr,                // [B, N, H, S_kv, D]
  void* v_ptr,                // [B, N, H, S_kv, D]
  void* o_ptr,                // [B, N, H, S_qo, D]
  bool* mask_bias_ptr,        // [B, N, 1, 1, S_kv] (can be nullptr)
  void* triangle_bias_ptr,    // [B, 1, H, S_qo, S_kv] (same dtype as q/k/v)
  float* softmax_lse_ptr,     // [B, N, H, S_qo, 1]
  void* do_ptr,               // [B, N, H, S_qo, D]
  void* dq_ptr,               // [B, N, H, S_qo, D] output
  void* dk_ptr,               // [B, N, H, S_kv, D] output
  void* dv_ptr,               // [B, N, H, S_kv, D] output
  void* triangle_dbias_ptr,   // [B, 1, H, S_qo, S_kv] output (same dtype as q/k/v)
  float* do_o_dot_ptr,        // [B, N, H, S_qo, 1] workspace
  float* dq_fp32_buf_ptr,     // [B, N, H, S_qo, D] workspace
  float* dbias_fp32_buf_ptr,  // [B, 1, H, padded_S_qo, padded_S_kv] workspace
  uint32_t B,
  uint32_t I,
  uint32_t H,
  uint32_t S_qo,
  uint32_t S_kv,
  uint32_t D,
  float bmm_scale,
  bool zero_init_dbias_dq_buf,  // Whether to zero initialize dq_fp32_buf and dbias_fp32_buf
  void* stream);

// Returns true if FP32 bias is needed for forward pass, false if same-dtype bias is used (SM100
// case) Takes minimal arguments needed to determine bias dtype requirement for forward pass
__attribute__((visibility("default"))) bool needs_fp32_bias_fwd(
  int bits,       // Bit width of dtype (16 for FP16/BF16, 32 for FP32, 64 for FP64)
  uint32_t D,     // Head dimension
  uint32_t S_kv,  // Key/value sequence length (for forward pass constraint)
  void* stream);  // CUDA stream (for device capability check)

// Returns true if FP32 bias input is needed for backward pass, false if same-dtype bias is used
// (SM100 case) Takes minimal arguments needed to determine bias input dtype requirement for
// backward pass.
__attribute__((visibility("default"))) bool needs_fp32_bias_bwd(
  int bits,                 // Bit width of dtype (16 for FP16/BF16, 32 for FP32, 64 for FP64)
  uint32_t D,               // Head dimension
  bool has_dbias_fp32_buf,  // Whether dbias FP32 workspace buffer is provided (required for SM100)
  void* stream);            // CUDA stream (for device capability check)

}  // namespace cudnn_fmha

#endif  // CUDNN_FMHA_RUN_FMHA_CUDAFREE_H
