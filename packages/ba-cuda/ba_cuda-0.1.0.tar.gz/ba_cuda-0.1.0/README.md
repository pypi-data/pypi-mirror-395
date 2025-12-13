# ba-cuda

GPU-accelerated Bundle Adjustment using PyTorch with Analytical Jacobians.

## Features

- **SE3 Lie Group**: Right perturbation convention for camera pose representation
- **Analytical Jacobians**: Fast and accurate gradient computation
- **Batched Operations**: Efficient GPU parallelization
- **Levenberg-Marquardt Optimizer**: Robust non-linear optimization
- **Huber Loss**: Robust to outliers

## Installation

### 1. Install PyTorch (Required - Manual Installation)

**⚠️ Important**: PyTorch must be installed manually according to your CUDA version.

1. Check your CUDA version:
   ```bash
   nvcc --version
   ```

2. Install PyTorch from the [official website](https://pytorch.org/get-started/locally/):
   
   For example, with CUDA 12.1:
   ```bash
   pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
   ```
   
   For CUDA 11.8:
   ```bash
   pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
   ```

### 2. Install ba-cuda

```bash
pip install ba-cuda
```

Or from source:
```bash
git clone https://github.com/hunminkim98/BA_on_CUDA_130_Win.git
cd BA_on_CUDA_130_Win
pip install -e .
```

## Quick Start

```python
import torch
from ba_cuda import LevenbergMarquardtOptimizer

# Prepare your data
observations = torch.tensor(...)      # (N_obs, 2) - 2D observations
points_3d = torch.tensor(...)         # (N_obs, 3) - 3D points
camera_indices = torch.tensor(...)    # (N_obs,) - camera index per observation
intrinsics = torch.tensor(...)        # (N_cams, 3, 3)
distortions = torch.tensor(...)       # (N_cams, 5)
initial_poses = torch.tensor(...)     # (N_cams, 3, 4) - [R|t]

# Run optimization
optimizer = LevenbergMarquardtOptimizer()
optimized_poses, rmse = optimizer.optimize(
    observations=observations,
    points_3d=points_3d,
    camera_indices=camera_indices,
    intrinsics=intrinsics,
    distortions=distortions,
    initial_poses=initial_poses,
    ref_cam_idx=0
)

print(f"Final RMSE: {rmse:.4f}")
```

## API Reference

### LevenbergMarquardtOptimizer

```python
optimizer = LevenbergMarquardtOptimizer(
    max_iterations=50,      # Maximum LM iterations
    abs_tolerance=1e-6,     # Absolute convergence tolerance
    rel_tolerance=1e-6,     # Relative convergence tolerance
    initial_damping=1e-3,   # Initial LM damping factor
    huber_delta=1.0,        # Huber loss delta
    device=None,            # torch.device (auto-detects CUDA if available)
    dtype=torch.float64     # Precision
)
```

### Input Tensor Formats

| Tensor | Shape | Description |
|--------|-------|-------------|
| `observations` | (N_obs, 2) | 2D keypoint observations (u, v) |
| `points_3d` | (N_obs, 3) | 3D points in reference camera frame |
| `camera_indices` | (N_obs,) | Camera index for each observation |
| `intrinsics` | (N_cams, 3, 3) | Camera intrinsic matrices K |
| `distortions` | (N_cams, 5) | Distortion coefficients [k1, k2, p1, p2, k3] |
| `initial_poses` | (N_cams, 3, 4) | Initial camera poses [R|t] |

## Requirements

- Python >= 3.10
- PyTorch >= 2.0.0 (with CUDA support recommended)
- NumPy >= 1.20.0

## License

MIT License
