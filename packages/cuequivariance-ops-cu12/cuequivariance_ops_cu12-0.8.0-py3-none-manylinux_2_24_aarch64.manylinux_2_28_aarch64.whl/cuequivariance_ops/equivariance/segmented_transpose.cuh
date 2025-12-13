/*
 * Copyright (c) 2021-2024, NVIDIA CORPORATION. All rights reserved.
 *
 * This source code and/or documentation ("Licensed Deliverables") are
 * subject to NVIDIA intellectual property rights under U.S. and
 * international Copyright laws.
 */

#pragma once

#include "../common/common.hpp"

namespace kernelcatcher::tensor_product {

template <typename DataT>
void segmented_transpose(DataT* tensor_transpose,
                         const DataT* tensor,
                         const int32_t* segment_info,
                         int32_t num_segments,
                         int64_t batch_size,
                         int64_t stride,
                         bool input_contiguous_as_info,
                         cudaStream_t stream);

extern template void segmented_transpose<float>(
  float*, const float*, const int32_t*, int32_t, int64_t, int64_t, bool, cudaStream_t);
extern template void segmented_transpose<double>(
  double*, const double*, const int32_t*, int32_t, int64_t, int64_t, bool, cudaStream_t);
extern template void segmented_transpose<__nv_bfloat16>(__nv_bfloat16*,
                                                        const __nv_bfloat16*,
                                                        const int32_t*,
                                                        int32_t,
                                                        int64_t,
                                                        int64_t,
                                                        bool,
                                                        cudaStream_t);
extern template void segmented_transpose<__half>(
  __half*, const __half*, const int32_t*, int32_t, int64_t, int64_t, bool, cudaStream_t);

}  // namespace kernelcatcher::tensor_product
