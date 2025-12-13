/*
 * Copyright (c) 2025, NVIDIA CORPORATION. All rights reserved.
 *
 * This source code and/or documentation ("Licensed Deliverables") are
 * subject to NVIDIA intellectual property rights under U.S. and
 * international Copyright laws.
 */

/*
 * GPU Events Implementation Attribution
 *
 * The CUDA event recording and timing functionality (record_event, event_elapsed)
 * has been adapted from JAX's GPU events implementation that was removed in version 0.7.2.
 *
 * Original source: https://github.com/jax-ml/jax/
 * License: Apache License 2.0
 *
 * JAX Copyright 2018 The JAX Authors.
 * Licensed under the Apache License, Version 2.0.
 */

#pragma once

#include <cstdint>

namespace kernelcatcher::gpu_utilities {

int run_sleep(float* seconds, int64_t* elapsed_ticks, void* stream);
int run_synchronize(float* elapsed_seconds, void* stream);

// Record a CUDA event on the given stream
// Returns 0 on success, non-zero on error
int record_event(uint64_t* event_handle, void* stream, bool copy_before);

// Calculate elapsed time between two events
// Returns 0 on success, non-zero on error
int event_elapsed(const uint64_t* start_event_handle,
                  const uint64_t* end_event_handle,
                  float* elapsed_ms,
                  void* stream);

}  // namespace kernelcatcher::gpu_utilities
