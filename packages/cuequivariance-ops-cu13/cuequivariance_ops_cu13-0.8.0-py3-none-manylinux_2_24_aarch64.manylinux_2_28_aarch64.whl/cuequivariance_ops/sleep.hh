/*
 * Copyright (c) 2025, NVIDIA CORPORATION. All rights reserved.
 *
 * This source code and/or documentation ("Licensed Deliverables") are
 * subject to NVIDIA intellectual property rights under U.S. and
 * international Copyright laws.
 */

#pragma once

/*
 * DEPRECATED HEADER: This header has been renamed to gpu_timing_kernels.hh
 *
 * This compatibility header provides backward compatibility for code that includes
 * the old sleep.hh header name. The header has been renamed to better reflect
 * its content (GPU timing and synchronization kernels).
 *
 * For new code, please use:
 *     #include "gpu_timing_kernels.hh"
 *
 * OLD (deprecated but still works):
 *     #include "sleep.hh"
 *
 * NEW (recommended):
 *     #include "gpu_timing_kernels.hh"
 *
 * This compatibility header will be removed in a future version.
 */

#warning \
  "The 'sleep.hh' header has been renamed to 'gpu_timing_kernels.hh'. Please update your #include statements. This compatibility header will be removed in a future version."

// Include the new header to maintain compatibility
#include "gpu_timing_kernels.hh"

// Provide backward compatibility aliases
namespace kernelcatcher::sleep {
using kernelcatcher::gpu_utilities::run_sleep;
using kernelcatcher::gpu_utilities::run_synchronize;
}  // namespace kernelcatcher::sleep
