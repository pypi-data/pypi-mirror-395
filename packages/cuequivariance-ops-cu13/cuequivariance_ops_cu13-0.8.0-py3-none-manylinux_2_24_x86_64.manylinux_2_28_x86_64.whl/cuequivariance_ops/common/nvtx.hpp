/*
 * Copyright (c) 2019-2023, NVIDIA CORPORATION. All rights reserved.
 *
 * This source code and/or documentation ("Licensed Deliverables") are
 * subject to NVIDIA intellectual property rights under U.S. and
 * international Copyright laws.
 */

#pragma once

namespace kernelcatcher::utils {

/**
 * @brief Push a named nvtx range
 * @param name range name
 */
void push_range(const char* name);

/** Pop the latest range */
void pop_range();

struct range_guard {
  range_guard(const char* name) { push_range(name); }
  ~range_guard() { pop_range(); }
  range_guard(range_guard const&)            = delete;
  range_guard& operator=(range_guard const&) = delete;
};

}  // namespace kernelcatcher::utils
