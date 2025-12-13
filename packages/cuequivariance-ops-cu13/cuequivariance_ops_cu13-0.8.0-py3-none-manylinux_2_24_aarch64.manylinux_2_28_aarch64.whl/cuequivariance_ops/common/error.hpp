/*
 * Copyright (c) 2020-2024, NVIDIA CORPORATION. All rights reserved.
 *
 * This source code and/or documentation ("Licensed Deliverables") are
 * subject to NVIDIA intellectual property rights under U.S. and
 * international Copyright laws.
 */

#pragma once

#include "error_raft.hpp"

#include <cuda_bf16.h>
#include <cuda_fp16.h>

namespace kernelcatcher::utils {

template <typename DataT>
void inline assert_data_type_support()
{
  // defaut data type is always supported
}

template <>
void inline assert_data_type_support<__half>()
{
  int device, major;
  RAFT_CUDA_TRY(cudaGetDevice(&device));
  RAFT_CUDA_TRY(cudaDeviceGetAttribute(&major, cudaDevAttrComputeCapabilityMajor, device));
  ASSERT(major >= 7,
         "Detected compute capability < 7, however requested DataType __half requires >= 7.");
}

template <>
void inline assert_data_type_support<__half2>()
{
  int device, major;
  RAFT_CUDA_TRY(cudaGetDevice(&device));
  RAFT_CUDA_TRY(cudaDeviceGetAttribute(&major, cudaDevAttrComputeCapabilityMajor, device));
  ASSERT(major >= 7,
         "Detected compute capability < 7, however requested DataType __half2 requires >= 7.");
}

template <>
void inline assert_data_type_support<__nv_bfloat16>()
{
  int device, major;
  RAFT_CUDA_TRY(cudaGetDevice(&device));
  RAFT_CUDA_TRY(cudaDeviceGetAttribute(&major, cudaDevAttrComputeCapabilityMajor, device));
  ASSERT(
    major >= 8,
    "Detected compute capability < 8, however requested DataType __nv_bfloat16 requires >= 8.");
}

template <>
void inline assert_data_type_support<__nv_bfloat162>()
{
  int device, major;
  RAFT_CUDA_TRY(cudaGetDevice(&device));
  RAFT_CUDA_TRY(cudaDeviceGetAttribute(&major, cudaDevAttrComputeCapabilityMajor, device));
  ASSERT(
    major >= 8,
    "Detected compute capability < 8, however requested DataType __nv_bfloat162 requires >= 8.");
}

}  // namespace kernelcatcher::utils
