# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Python library for Signed Distance Function (SDF) based loss functions for deep learning semantic segmentation. The library implements several loss functions that weight pixels based on their distance from object boundaries, putting heavier penalties on false positives and false negatives that are farther from the correct boundary.

## Development Setup

This project uses `uv` as the package manager. Python 3.10+ is required.

### Installing Dependencies

```bash
uv sync
```

### Code Quality

The project uses Ruff for linting and formatting:

```bash
uv run ruff check src/
uv run ruff format src/
```

## Architecture

### Core Loss Functions

The library provides a hierarchy of loss functions in `src/sdf_loss/`:

1. **DiceLoss** (`DiceLoss.py`): Base Dice loss implementation with support for custom weight functions
   - Modified from segmentation_models_pytorch (SMP)
   - Supports pixel-wise weighting via `weight_func` parameter
   - Can operate on logits or probabilities

2. **SDFWeightedBCELoss** (`SDFWeightedBCELoss.py`): Binary cross-entropy loss weighted by SDF differences
   - Weights pixels by the absolute difference between predicted and target SDFs
   - Uses `sdf_difference_weighted_bceloss_from_logits` from utils

3. **SDFWeightedDiceLoss** (`SDFWeightedDiceLoss.py`): Dice loss weighted by SDF differences
   - Inherits from DiceLoss
   - Uses `sdf_difference_map` as the weight function

4. **DiscoLoss** (`DiSCoLoss.py`): Combined loss function
   - Distance-scaled combination of base losses (BCE + Dice) and SDF-weighted losses
   - Configurable weights via `baseloss_weight` and `sdfweighted_weight` parameters
   - Default: only SDF-weighted losses (baseloss_weight=0, sdfweighted_weight=1)

### Key Design Patterns

- All loss functions inherit from `torch.nn.Module`
- SDF-weighted losses use utility functions from `utils.py`
- The `normalize` parameter controls whether SDFs are normalized to [-1, 1] range
- The `clip_negatives` parameter controls handling of negative distance values
- All composite losses operate on logits by default

### Import Structure

The loss modules use relative imports (e.g., `from DiceLoss import DiceLoss`), which assumes they're imported from within the package or the package directory is in the Python path.

## Dependencies

Key dependencies:
- **torch**: Deep learning framework (>= 2.9.1)
- **numpy**: Numerical operations (>= 2.2.6)
- **scikit-image**: Image processing, likely for distance transforms (>= 0.25.2)
- **scipy**: Scientific computing utilities (>= 1.15.3)
- **ruff**: Linting and formatting (>= 0.14.7)
