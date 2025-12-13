# SPDX-FileCopyrightText: Copyright (c) 2024 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: LicenseRef-NvidiaProprietary
#
# NVIDIA CORPORATION, its affiliates and licensors retain all intellectual
# property and proprietary rights in and to this material, related
# documentation and any modifications thereto. Any use, reproduction,
# disclosure or distribution of this material and related documentation
# without an express license agreement from NVIDIA CORPORATION or
# its affiliates is strictly prohibited.

from ._version import __version__, __git_commit__
import os
import sys
import ctypes

PREFERRED_LOAD_FLAG = ctypes.RTLD_LOCAL


def root_dir():
    try:
        import importlib.metadata

        dist = importlib.metadata.distribution("cuequivariance_ops")
        root = dist.locate_file("cuequivariance_ops")
    except Exception:
        # last resort, will fail with writeable install
        root = os.path.dirname(__file__)
    return root


def load_library():
    try:
        ctypes.CDLL(
            os.path.join(root_dir(), "lib/libcue_ops.so"), mode=PREFERRED_LOAD_FLAG
        )
    except Exception as e:
        print(f"Error while loading libcue_ops.so: {e}", file=sys.stderr)


load_library()

__all__ = ["__version__", "__git_commit__", "root_dir", "load_library"]
