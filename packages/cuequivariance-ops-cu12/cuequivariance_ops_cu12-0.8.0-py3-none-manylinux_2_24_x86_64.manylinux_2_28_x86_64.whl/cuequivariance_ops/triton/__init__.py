# SPDX-FileCopyrightText: Copyright (c) 2024 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: LicenseRef-NvidiaProprietary
#
# NVIDIA CORPORATION, its affiliates and licensors retain all intellectual
# property and proprietary rights in and to this material, related
# documentation and any modifications thereto. Any use, reproduction,
# disclosure or distribution of this material and related documentation
# without an express license agreement from NVIDIA CORPORATION or
# its affiliates is strictly prohibited.

from .fused_layer_norm_triton import (
    Layout,
    layer_norm_transpose_backward_kernel,
    layer_norm_transpose_backward_single_pass_kernel,
    layer_norm_transpose_forward_kernel,
    layer_norm_transpose_forward_single_pass_kernel,
)

from .gated_gemm_triton import (
    fused_sigmoid_gated_dual_gemm_backward_pregemm_kernel,
    fused_sigmoid_gated_dual_gemm_forward_kernel,
)
from .utils import Precision
from .tuning_decorator import autotune_aot
from .cache_manager import get_cache_manager

cached_kernels = [ "fused_sigmoid_gated_dual_gemm_backward_pregemm_kernel",
                   "fused_sigmoid_gated_dual_gemm_forward_kernel",
                  ]

def init_triton_cache():
    """
    Initializes Triton cache manager by pre-loading cache for all available kernels.
    This function is useful to initialize cache in eager mode before running torch.compile()'d methods
    that cannot handle cache initialization code
    """
    mgr = get_cache_manager()
    for kernel in cached_kernels:
        mgr.load_cache(kernel+'_wrapper')

from .utils import (
    Precision,
)

from .pair_bias import (
    pair_bias_norm_linear_mask_forward_kernel,
    pair_bias_linear_mask_forward_kernel,
    pair_bias_mask_forward_kernel,
)


__all__ = [
    "Precision",
    "fused_sigmoid_gated_dual_gemm_backward_pregemm_kernel",
    "fused_sigmoid_gated_dual_gemm_forward_kernel",
    "layer_norm_transpose_backward_kernel",
    "layer_norm_transpose_backward_single_pass_kernel",
    "layer_norm_transpose_forward_kernel",
    "layer_norm_transpose_forward_single_pass_kernel",
    "pair_bias_norm_linear_mask_forward_kernel",
    "pair_bias_linear_mask_forward_kernel",
    "pair_bias_mask_forward_kernel",
    "autotune_aot",
    "get_cache_manager",
    "init_triton_cache"
] + cached_kernels
