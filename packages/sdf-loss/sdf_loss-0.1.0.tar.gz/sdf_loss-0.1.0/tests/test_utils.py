"""Tests for utility functions."""

import pytest
import torch
from sdf_loss.utils import (
    compute_sdf,
    sdf_difference_map,
    sdf_difference_weighted_bceloss_from_logits,
)


class TestComputeSDF:
    """Tests for compute_sdf function."""

    def test_compute_sdf_basic(self):
        """Test basic SDF computation."""
        # Create a simple binary mask with a square in the center
        mask = torch.zeros(1, 1, 10, 10)
        mask[0, 0, 3:7, 3:7] = 1.0

        sdf = compute_sdf(mask, normalize=False)

        assert sdf.shape == mask.shape, "SDF should have same shape as input"
        # Center pixels (inside) should have positive values
        assert sdf[0, 0, 5, 5].item() > 0, "Center should have positive SDF"
        # Corner pixels (outside) should have negative values
        assert sdf[0, 0, 0, 0].item() < 0, "Corner should have negative SDF"

    def test_compute_sdf_normalize(self):
        """Test SDF normalization."""
        mask = torch.zeros(1, 1, 20, 20)
        mask[0, 0, 5:15, 5:15] = 1.0

        sdf_norm = compute_sdf(mask, normalize=True)
        sdf_raw = compute_sdf(mask, normalize=False)

        # Normalized SDF should be in [-1, 1] range
        assert sdf_norm.min().item() >= -1.0, "Normalized SDF min should be >= -1"
        assert sdf_norm.max().item() <= 1.0, "Normalized SDF max should be <= 1"

        # Raw SDF should have larger magnitude
        assert abs(sdf_raw.min().item()) > abs(sdf_norm.min().item()), (
            "Raw SDF should have larger magnitude"
        )

    def test_compute_sdf_batch(self):
        """Test SDF computation with batches."""
        batch_size = 4
        mask = torch.zeros(batch_size, 1, 10, 10)

        # Create different patterns in each batch
        for i in range(batch_size):
            mask[i, 0, 2 + i : 8 - i, 2 + i : 8 - i] = 1.0

        sdf = compute_sdf(mask, normalize=True)

        assert sdf.shape == mask.shape, "SDF should have same shape as input"
        assert torch.isfinite(sdf).all(), "All SDF values should be finite"

    def test_compute_sdf_3d_input(self):
        """Test SDF with 3D input (B, H, W)."""
        mask = torch.zeros(2, 10, 10)
        mask[0, 3:7, 3:7] = 1.0
        mask[1, 2:8, 2:8] = 1.0

        sdf = compute_sdf(mask, normalize=True)

        assert sdf.shape == mask.shape, "SDF should have same shape as 3D input"
        assert torch.isfinite(sdf).all(), "All SDF values should be finite"

    def test_compute_sdf_empty_mask(self):
        """Test SDF with empty mask."""
        mask = torch.zeros(1, 1, 10, 10)

        sdf = compute_sdf(mask, normalize=True)

        assert sdf.shape == mask.shape, "SDF should have same shape as input"
        # All values should be negative (outside)
        assert (sdf <= 0).all(), "Empty mask should have all negative SDF"

    def test_compute_sdf_full_mask(self):
        """Test SDF with full mask."""
        mask = torch.ones(1, 1, 10, 10)

        sdf = compute_sdf(mask, normalize=True)

        assert sdf.shape == mask.shape, "SDF should have same shape as input"
        # All values should be positive (inside)
        assert (sdf >= 0).all(), "Full mask should have all positive SDF"


class TestSDFDifferenceMap:
    """Tests for sdf_difference_map function."""

    def test_sdf_difference_map_basic(self):
        """Test basic SDF difference map computation."""
        pred = torch.zeros(1, 1, 10, 10)
        pred[0, 0, 3:7, 3:7] = 0.9

        target = torch.zeros(1, 1, 10, 10)
        target[0, 0, 3:7, 3:7] = 1.0

        diff = sdf_difference_map(pred, target, normalize=True, clip_negatives=False)

        assert diff.shape == pred.shape, (
            "Difference map should have same shape as input"
        )
        assert (diff >= 0).all(), "Differences should be non-negative (absolute value)"
        assert torch.isfinite(diff).all(), "All differences should be finite"

    def test_sdf_difference_map_identical(self):
        """Test SDF difference map with identical inputs."""
        mask = torch.zeros(1, 1, 10, 10)
        mask[0, 0, 3:7, 3:7] = 1.0

        diff = sdf_difference_map(mask, mask, normalize=True, clip_negatives=False)

        # Difference should be close to zero for identical inputs
        assert diff.max().item() < 0.1, (
            "Difference should be near zero for identical inputs"
        )

    def test_sdf_difference_map_opposite(self):
        """Test SDF difference map with opposite inputs."""
        pred = torch.zeros(1, 1, 10, 10)
        pred[0, 0, 3:7, 3:7] = 1.0

        target = torch.ones(1, 1, 10, 10)
        target[0, 0, 3:7, 3:7] = 0.0

        diff = sdf_difference_map(pred, target, normalize=True, clip_negatives=False)

        # Difference should be large for opposite inputs
        assert diff.mean().item() > 0.5, (
            "Difference should be large for opposite inputs"
        )

    def test_sdf_difference_map_clip_negatives(self):
        """Test clip_negatives parameter."""
        pred = torch.randn(1, 1, 10, 10).sigmoid()
        target = torch.randint(0, 2, (1, 1, 10, 10)).float()

        diff_clip = sdf_difference_map(pred, target, clip_negatives=True)
        diff_no_clip = sdf_difference_map(pred, target, clip_negatives=False)

        # Both should be non-negative (absolute value is taken)
        assert (diff_clip >= 0).all(), "Should be non-negative with clipping"
        assert (diff_no_clip >= 0).all(), "Should be non-negative without clipping"


class TestSDFDifferenceWeightedBCELoss:
    """Tests for sdf_difference_weighted_bceloss_from_logits function."""

    def test_weighted_bce_basic(self):
        """Test basic weighted BCE computation."""
        pred_logits = torch.randn(2, 1, 8, 8)
        target = torch.randint(0, 2, (2, 1, 8, 8)).float()

        loss = sdf_difference_weighted_bceloss_from_logits(
            pred_logits, target, reduction="mean", normalize=True
        )

        assert torch.isfinite(loss), "Loss should be finite"
        assert loss.item() >= 0.0, "Loss should be non-negative"

    def test_weighted_bce_reduction_modes(self):
        """Test different reduction modes."""
        pred_logits = torch.randn(2, 1, 8, 8)
        target = torch.randint(0, 2, (2, 1, 8, 8)).float()

        loss_mean = sdf_difference_weighted_bceloss_from_logits(
            pred_logits, target, reduction="mean"
        )
        loss_sum = sdf_difference_weighted_bceloss_from_logits(
            pred_logits, target, reduction="sum"
        )
        loss_none = sdf_difference_weighted_bceloss_from_logits(
            pred_logits, target, reduction="none"
        )

        assert loss_mean.dim() == 0, "Mean reduction should produce scalar"
        assert loss_sum.dim() == 0, "Sum reduction should produce scalar"
        assert loss_none.shape == pred_logits.shape, (
            "None reduction should preserve shape"
        )
        assert loss_sum.item() > loss_mean.item(), "Sum should be larger than mean"

    def test_weighted_bce_perfect_prediction(self):
        """Test weighted BCE with perfect prediction."""
        # Perfect prediction (high logits for positive class)
        pred_logits = torch.ones(1, 1, 10, 10) * 10.0
        target = torch.ones(1, 1, 10, 10)

        loss = sdf_difference_weighted_bceloss_from_logits(
            pred_logits, target, reduction="mean"
        )

        assert loss.item() < 0.1, "Loss should be low for perfect prediction"

    def test_weighted_bce_gradient_flow(self):
        """Test that gradients flow through weighted BCE."""
        pred_logits = torch.randn(2, 1, 8, 8, requires_grad=True)
        target = torch.randint(0, 2, (2, 1, 8, 8)).float()

        loss = sdf_difference_weighted_bceloss_from_logits(
            pred_logits, target, reduction="mean"
        )
        loss.backward()

        assert pred_logits.grad is not None, "Gradients should flow through"
        assert torch.isfinite(pred_logits.grad).all(), "Gradients should be finite"


class TestIntegration:
    """Integration tests for utils functions."""

    def test_sdf_computation_consistency(self):
        """Test that SDF computation is consistent."""
        mask = torch.zeros(1, 1, 20, 20)
        mask[0, 0, 5:15, 5:15] = 1.0

        # Compute SDF multiple times
        sdf1 = compute_sdf(mask, normalize=True)
        sdf2 = compute_sdf(mask, normalize=True)

        # Should be identical
        assert torch.allclose(sdf1, sdf2), "SDF computation should be deterministic"

    def test_device_compatibility(self):
        """Test that functions work with CPU tensors."""
        mask = torch.zeros(1, 1, 10, 10)
        mask[0, 0, 3:7, 3:7] = 1.0

        sdf = compute_sdf(mask, normalize=True)
        assert sdf.device == mask.device, "Output should be on same device as input"

    def test_dtype_preservation(self):
        """Test that dtype is preserved."""
        mask = torch.zeros(1, 1, 10, 10, dtype=torch.float32)
        mask[0, 0, 3:7, 3:7] = 1.0

        sdf = compute_sdf(mask, normalize=True)
        assert sdf.dtype == torch.float32, "Should preserve float32 dtype"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
