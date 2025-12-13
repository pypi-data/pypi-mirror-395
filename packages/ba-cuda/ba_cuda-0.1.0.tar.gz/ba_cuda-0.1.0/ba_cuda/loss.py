# ba_cuda/loss.py
# Huber Loss Implementation
# Copied from auto_calib/bundle_adjustment.py

import torch


class HuberLoss:
    """Huber loss for robust optimization."""
    
    def __init__(self, delta: float = 1.0):
        self.delta = delta
    
    def __call__(self, residual: torch.Tensor) -> torch.Tensor:
        """Compute Huber loss."""
        abs_r = torch.abs(residual)
        quadratic = 0.5 * residual * residual
        linear = self.delta * (abs_r - 0.5 * self.delta)
        return torch.where(abs_r <= self.delta, quadratic, linear)
    
    def weight(self, residual: torch.Tensor) -> torch.Tensor:
        """Compute IRLS weight for Huber loss."""
        abs_r = torch.abs(residual) + 1e-12
        return torch.where(abs_r <= self.delta, torch.ones_like(abs_r), self.delta / abs_r)
