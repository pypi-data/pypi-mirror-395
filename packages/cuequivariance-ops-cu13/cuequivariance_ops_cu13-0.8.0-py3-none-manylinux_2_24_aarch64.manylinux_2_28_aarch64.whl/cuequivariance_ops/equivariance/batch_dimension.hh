/*
 * Copyright (c) 2023-2024, NVIDIA CORPORATION. All rights reserved.
 *
 * This source code and/or documentation ("Licensed Deliverables") are
 * subject to NVIDIA intellectual property rights under U.S. and
 * international Copyright laws.
 */

#pragma once

namespace kernelcatcher::utils {

enum class BatchDimension : int { kBatched = 0, kShared = 1, kIndexed = 2 };

}  // namespace kernelcatcher::utils
