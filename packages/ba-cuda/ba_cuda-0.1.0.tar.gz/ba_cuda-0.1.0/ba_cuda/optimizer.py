# ba_cuda/optimizer.py
# Batched Levenberg-Marquardt Optimizer
# Copied from auto_calib/bundle_adjustment.py

import numpy as np
import torch
from typing import Dict, List, Tuple
import logging

from .se3 import SE3
from .loss import HuberLoss
from .projection import project_points_batch

logger = logging.getLogger(__name__)


class LevenbergMarquardtOptimizer:
    """
    Batched Levenberg-Marquardt optimizer for Bundle Adjustment.
    
    Optimizes camera extrinsics to minimize reprojection error.
    Uses analytical Jacobians for high performance on GPU.
    """
    
    def __init__(
        self,
        max_iterations: int = 50,
        abs_tolerance: float = 1e-6,
        rel_tolerance: float = 1e-6,
        initial_damping: float = 1e-3,
        huber_delta: float = 1.0,
        device: torch.device = None,
        dtype: torch.dtype = torch.float64
    ):
        self.max_iterations = max_iterations
        self.abs_tolerance = abs_tolerance
        self.rel_tolerance = rel_tolerance
        self.initial_damping = initial_damping
        self.device = device if device else torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.dtype = dtype
        self.huber = HuberLoss(delta=huber_delta)

    def optimize(
        self,
        observations: torch.Tensor,     # (N_obs, 2) - 2D observations
        points_3d: torch.Tensor,         # (N_obs, 3) - 3D points
        camera_indices: torch.Tensor,    # (N_obs,) - camera index per observation
        intrinsics: torch.Tensor,        # (N_cams, 3, 3)
        distortions: torch.Tensor,       # (N_cams, 5)
        initial_poses: torch.Tensor,     # (N_cams, 3, 4) - [R|t]
        ref_cam_idx: int = 0,
        verbose: bool = True
    ) -> Tuple[torch.Tensor, float]:
        """
        Run Levenberg-Marquardt optimization.
        
        Args:
            observations: (N_obs, 2) 2D observed keypoints
            points_3d: (N_obs, 3) corresponding 3D points (in reference camera frame)
            camera_indices: (N_obs,) camera index for each observation
            intrinsics: (N_cams, 3, 3) camera intrinsic matrices
            distortions: (N_cams, 5) distortion coefficients [k1, k2, p1, p2, k3]
            initial_poses: (N_cams, 3, 4) initial camera poses [R|t]
            ref_cam_idx: index of reference camera (fixed during optimization)
            verbose: whether to print progress
            
        Returns:
            optimized_poses: (N_cams, 3, 4) optimized camera poses
            rmse: final reprojection RMSE
        """
        # Move to device
        observations = observations.to(device=self.device, dtype=self.dtype)
        points_3d = points_3d.to(device=self.device, dtype=self.dtype)
        camera_indices = camera_indices.to(device=self.device, dtype=torch.long)
        intrinsics = intrinsics.to(device=self.device, dtype=self.dtype)
        distortions = distortions.to(device=self.device, dtype=self.dtype)
        initial_poses = initial_poses.to(device=self.device, dtype=self.dtype)
        
        n_cams = initial_poses.shape[0]
        
        # Current Estimate
        current_poses = SE3(initial_poses, device=self.device, dtype=self.dtype)
        
        # Expand intrinsics/distortions for every observation
        batch_intrinsics = intrinsics.index_select(0, camera_indices)
        batch_distortions = distortions.index_select(0, camera_indices)
        
        damping = self.initial_damping
        
        # Initial Error
        with torch.no_grad():
            obs_poses_tensor = current_poses.tensor.index_select(0, camera_indices)
            obs_poses = SE3(obs_poses_tensor, device=self.device, dtype=self.dtype)
            
            uv_init, _ = project_points_batch(obs_poses, points_3d, batch_intrinsics, batch_distortions)
            residuals_init = uv_init - observations
            loss_init = self.huber(residuals_init).sum()
            prev_error = loss_init.item()
        
        if verbose:
            logger.info(f"Initial Error: {prev_error:.4f}")
        
        for iteration in range(self.max_iterations):
            # 1. Linearize (Compute Jacobian and Residuals)
            obs_poses_tensor = current_poses.tensor.index_select(0, camera_indices)
            obs_poses = SE3(obs_poses_tensor, device=self.device, dtype=self.dtype)
            
            # This is the heavy lifting, batched on GPU
            uv, J = project_points_batch(obs_poses, points_3d, batch_intrinsics, batch_distortions)
            
            residuals = uv - observations # (N_obs, 2)
            
            # Robust Weighting
            r_norm = torch.norm(residuals, dim=1, keepdim=True) # (N_obs, 1)
            sqrt_w = torch.sqrt(self.huber.weight(r_norm)) # (N_obs, 1)
            
            J_weighted = J * sqrt_w.unsqueeze(-1) # (N_obs, 2, 6)
            r_weighted = residuals * sqrt_w # (N_obs, 2)
            
            # 2. Build Linear System (JtJ delta = -Jtr)
            JtJ_obs = torch.bmm(J_weighted.transpose(1, 2), J_weighted)
            Jtr_obs = torch.bmm(J_weighted.transpose(1, 2), r_weighted.unsqueeze(-1))
            
            # Accumulate into (N_cams, 6, 6) and (N_cams, 6)
            H = torch.zeros(n_cams, 6, 6, device=self.device, dtype=self.dtype)
            b = torch.zeros(n_cams, 6, device=self.device, dtype=self.dtype)
            
            H.index_add_(0, camera_indices, JtJ_obs)
            b.index_add_(0, camera_indices, Jtr_obs.squeeze(-1))
            
            # 3. Apply Damping (Levenberg-Marquardt)
            diag_H = torch.diagonal(H, dim1=-2, dim2=-1) # (N_cams, 6)
            damping_diag = torch.diag_embed(damping * diag_H.clamp(min=1e-6)) # (N_cams, 6, 6)
            
            H_damped = H + damping_diag
            
            # Fix Reference Camera
            H_damped[ref_cam_idx] = torch.eye(6, device=self.device, dtype=self.dtype) * 1e9
            b[ref_cam_idx] = 0
            
            # 4. Solve System
            try:
                delta = torch.linalg.solve(H_damped, -b) # (N_cams, 6)
            except RuntimeError:
                delta = torch.linalg.lstsq(H_damped, -b).solution
            
            # Force ref cam delta to 0
            delta[ref_cam_idx] = 0
            
            # 5. Update
            new_current_poses = current_poses.retract(delta)
            
            # 6. Evaluate
            obs_poses_tensor_new = new_current_poses.tensor.index_select(0, camera_indices)
            obs_poses_new = SE3(obs_poses_tensor_new, device=self.device, dtype=self.dtype)
            uv_new, _ = project_points_batch(obs_poses_new, points_3d, batch_intrinsics, batch_distortions)
            loss_new = self.huber(uv_new - observations).sum().item()
            
            if loss_new < prev_error:
                # Accept
                current_poses = new_current_poses
                damping /= 10.0
                if verbose and iteration % 5 == 0:
                    logger.info(f"Iter {iteration}: Error {prev_error:.1f} -> {loss_new:.1f}")
                
                if (prev_error - loss_new) / prev_error < self.rel_tolerance:
                    if verbose: logger.info("Converged (Rel)")
                    break
                prev_error = loss_new
            else:
                # Reject
                damping *= 10.0
                if verbose and iteration % 10 == 0:
                    logger.debug(f"Iter {iteration}: Rejected. Damping {damping:.4f}")
        
        # Final RMSE
        rmse = np.sqrt(prev_error / (2 * len(points_3d)))
        
        if verbose:
            logger.info(f"Final RMSE: {rmse:.4f}")
        
        return current_poses.tensor, rmse
