# SPDX-FileCopyrightText: Copyright (c) 2024 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: LicenseRef-NvidiaProprietary
#
# NVIDIA CORPORATION, its affiliates and licensors retain all intellectual
# property and proprietary rights in and to this material, related
# documentation and any modifications thereto. Any use, reproduction,
# disclosure or distribution of this material and related documentation
# without an express license agreement from NVIDIA CORPORATION or
# its affiliates is strictly prohibited.

import enum

import triton
import triton.language as tl


class Precision(enum.Enum):
    DEFAULT = 0
    TF32 = 1
    TF32x3 = 2
    IEEE = 3
    NONE = -1


@triton.jit
def cvt_tf32_rn(x: tl.tensor) -> tl.tensor:
    return tl.inline_asm_elementwise(
        "cvt.rna.tf32.f32 $0, $1;", "=r, r", [x], dtype=tl.float32, is_pure=True, pack=1
    )
