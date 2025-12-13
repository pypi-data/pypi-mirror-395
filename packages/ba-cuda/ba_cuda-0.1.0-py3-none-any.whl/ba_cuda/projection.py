# ba_cuda/projection.py
# Functional Reprojection with Analytical Jacobians
# Copied from auto_calib/bundle_adjustment.py

import torch
from typing import Tuple

from .se3 import SE3


def project_points_batch(
    poses: SE3, 
    points_3d: torch.Tensor, 
    intrinsics: torch.Tensor, 
    distortions: torch.Tensor
) -> Tuple[torch.Tensor, torch.Tensor]:
    """
    Batched projection with analytical Jacobian.
    
    Args:
        poses: SE3 object with batch size N (or broadcastable)
        points_3d: (N, 3)
        intrinsics: (N, 3, 3)
        distortions: (N, 5)
        
    Returns:
        uv: (N, 2)
        J_total: (N, 2, 6) Jacobian w.r.t pose
    """
    N = points_3d.shape[0]
    
    # 1. Transform: World -> Camera
    jacobians_se3 = []
    p_cam = poses.transform_from(points_3d, jacobians_se3)  # (N, 3)
    J_se3 = jacobians_se3[0]  # (N, 3, 6)
    
    x, y, z = p_cam[:, 0], p_cam[:, 1], p_cam[:, 2]
    z_safe = torch.clamp(z, min=1e-6)
    z2 = z_safe * z_safe
    
    # 2. Normalized coords
    xn = x / z_safe
    yn = y / z_safe
    
    # Jacobian d(xn,yn)/d(p_cam)
    # dxn/dp = [1/z, 0, -x/z^2]
    # dyn/dp = [0, 1/z, -y/z^2]
    dxn_dp = torch.stack([1/z_safe, torch.zeros_like(z), -x/z2], dim=-1) # (N, 3)
    dyn_dp = torch.stack([torch.zeros_like(z), 1/z_safe, -y/z2], dim=-1) # (N, 3)
    
    # 3. Distortion
    r2 = xn*xn + yn*yn
    r4 = r2*r2
    r6 = r4*r2
    
    k1 = distortions[:, 0]; k2 = distortions[:, 1]; p1 = distortions[:, 2]
    p2 = distortions[:, 3]; k3 = distortions[:, 4]
    
    radial = 1.0 + k1*r2 + k2*r4 + k3*r6
    
    xd = xn*radial + 2*p1*xn*yn + p2*(r2 + 2*xn*xn)
    yd = yn*radial + p1*(r2 + 2*yn*yn) + 2*p2*xn*yn
    
    # Derivatives of Distortion
    dr2_dxn = 2*xn; dr2_dyn = 2*yn
    dradial_dr2 = k1 + 2*k2*r2 + 3*k3*r4
    
    # dxd/dxn
    dxd_dxn = radial + xn * dradial_dr2 * dr2_dxn + 2*p1*yn + p2*6*xn
    dxd_dyn = xn * dradial_dr2 * dr2_dyn + 2*p1*xn + p2*2*yn
    
    # dyd/dyn
    dyd_dxn = yn * dradial_dr2 * dr2_dxn + p1*2*xn + 2*p2*yn
    dyd_dyn = radial + yn * dradial_dr2 * dr2_dyn + p1*6*yn + 2*p2*xn
    
    # 4. Intrinsics
    fx = intrinsics[:, 0, 0]
    fy = intrinsics[:, 1, 1]
    cx = intrinsics[:, 0, 2]
    cy = intrinsics[:, 1, 2]
    
    u = fx * xd + cx
    v = fy * yd + cy
    uv = torch.stack([u, v], dim=-1)
    
    # Chain Rule Assembly
    # J_proj_norm = d(uv)/d(xn,yn) @ d(xn,yn)/d(p_cam)
    
    du_dxn = fx * dxd_dxn
    du_dyn = fx * dxd_dyn
    dv_dxn = fy * dyd_dxn
    dv_dyn = fy * dyd_dyn
    
    # Shape: (N, 2, 3)
    # Row 0 (u): du/dxn * dxn/dp + du/dyn * dyn/dp
    J_proj_u = du_dxn.unsqueeze(-1) * dxn_dp + du_dyn.unsqueeze(-1) * dyn_dp
    J_proj_v = dv_dxn.unsqueeze(-1) * dxn_dp + dv_dyn.unsqueeze(-1) * dyn_dp
    
    J_proj = torch.stack([J_proj_u, J_proj_v], dim=1) # (N, 2, 3)
    
    # Final Jacobian: J_total = J_proj @ J_se3
    # (N, 2, 3) @ (N, 3, 6) -> (N, 2, 6)
    J_total = torch.bmm(J_proj, J_se3)
    
    return uv, J_total
