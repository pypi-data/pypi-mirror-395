# tests/test_basic.py
# Basic tests for ba-cuda package

import torch
import numpy as np
import pytest


def test_se3_creation():
    """Test SE3 creation from R and t."""
    from ba_cuda import SE3
    
    R = torch.eye(3, dtype=torch.float64)
    t = torch.zeros(3, dtype=torch.float64)
    
    pose = SE3.from_Rt(R, t)
    
    assert pose.shape == torch.Size([1])
    assert pose.R.shape == (1, 3, 3)
    assert pose.t.shape == (1, 3)


def test_se3_transform():
    """Test SE3 point transformation."""
    from ba_cuda import SE3
    
    R = torch.eye(3, dtype=torch.float64)
    t = torch.tensor([1.0, 2.0, 3.0], dtype=torch.float64)
    
    pose = SE3.from_Rt(R, t)
    
    point = torch.tensor([[0.0, 0.0, 0.0]], dtype=torch.float64)
    p_cam = pose.transform_from(point)
    
    assert torch.allclose(p_cam, t.unsqueeze(0))


def test_se3_retract():
    """Test SE3 retract (pose update)."""
    from ba_cuda import SE3
    
    R = torch.eye(3, dtype=torch.float64).unsqueeze(0)
    t = torch.zeros(1, 3, dtype=torch.float64)
    
    pose = SE3.from_Rt(R, t)
    
    # Small perturbation
    delta = torch.zeros(1, 6, dtype=torch.float64)
    delta[0, 0] = 0.1  # small translation in v_x
    
    new_pose = pose.retract(delta)
    
    # Translation should change
    assert new_pose.t[0, 0] > 0


def test_huber_loss():
    """Test HuberLoss."""
    from ba_cuda import HuberLoss
    
    huber = HuberLoss(delta=1.0)
    
    # Small residuals should give quadratic loss
    r_small = torch.tensor([0.1, -0.1])
    loss_small = huber(r_small)
    expected_small = 0.5 * r_small * r_small
    assert torch.allclose(loss_small, expected_small)
    
    # Large residuals should give linear loss
    r_large = torch.tensor([10.0, -10.0])
    loss_large = huber(r_large)
    expected_large = 1.0 * (torch.abs(r_large) - 0.5 * 1.0)
    assert torch.allclose(loss_large, expected_large)


def test_projection():
    """Test project_points_batch."""
    from ba_cuda import SE3, project_points_batch
    
    # Identity pose
    R = torch.eye(3, dtype=torch.float64).unsqueeze(0)
    t = torch.zeros(1, 3, dtype=torch.float64)
    pose = SE3.from_Rt(R, t)
    
    # Simple point at (0, 0, 1)
    points = torch.tensor([[0.0, 0.0, 1.0]], dtype=torch.float64)
    
    # Simple intrinsics (fx=fy=100, cx=cy=50)
    K = torch.tensor([[[100.0, 0.0, 50.0],
                       [0.0, 100.0, 50.0],
                       [0.0, 0.0, 1.0]]], dtype=torch.float64)
    
    # No distortion
    dist = torch.zeros(1, 5, dtype=torch.float64)
    
    uv, J = project_points_batch(pose, points, K, dist)
    
    # Point at (0,0,1) should project to (cx, cy) = (50, 50)
    assert torch.allclose(uv, torch.tensor([[50.0, 50.0]], dtype=torch.float64), atol=1e-6)
    assert J.shape == (1, 2, 6)


def test_optimizer_smoke():
    """Smoke test for LevenbergMarquardtOptimizer."""
    from ba_cuda import LevenbergMarquardtOptimizer
    
    # Create simple test case with 2 cameras
    n_cams = 2
    n_obs = 10
    
    # Random observations
    observations = torch.randn(n_obs, 2, dtype=torch.float64) * 10 + 50
    points_3d = torch.randn(n_obs, 3, dtype=torch.float64)
    points_3d[:, 2] = torch.abs(points_3d[:, 2]) + 1  # Ensure positive Z
    camera_indices = torch.randint(0, n_cams, (n_obs,))
    
    # Intrinsics
    K = torch.zeros(n_cams, 3, 3, dtype=torch.float64)
    K[:, 0, 0] = 100; K[:, 1, 1] = 100
    K[:, 0, 2] = 50; K[:, 1, 2] = 50
    K[:, 2, 2] = 1
    
    # No distortion
    dist = torch.zeros(n_cams, 5, dtype=torch.float64)
    
    # Initial poses (identity)
    poses = torch.zeros(n_cams, 3, 4, dtype=torch.float64)
    poses[:, :3, :3] = torch.eye(3, dtype=torch.float64)
    
    optimizer = LevenbergMarquardtOptimizer(max_iterations=5)
    
    # Should run without error
    optimized_poses, rmse = optimizer.optimize(
        observations=observations,
        points_3d=points_3d,
        camera_indices=camera_indices,
        intrinsics=K,
        distortions=dist,
        initial_poses=poses,
        ref_cam_idx=0,
        verbose=False
    )
    
    assert optimized_poses.shape == (n_cams, 3, 4)
    assert isinstance(rmse, float)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
