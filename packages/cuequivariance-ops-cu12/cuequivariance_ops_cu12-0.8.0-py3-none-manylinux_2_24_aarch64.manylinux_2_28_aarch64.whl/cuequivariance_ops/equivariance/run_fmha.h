#ifndef CUDNN_FMHA_RUN_FMHA_H
#define CUDNN_FMHA_RUN_FMHA_H

#include <cstdint>  // for uint32_t
#include <cuda_fp16.h>
#include <cuda_fp8.h>

namespace cudnn_fmha {
using DataType_TriBias = float;

/**
 * @brief Performs Flash Multi-Head Attention computation on GPU using cuDNN
 * @tparam DType Data type for the computation (float, __half, or __nv_bfloat16)
 */
template <typename DType>
void run_fmha(DType* q_ptr,
              DType* k_ptr,
              DType* v_ptr,
              DType* o_ptr,
              bool* mask_bias_ptr,
              DataType_TriBias* triangle_bias_ptr,
              float* softmax_lse_ptr,
              float* softmax_max_ptr,
              const uint32_t B,
              const uint32_t I,
              const uint32_t H,
              const uint32_t S_qo,
              const uint32_t S_kv,
              const uint32_t D,
              const float bmm_scale,
              bool use_tf32,
              void* stream = nullptr);

/**
 * @brief Performs the backward pass of Flash Multi-Head Attention computation on GPU using cuDNN
 * Note: Backward pass remains in float before fp16/bf16 integration
 */
template <typename DType>
void run_fmha_bwd(DType* do_ptr,              // [B, N, H, S_qo, D]
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
                  float* do_o_dot_ptr,
                  float* dq_fp32_buf,  // [B, N, H, S_qo, D] worspace
                  const uint32_t B,
                  const uint32_t I,
                  const uint32_t H,
                  const uint32_t S_qo,
                  const uint32_t S_kv,
                  const uint32_t D,
                  const float bmm_scale,
                  bool use_tf32,
                  void* stream = nullptr);

// Explicit template declarations for supported types
extern template void run_fmha<float>(float*,
                                     float*,
                                     float*,
                                     float*,
                                     bool*,
                                     DataType_TriBias*,
                                     float*,
                                     float*,
                                     uint32_t,
                                     uint32_t,
                                     uint32_t,
                                     uint32_t,
                                     uint32_t,
                                     uint32_t,
                                     float,
                                     bool,
                                     void*);

extern template void run_fmha<__half>(__half*,
                                      __half*,
                                      __half*,
                                      __half*,
                                      bool*,
                                      DataType_TriBias*,
                                      float*,
                                      float*,
                                      uint32_t,
                                      uint32_t,
                                      uint32_t,
                                      uint32_t,
                                      uint32_t,
                                      uint32_t,
                                      float,
                                      bool,
                                      void*);

extern template void run_fmha<__nv_bfloat16>(__nv_bfloat16*,
                                             __nv_bfloat16*,
                                             __nv_bfloat16*,
                                             __nv_bfloat16*,
                                             bool*,
                                             DataType_TriBias*,
                                             float*,
                                             float*,
                                             uint32_t,
                                             uint32_t,
                                             uint32_t,
                                             uint32_t,
                                             uint32_t,
                                             uint32_t,
                                             float,
                                             bool,
                                             void*);

extern template void run_fmha_bwd<__half>(__half* do_ptr,
                                          __half* o_ptr,
                                          float* softmax_lse_ptr,
                                          __half* q_ptr,
                                          __half* k_ptr,
                                          __half* v_ptr,
                                          bool* mask_bias_ptr,
                                          float* triangle_bias_ptr,
                                          __half* dq_ptr,
                                          __half* dk_ptr,
                                          __half* dv_ptr,
                                          float* triangle_dbias_ptr,
                                          float* do_o_dot_ptr,
                                          float* dq_fp32_buf,
                                          const uint32_t B,
                                          const uint32_t I,
                                          const uint32_t H,
                                          const uint32_t S_qo,
                                          const uint32_t S_kv,
                                          const uint32_t D,
                                          const float bmm_scale,
                                          bool use_tf32,
                                          void* stream);

extern template void run_fmha_bwd<__nv_bfloat16>(__nv_bfloat16* do_ptr,
                                                 __nv_bfloat16* o_ptr,
                                                 float* softmax_lse_ptr,
                                                 __nv_bfloat16* q_ptr,
                                                 __nv_bfloat16* k_ptr,
                                                 __nv_bfloat16* v_ptr,
                                                 bool* mask_bias_ptr,
                                                 float* triangle_bias_ptr,
                                                 __nv_bfloat16* dq_ptr,
                                                 __nv_bfloat16* dk_ptr,
                                                 __nv_bfloat16* dv_ptr,
                                                 float* triangle_dbias_ptr,
                                                 float* do_o_dot_ptr,
                                                 float* dq_fp32_buf,
                                                 const uint32_t B,
                                                 const uint32_t I,
                                                 const uint32_t H,
                                                 const uint32_t S_qo,
                                                 const uint32_t S_kv,
                                                 const uint32_t D,
                                                 const float bmm_scale,
                                                 bool use_tf32,
                                                 void* stream);

extern template void run_fmha_bwd<float>(float* do_ptr,
                                         float* o_ptr,
                                         float* softmax_lse_ptr,
                                         float* q_ptr,
                                         float* k_ptr,
                                         float* v_ptr,
                                         bool* mask_bias_ptr,
                                         float* triangle_bias_ptr,
                                         float* dq_ptr,
                                         float* dk_ptr,
                                         float* dv_ptr,
                                         float* triangle_dbias_ptr,
                                         float* do_o_dot_ptr,
                                         float* dq_fp32_buf,
                                         const uint32_t B,
                                         const uint32_t I,
                                         const uint32_t H,
                                         const uint32_t S_qo,
                                         const uint32_t S_kv,
                                         const uint32_t D,
                                         const float bmm_scale,
                                         bool use_tf32,
                                         void* stream);

}  // namespace cudnn_fmha

#endif  // CUDNN_FMHA_RUN_FMHA_H
