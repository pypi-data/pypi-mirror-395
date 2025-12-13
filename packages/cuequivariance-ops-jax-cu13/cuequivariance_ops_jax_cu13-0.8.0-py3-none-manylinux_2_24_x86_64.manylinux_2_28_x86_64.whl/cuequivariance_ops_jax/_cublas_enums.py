# SPDX-FileCopyrightText: Copyright (c) 2024 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: LicenseRef-NvidiaProprietary
#
# NVIDIA CORPORATION, its affiliates and licensors retain all intellectual
# property and proprietary rights in and to this material, related
# documentation and any modifications thereto. Any use, reproduction,
# disclosure or distribution of this material and related documentation
# without an express license agreement from NVIDIA CORPORATION or
# its affiliates is strictly prohibited.

# CUBLAS Compute Types
# Converted from cublas_api.h cublasComputeType_t enum


class CublasComputeTypes:
    """Class to provide getattr access to CUBLAS compute types."""

    CUBLAS_COMPUTE_16F = 64
    CUBLAS_COMPUTE_16F_PEDANTIC = 65
    CUBLAS_COMPUTE_32F = 68
    CUBLAS_COMPUTE_32F_PEDANTIC = 69
    CUBLAS_COMPUTE_32F_FAST_16F = 74
    CUBLAS_COMPUTE_32F_FAST_16BF = 75
    CUBLAS_COMPUTE_32F_FAST_TF32 = 77
    CUBLAS_COMPUTE_64F = 70
    CUBLAS_COMPUTE_64F_PEDANTIC = 71
    CUBLAS_COMPUTE_32I = 72
    CUBLAS_COMPUTE_32I_PEDANTIC = 73


# Create instance for getattr access
cublas_compute_types = CublasComputeTypes()
