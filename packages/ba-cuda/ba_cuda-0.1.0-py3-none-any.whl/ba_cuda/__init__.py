# ba_cuda/__init__.py
# Public API for ba-cuda package

"""
ba-cuda: GPU-accelerated Bundle Adjustment using PyTorch with Analytical Jacobians.

This package provides a high-performance bundle adjustment implementation
optimized for CUDA GPUs using PyTorch.

Example:
    >>> import torch
    >>> from ba_cuda import LevenbergMarquardtOptimizer
    >>> 
    >>> optimizer = LevenbergMarquardtOptimizer()
    >>> optimized_poses, rmse = optimizer.optimize(
    ...     observations=observations,
    ...     points_3d=points_3d,
    ...     camera_indices=camera_indices,
    ...     intrinsics=intrinsics,
    ...     distortions=distortions,
    ...     initial_poses=initial_poses,
    ...     ref_cam_idx=0
    ... )
"""

from .se3 import SE3
from .loss import HuberLoss
from .projection import project_points_batch
from .optimizer import LevenbergMarquardtOptimizer

__version__ = "0.1.0"
__all__ = [
    "SE3",
    "HuberLoss",
    "project_points_batch",
    "LevenbergMarquardtOptimizer",
]
