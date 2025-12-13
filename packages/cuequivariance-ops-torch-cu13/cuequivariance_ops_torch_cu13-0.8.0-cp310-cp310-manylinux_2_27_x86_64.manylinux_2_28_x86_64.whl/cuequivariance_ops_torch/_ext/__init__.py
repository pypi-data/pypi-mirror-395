# SPDX-FileCopyrightText: Copyright (c) 2024 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: LicenseRef-NvidiaProprietary
#
# NVIDIA CORPORATION, its affiliates and licensors retain all intellectual
# property and proprietary rights in and to this material, related
# documentation and any modifications thereto. Any use, reproduction,
# disclosure or distribution of this material and related documentation
# without an express license agreement from NVIDIA CORPORATION or
# its affiliates is strictly prohibited.


from .cuequivariance_ops_torch_ext import *  # light-weight wrapper


## CLEAN-UP BEGIN ############################################################
# clean up references from the typing module
# it's important to register this function *after* including the extension
# module, since this will run the function *before* nanobind's clean-up
# see https://github.com/wjakob/nanobind/issues/69
def _typing_cleanup():
    import typing

    for cleanup in typing._cleanups:
        cleanup()


import atexit

atexit.register(_typing_cleanup)
# remove atexit from this package
del atexit
## CLEAN-UP END ##############################################################
