/*
 * Copyright (c) 2025, NVIDIA CORPORATION. All rights reserved.
 *
 * This source code and/or documentation ("Licensed Deliverables") are
 * subject to NVIDIA intellectual property rights under U.S. and
 * international Copyright laws.
 */

#pragma once

#include "dtypes.hh"  // for Datatype

namespace kernelcatcher::equivariance::indexed_linear {
using namespace kernelcatcher::utils;  // for Datatype

#define KC_INDEXED_LINEAR_DECL_ARGUMENTS                                                  \
  const void *ptr_A, const void *ptr_B, const int *counts, void *ptr_C, Datatype dtype_A, \
    Datatype dtype_B, Datatype dtype_D, int Z, int C, int u, int v, double coefficient,   \
    int compute_type, void *workspace, size_t workspace_size, void *stream

#define KC_INDEXED_LINEAR_ARGUMENTS                                                              \
  ptr_A, ptr_B, counts, ptr_C, dtype_A, dtype_B, dtype_D, Z, C, u, v, coefficient, compute_type, \
    workspace, workspace_size, stream

int run_indexed_linear_B(  // ptr_A  Zu
                           // ptr_B  Cuv or Cvu
                           // ptr_C  Zv
  bool transpose_B,
  KC_INDEXED_LINEAR_DECL_ARGUMENTS);

int run_indexed_linear_C(  // ptr_A  Zu
                           // ptr_B  Zv
                           // ptr_C  Cuv
  KC_INDEXED_LINEAR_DECL_ARGUMENTS);

}  // namespace kernelcatcher::equivariance::indexed_linear
