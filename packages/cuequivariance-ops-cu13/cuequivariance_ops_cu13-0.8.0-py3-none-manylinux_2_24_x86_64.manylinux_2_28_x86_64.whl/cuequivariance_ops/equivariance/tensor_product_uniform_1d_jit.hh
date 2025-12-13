/*
 * Copyright (c) 2025, NVIDIA CORPORATION. All rights reserved.
 *
 * This source code and/or documentation ("Licensed Deliverables") are
 * subject to NVIDIA intellectual property rights under U.S. and
 * international Copyright laws.
 */

#pragma once

#include "batch_dimension.hh"  // for BatchDimension
#include "dtypes.hh"           // for Datatype
#include <cstdint>
#include <string>
#include <vector>

namespace kernelcatcher::equivariance::tensor_product_uniform_1d_jit {
using namespace kernelcatcher::utils;

enum class Dimension : int { kScalar = 0, kOneDimensional = 1 };

#define KC_UNIFORM_1D_DECL_ARGUMENTS                                                         \
  std::string const &name, Datatype math_dtype, int operand_extent, int num_inputs,          \
    int num_outputs, int num_index, std::vector<Dimension> const &buffer_dim,                \
    std::vector<int> const &buffer_num_segments,                                             \
    std::vector<std::vector<BatchDimension>> const &batch_dim,                               \
    std::vector<std::vector<int>> const &index_buffer, std::vector<int> const &index_extent, \
    std::vector<Datatype> const &dtypes, std::vector<std::vector<int>> const &operations,    \
    std::vector<int> const &num_paths, std::vector<int> const &path_indices_start,           \
    std::vector<int> const &path_coefficients_start, std::vector<int> const &path_indices,   \
    std::vector<double> const &path_coefficients, std::vector<int> const &batch_sizes,       \
    std::vector<void*> const &buffers, std::vector<size_t> const &buffer_bytes,              \
    bool zero_output_buffers

extern int run_tensor_product_uniform_1d_jit(KC_UNIFORM_1D_DECL_ARGUMENTS, void* stream);
extern int run_tensor_product_uniform_1d_cpu(KC_UNIFORM_1D_DECL_ARGUMENTS);

}  // namespace kernelcatcher::equivariance::tensor_product_uniform_1d_jit
