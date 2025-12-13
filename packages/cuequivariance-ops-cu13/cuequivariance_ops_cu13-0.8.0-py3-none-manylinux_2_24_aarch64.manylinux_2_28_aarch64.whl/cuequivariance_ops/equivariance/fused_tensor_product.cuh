/*
 * Copyright (c) 2021-2024, NVIDIA CORPORATION. All rights reserved.
 *
 * This source code and/or documentation ("Licensed Deliverables") are
 * subject to NVIDIA intellectual property rights under U.S. and
 * international Copyright laws.
 */

#pragma once

#include "../common/common.hpp"

#include <algorithm>
#include <limits>

namespace kernelcatcher::tensor_product {

struct __attribute__((aligned(16))) tp_data_sizes {
  int64_t batch_size;
  bool shared_a;
  bool shared_b;
  bool shared_w;
  int32_t stride_a;
  int32_t stride_b;
  int32_t stride_w;
  int32_t stride_o;
};  // struct tp_data_sizes

template <typename DataAT, typename DataBT, typename DataWeightT, typename DataOutT, typename MathT>
void fused_tensor_product_fwd(DataOutT* out,
                              const DataAT* in_a,
                              const DataBT* in_b,
                              const DataWeightT* weight,
                              ConnectionModeT mode,
                              const tp_info<MathT>& info,
                              const tp_data_sizes& sizes,
                              cudaStream_t stream);

template <typename DataAT, typename DataBT, typename DataWeightT, typename DataOutT, typename MathT>
void fused_tensor_product_bwd(DataAT* grad_in_a,
                              DataBT* grad_in_b,
                              DataWeightT* grad_weight,
                              const DataOutT* grad_out,
                              const DataAT* in_a,
                              const DataBT* in_b,
                              const DataWeightT* weight,
                              ConnectionModeT mode,
                              const tp_info<MathT>& info_bwd_dgrad_a,
                              const tp_info<MathT>& info_bwd_dgrad_b,
                              const tp_info<MathT>& info_bwd_dgrad_w,
                              const tp_data_sizes& sizes,
                              cudaStream_t stream);

template <typename DataAT, typename DataBT, typename DataWeightT, typename DataOutT, typename MathT>
void fused_tensor_product_bwd_bwd(DataAT* grad_in_a,
                                  DataBT* grad_in_b,
                                  DataWeightT* grad_weight,
                                  DataOutT* grad_grad_out,
                                  const DataAT* grad_grad_in_a,
                                  const DataBT* grad_grad_in_b,
                                  const DataWeightT* grad_grad_weight,
                                  const DataOutT* grad_out,
                                  const DataAT* in_a,
                                  const DataBT* in_b,
                                  const DataWeightT* weight,
                                  ConnectionModeT mode,
                                  const tp_info<MathT>& info_fwd,
                                  const tp_info<MathT>& info_bwd_dgrad_a,
                                  const tp_info<MathT>& info_bwd_dgrad_b,
                                  const tp_info<MathT>& info_bwd_dgrad_w,
                                  const tp_data_sizes& sizes,
                                  cudaStream_t stream);

extern template void fused_tensor_product_bwd_bwd<float, float, float, float, float>(
  float*,
  float*,
  float*,
  float*,
  const float*,
  const float*,
  const float*,
  const float*,
  const float*,
  const float*,
  const float*,
  ConnectionModeT,
  const tp_info<float>&,
  const tp_info<float>&,
  const tp_info<float>&,
  const tp_info<float>&,
  const tp_data_sizes&,
  cudaStream_t);

extern template void fused_tensor_product_bwd_bwd<float, float, float, float, double>(
  float*,
  float*,
  float*,
  float*,
  const float*,
  const float*,
  const float*,
  const float*,
  const float*,
  const float*,
  const float*,
  ConnectionModeT,
  const tp_info<double>&,
  const tp_info<double>&,
  const tp_info<double>&,
  const tp_info<double>&,
  const tp_data_sizes&,
  cudaStream_t);

extern template void fused_tensor_product_bwd_bwd<double, double, double, double, double>(
  double*,
  double*,
  double*,
  double*,
  const double*,
  const double*,
  const double*,
  const double*,
  const double*,
  const double*,
  const double*,
  ConnectionModeT,
  const tp_info<double>&,
  const tp_info<double>&,
  const tp_info<double>&,
  const tp_info<double>&,
  const tp_data_sizes&,
  cudaStream_t);

extern template void fused_tensor_product_bwd_bwd<__half, __half, __half, __half, float>(
  __half*,
  __half*,
  __half*,
  __half*,
  const __half*,
  const __half*,
  const __half*,
  const __half*,
  const __half*,
  const __half*,
  const __half*,
  ConnectionModeT,
  const tp_info<float>&,
  const tp_info<float>&,
  const tp_info<float>&,
  const tp_info<float>&,
  const tp_data_sizes&,
  cudaStream_t);
extern template void
fused_tensor_product_bwd_bwd<__nv_bfloat16, __nv_bfloat16, __nv_bfloat16, __nv_bfloat16, float>(
  __nv_bfloat16*,
  __nv_bfloat16*,
  __nv_bfloat16*,
  __nv_bfloat16*,
  const __nv_bfloat16*,
  const __nv_bfloat16*,
  const __nv_bfloat16*,
  const __nv_bfloat16*,
  const __nv_bfloat16*,
  const __nv_bfloat16*,
  const __nv_bfloat16*,
  ConnectionModeT,
  const tp_info<float>&,
  const tp_info<float>&,
  const tp_info<float>&,
  const tp_info<float>&,
  const tp_data_sizes&,
  cudaStream_t);

extern template void fused_tensor_product_bwd<float, float, float, float, float>(
  float*,
  float*,
  float*,
  const float*,
  const float*,
  const float*,
  const float*,
  ConnectionModeT,
  const tp_info<float>&,
  const tp_info<float>&,
  const tp_info<float>&,
  const tp_data_sizes&,
  cudaStream_t);

extern template void fused_tensor_product_bwd<float, float, float, float, double>(
  float*,
  float*,
  float*,
  const float*,
  const float*,
  const float*,
  const float*,
  ConnectionModeT,
  const tp_info<double>&,
  const tp_info<double>&,
  const tp_info<double>&,
  const tp_data_sizes&,
  cudaStream_t);

extern template void fused_tensor_product_bwd<double, double, double, double, double>(
  double*,
  double*,
  double*,
  const double*,
  const double*,
  const double*,
  const double*,
  ConnectionModeT,
  const tp_info<double>&,
  const tp_info<double>&,
  const tp_info<double>&,
  const tp_data_sizes&,
  cudaStream_t);

extern template void fused_tensor_product_bwd<__half, __half, __half, __half, float>(
  __half*,
  __half*,
  __half*,
  const __half*,
  const __half*,
  const __half*,
  const __half*,
  ConnectionModeT,
  const tp_info<float>&,
  const tp_info<float>&,
  const tp_info<float>&,
  const tp_data_sizes&,
  cudaStream_t);
extern template void
fused_tensor_product_bwd<__nv_bfloat16, __nv_bfloat16, __nv_bfloat16, __nv_bfloat16, float>(
  __nv_bfloat16*,
  __nv_bfloat16*,
  __nv_bfloat16*,
  const __nv_bfloat16*,
  const __nv_bfloat16*,
  const __nv_bfloat16*,
  const __nv_bfloat16*,
  ConnectionModeT,
  const tp_info<float>&,
  const tp_info<float>&,
  const tp_info<float>&,
  const tp_data_sizes&,
  cudaStream_t);

extern template void fused_tensor_product_fwd<float, float, float, float, float>(
  float*,
  const float*,
  const float*,
  const float*,
  ConnectionModeT,
  const tp_info<float>&,
  const tp_data_sizes&,
  cudaStream_t);
extern template void fused_tensor_product_fwd<float, float, float, float, double>(
  float*,
  const float*,
  const float*,
  const float*,
  ConnectionModeT,
  const tp_info<double>&,
  const tp_data_sizes&,
  cudaStream_t);
extern template void fused_tensor_product_fwd<double, double, double, double, double>(
  double*,
  const double*,
  const double*,
  const double*,
  ConnectionModeT,
  const tp_info<double>&,
  const tp_data_sizes&,
  cudaStream_t);

extern template void fused_tensor_product_fwd<__half, __half, __half, __half, float>(
  __half*,
  const __half*,
  const __half*,
  const __half*,
  ConnectionModeT,
  const tp_info<float>&,
  const tp_data_sizes&,
  cudaStream_t);
extern template void
fused_tensor_product_fwd<__nv_bfloat16, __nv_bfloat16, __nv_bfloat16, __nv_bfloat16, float>(
  __nv_bfloat16*,
  const __nv_bfloat16*,
  const __nv_bfloat16*,
  const __nv_bfloat16*,
  ConnectionModeT,
  const tp_info<float>&,
  const tp_data_sizes&,
  cudaStream_t);

}  // namespace kernelcatcher::tensor_product
