/*
 * Copyright (c) 2023-2024, NVIDIA CORPORATION. All rights reserved.
 *
 * This source code and/or documentation ("Licensed Deliverables") are
 * subject to NVIDIA intellectual property rights under U.S. and
 * international Copyright laws.
 */

#pragma once

#include <iostream>

namespace kernelcatcher::utils {

enum class Datatype : int {
  kFloat32  = 0,
  kFloat64  = 1,
  kFloat16  = 2,
  kBFloat16 = 3,
  kInt32    = 4,
  kInt64    = 5
};

inline int size_of(Datatype dtype)
{
  switch (dtype) {
    case Datatype::kFloat32: return 4;
    case Datatype::kFloat64: return 8;
    case Datatype::kFloat16: return 2;
    case Datatype::kBFloat16: return 2;
    case Datatype::kInt32: return 4;
    case Datatype::kInt64: return 8;
    default: return -1;
  }
}

inline std::ostream& operator<<(std::ostream& s, Datatype const& d)
{
  switch (d) {
    case Datatype::kFloat32: return s << "float";
    case Datatype::kFloat64: return s << "double";
    case Datatype::kFloat16: return s << "k_fp16";
    case Datatype::kBFloat16: return s << "k_bf16";
    case Datatype::kInt32: return s << "kc_int32";
    case Datatype::kInt64: return s << "kc_int64";
  }
  return s << "unknown_datatype";
}

inline bool is_real(Datatype const& d)
{
  switch (d) {
    case Datatype::kFloat32:
    case Datatype::kFloat64:
    case Datatype::kFloat16:
    case Datatype::kBFloat16: return true;
    case Datatype::kInt32:
    case Datatype::kInt64: return false;
  }
  return false;  // Default case, should not be reached
}

inline bool is_integral(Datatype const& d) { return !is_real(d); }

}  // namespace kernelcatcher::utils
