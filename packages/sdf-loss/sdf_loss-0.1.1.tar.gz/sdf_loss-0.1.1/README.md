# SDF Loss

Signed Distance Function (SDF) based loss functions for deep learning semantic segmentation.

## Overview

This library provides PyTorch loss functions that use Signed Distance Functions to weight pixels based on their distance from object boundaries. This approach puts heavier penalties on false positives and false negatives that are farther from the correct boundary, leading to more accurate segmentation results.

## Installation

Install directly from PyPI:

```bash
pip install sdf-loss
```

Or using uv:

```bash
uv add sdf-loss
```

## Quick Start

```python
import torch
from sdf_loss import DiSCoLoss

# Initialize the loss function
criterion = DiSCoLoss()

# Your model predictions (logits) and ground truth
pred_logits = model(images)  # Shape: (B, 1, H, W)
target = ground_truth         # Shape: (B, 1, H, W), binary mask

# Compute loss
loss = criterion(pred_logits, target)
loss.backward()
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.
