# ba_cuda/se3.py
# SE3 Lie Group Implementation (Theseus-style Right Perturbation)
# Copied from auto_calib/bundle_adjustment.py

import torch
from typing import Optional, List


class SE3:
    """
    SE3 Lie group for camera poses.
    
    Stores transformation as (batch, 3, 4) matrix.
    Convention: Right Perturbation T_new = T * exp(delta)
    Delta order: [v(3), omega(3)] (Translation, Rotation)
    """
    
    def __init__(
        self, 
        tensor: torch.Tensor,
        device: torch.device = None,
        dtype: torch.dtype = torch.float64
    ):
        """
        Args:
            tensor: (batch, 3, 4) or (batch, 4, 4) or (3, 4) or (4, 4) transformation matrix
        """
        if tensor.dim() == 2:
            tensor = tensor.unsqueeze(0)
        
        # Convert to (batch, 3, 4)
        if tensor.shape[-2:] == (4, 4):
            tensor = tensor[..., :3, :]
        
        self.tensor = tensor.to(dtype=dtype, device=device if device else tensor.device)
        self.device = self.tensor.device
        self.dtype = self.tensor.dtype
    
    @property
    def shape(self) -> torch.Size:
        return self.tensor.shape[:-2]
    
    @property
    def R(self) -> torch.Tensor:
        """Rotation matrix (batch, 3, 3)"""
        return self.tensor[..., :3, :3]
    
    @property
    def t(self) -> torch.Tensor:
        """Translation vector (batch, 3)"""
        return self.tensor[..., :3, 3]
    
    @staticmethod
    def from_Rt(
        R: torch.Tensor, 
        t: torch.Tensor,
        device: torch.device = None,
        dtype: torch.dtype = torch.float64
    ) -> 'SE3':
        if R.dim() == 2:
            R = R.unsqueeze(0)
        if t.dim() == 1:
            t = t.unsqueeze(0)
        
        batch = R.shape[0]
        T = torch.zeros(batch, 3, 4, dtype=dtype, device=device if device else R.device)
        T[:, :3, :3] = R.to(dtype=dtype)
        T[:, :3, 3] = t.to(dtype=dtype)
        
        return SE3(T, device=device, dtype=dtype)
    
    @staticmethod
    def _rodrigues_batch(rvec: torch.Tensor) -> torch.Tensor:
        """Batch Rodrigues formula: rotation vector -> rotation matrix."""
        theta = torch.norm(rvec, dim=1, keepdim=True)
        
        small_angle = (theta < 1e-8).squeeze(-1)
        axis = rvec / (theta + 1e-12)
        K = SE3._skew_batch(axis)
        
        sin_theta = torch.sin(theta).unsqueeze(-1)
        cos_theta = torch.cos(theta).unsqueeze(-1)
        
        I = torch.eye(3, dtype=rvec.dtype, device=rvec.device).unsqueeze(0)
        R = I + sin_theta * K + (1 - cos_theta) * torch.bmm(K, K)
        
        if small_angle.any():
            R[small_angle] = I + K[small_angle]
        
        return R
    
    @staticmethod
    def _skew_batch(v: torch.Tensor) -> torch.Tensor:
        """Batch skew-symmetric matrix."""
        batch = v.shape[0]
        K = torch.zeros(batch, 3, 3, dtype=v.dtype, device=v.device)
        K[:, 0, 1] = -v[:, 2]; K[:, 0, 2] = v[:, 1]
        K[:, 1, 0] = v[:, 2]; K[:, 1, 2] = -v[:, 0]
        K[:, 2, 0] = -v[:, 1]; K[:, 2, 1] = v[:, 0]
        return K
    
    @staticmethod
    def _hat(v: torch.Tensor) -> torch.Tensor:
        if v.dim() == 1: v = v.unsqueeze(0)
        return SE3._skew_batch(v)
    
    def transform_from(
        self, 
        point: torch.Tensor,
        jacobians: Optional[List[torch.Tensor]] = None
    ) -> torch.Tensor:
        """
        Transform point from world to camera frame.
        p_cam = R @ p_world + t
        """
        if point.dim() == 1:
            point = point.unsqueeze(0)
        
        N = point.shape[0]
        R = self.R
        t = self.t
        
        if R.shape[0] == 1 and N > 1:
            R = R.expand(N, -1, -1)
            t = t.expand(N, -1)
        
        p_cam = torch.bmm(R, point.unsqueeze(-1)).squeeze(-1) + t
        
        if jacobians is not None:
            # Analytical Jacobian for Right Perturbation T_new = T * exp(delta)
            # delta = [v, omega]
            # d(p_cam)/d(v) = R
            # d(p_cam)/d(omega) = -R @ [p_world]x  (Wait, this derivation depends on T * exp(delta) * p)
            # Actually: T * exp(delta) * p
            # = (T + T * delta_hat) * p = T*p + T * delta_hat * p
            # delta_hat * p = [omega]x p + v
            # T * ( [omega]x p + v ) = R * ( [omega]x p + v )
            # = R [omega]x p + R v
            # = -R [p]x omega + R v
            # So d/domega = -R [p]x, d/dv = R
            
            J_pose = torch.zeros(N, 3, 6, dtype=self.dtype, device=self.device)
            hat_p = SE3._hat(point)
            
            J_pose[:, :, :3] = R  # d/dv
            J_pose[:, :, 3:] = -torch.bmm(R, hat_p)  # d/domega
            
            # Jacobian w.r.t. point: d(Rp+t)/dp = R
            J_point = R.clone()
            
            jacobians.append(J_pose)
            jacobians.append(J_point)
        
        return p_cam
    
    def retract(self, delta: torch.Tensor) -> 'SE3':
        """
        Retract: self * exp(delta) (Right Perturbation)
        """
        v = delta[:, :3]
        omega = delta[:, 3:]
        
        dR = SE3._rodrigues_batch(omega)
        # T_new = T * exp(delta)
        # exp(delta) ~ [dR, v] (approx)
        # T_new = [R, t] * [dR, v; 0, 1] = [R*dR, R*v + t]
        
        new_R = torch.bmm(self.R, dR)
        new_t = torch.bmm(self.R, v.unsqueeze(-1)).squeeze(-1) + self.t
        
        return SE3.from_Rt(new_R, new_t, device=self.device, dtype=self.dtype)
    
    def copy(self) -> 'SE3':
        return SE3(self.tensor.clone(), device=self.device, dtype=self.dtype)
