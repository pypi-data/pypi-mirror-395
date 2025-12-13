/*
 * Copyright (c) 2024, NVIDIA CORPORATION. All rights reserved.
 *
 * This source code and/or documentation ("Licensed Deliverables") are
 * subject to NVIDIA intellectual property rights under U.S. and
 * international Copyright laws.
 */

#pragma once

#include <cstdint>
#include <cuda_bf16.h>
#include <cuda_fp16.h>
#include <vector>

namespace kernelcatcher {

namespace tensor_product {
/**
 * @brief a wrapper struct containing informations
 * about tensor-product paths
 */
template <typename MathT>
struct __attribute__((aligned(16))) tp_info {
  /** offsets into `path_offsets_and_dims` for each "target" */
  const int32_t* __restrict__ path_csr_offsets{nullptr};
  /** "sources" of all paths and their offsets and dimensions */
  const int32_t* __restrict__ path_offsets_and_dims{nullptr};
  /** clebsch-gordan values for each path */
  const MathT* __restrict__ path_cg_values{nullptr};
  /** number of "target" segments */
  int32_t num_target_segments{0};
  /** number of path (i.e. all paths between segments) */
  int32_t num_paths{0};
};  // struct tp_info

enum class ConnectionModeT : uint8_t {
  kUVW = 0,
  // UVW with U spherical harmonic
  k1VW,  // NOLINT
  // UVW with V spherical harmonic
  kU1W,  // NOLINT
  kUVU,
  kUVV,
  kUUW,
  kUUU,
  // FullTP, no weight
  kUVUV,
  // FullTP, U spherical harmonic
  k1V1V,
  // FullTP, V spherical harmonic
  kU1U1,
  // Linear
  kUUVV,
};
}  // namespace tensor_product

namespace symmetric_tensor_contraction {
/**
 * @brief a wrapper struct containing informations
 * about tensor-product paths
 */
template <typename DataT>
struct __attribute__((aligned(16))) clebsch_gordan_tensor {
  const DataT* __restrict__ cg_values{nullptr};
  const int16_t* __restrict__ cg_indices{nullptr};
  const int32_t* __restrict__ cg_offsets{nullptr};
  int32_t total_output_irreps{0};
};  // struct clebsch_gordan_tensor
}  // namespace symmetric_tensor_contraction

namespace batch_linear {
struct __attribute__((aligned(8))) MatrixLayout {
  int32_t size_row;  // uncontracted mode
  int32_t size_col;  // contracted mode
};

struct __attribute__((aligned(8))) IndexOffset {
  int32_t start;
  int32_t end;
};

enum class GemvModeT : std::uint8_t { kUVV = 0, kUUV = 1 };
enum class WeightSharedModeT : std::int32_t { kShared = 0, kIndexed = 1, kBatched = 2 };
/**
 * @brief a wrapper struct containing informations
 * about tensor-product paths
 */
template <typename DataT>
struct __attribute__((aligned(16))) batch_linear_info {
  const MatrixLayout* __restrict__ layouts{nullptr};
  const IndexOffset* __restrict__ index_offsets{nullptr};
  const int32_t* __restrict__ indices{nullptr};
  const DataT* __restrict__ alpha{nullptr};
};  // struct batch_linear_info

}  // namespace batch_linear
}  // namespace kernelcatcher
