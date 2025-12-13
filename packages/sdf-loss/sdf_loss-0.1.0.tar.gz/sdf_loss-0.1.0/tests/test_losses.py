"""Tests for loss functions."""

import pytest
import torch
from sdf_loss import DiceLoss, SDFWeightedBCELoss, SDFWeightedDiceLoss, DiSCoLoss


class TestDiceLoss:
    """Tests for DiceLoss."""

    def test_dice_loss_basic(self):
        """Test basic DiceLoss computation."""
        loss_fn = DiceLoss(from_logits=True, smooth=0.0)

        # Perfect prediction
        pred = torch.ones(2, 1, 10, 10) * 10.0  # High logits
        target = torch.ones(2, 1, 10, 10)
        loss = loss_fn(pred, target)

        assert loss.item() < 0.1, "Loss should be close to 0 for perfect prediction"

    def test_dice_loss_worst_case(self):
        """Test DiceLoss on worst case."""
        loss_fn = DiceLoss(from_logits=True, smooth=0.0)

        # Opposite prediction
        pred = torch.ones(2, 1, 10, 10) * 10.0
        target = torch.zeros(2, 1, 10, 10)
        loss = loss_fn(pred, target)

        assert loss.item() > 0.9, "Loss should be close to 1 for worst prediction"

    def test_dice_loss_shape(self):
        """Test DiceLoss with different shapes."""
        loss_fn = DiceLoss(from_logits=True)

        # Test various batch sizes and image sizes
        for batch_size in [1, 4]:
            for size in [8, 32]:
                pred = torch.randn(batch_size, 1, size, size)
                target = torch.randint(0, 2, (batch_size, 1, size, size)).float()
                loss = loss_fn(pred, target)

                assert loss.item() >= 0.0, "Loss should be non-negative"
                assert loss.item() <= 1.0, "Loss should be at most 1"


class TestSDFWeightedBCELoss:
    """Tests for SDFWeightedBCELoss."""

    def test_sdf_weighted_bce_basic(self):
        """Test basic SDFWeightedBCELoss computation."""
        loss_fn = SDFWeightedBCELoss(reduction="mean", normalize=True)

        # Create simple mask
        pred = torch.zeros(1, 1, 10, 10)
        pred[0, 0, 3:7, 3:7] = 5.0  # High logits for center square

        target = torch.zeros(1, 1, 10, 10)
        target[0, 0, 3:7, 3:7] = 1.0

        loss = loss_fn(pred, target)

        assert torch.isfinite(loss), "Loss should be finite"
        assert loss.item() >= 0.0, "Loss should be non-negative"

    def test_sdf_weighted_bce_reduction(self):
        """Test different reduction modes."""
        pred = torch.randn(2, 1, 8, 8)
        target = torch.randint(0, 2, (2, 1, 8, 8)).float()

        for reduction in ["mean", "sum", "none"]:
            loss_fn = SDFWeightedBCELoss(reduction=reduction)
            loss = loss_fn(pred, target)

            if reduction == "none":
                assert loss.shape == pred.shape, (
                    f"Shape mismatch for reduction={reduction}"
                )
            else:
                assert loss.dim() == 0, f"Should be scalar for reduction={reduction}"

    def test_sdf_weighted_bce_clip_negatives(self):
        """Test clip_negatives parameter."""
        pred = torch.randn(1, 1, 8, 8)
        target = torch.randint(0, 2, (1, 1, 8, 8)).float()

        loss_fn_clip = SDFWeightedBCELoss(clip_negatives=True)
        loss_fn_no_clip = SDFWeightedBCELoss(clip_negatives=False)

        loss_clip = loss_fn_clip(pred, target)
        loss_no_clip = loss_fn_no_clip(pred, target)

        assert torch.isfinite(loss_clip), "Loss should be finite with clipping"
        assert torch.isfinite(loss_no_clip), "Loss should be finite without clipping"


class TestSDFWeightedDiceLoss:
    """Tests for SDFWeightedDiceLoss."""

    def test_sdf_weighted_dice_basic(self):
        """Test basic SDFWeightedDiceLoss computation."""
        loss_fn = SDFWeightedDiceLoss(from_logits=True, normalize=True)

        pred = torch.randn(2, 1, 10, 10)
        target = torch.randint(0, 2, (2, 1, 10, 10)).float()

        loss = loss_fn(pred, target)

        assert torch.isfinite(loss), "Loss should be finite"
        assert loss.item() >= 0.0, "Loss should be non-negative"

    def test_sdf_weighted_dice_inheritance(self):
        """Test that SDFWeightedDiceLoss inherits from DiceLoss."""
        loss_fn = SDFWeightedDiceLoss()
        assert isinstance(loss_fn, DiceLoss), "Should inherit from DiceLoss"


class TestDiSCoLoss:
    """Tests for DiSCoLoss."""

    def test_disco_loss_basic(self):
        """Test basic DiSCoLoss computation."""
        loss_fn = DiSCoLoss(normalize=True, baseloss_weight=0, sdfweighted_weight=1)

        pred = torch.randn(2, 1, 10, 10)
        target = torch.randint(0, 2, (2, 1, 10, 10)).float()

        loss = loss_fn(pred, target)

        assert torch.isfinite(loss), "Loss should be finite"
        assert loss.item() >= 0.0, "Loss should be non-negative"

    def test_disco_loss_weights(self):
        """Test DiSCoLoss with different weight combinations."""
        pred = torch.randn(2, 1, 10, 10)
        target = torch.randint(0, 2, (2, 1, 10, 10)).float()

        # Test different weight combinations
        for base_w, sdf_w in [(0, 1), (1, 0), (1, 1), (0.5, 0.5)]:
            loss_fn = DiSCoLoss(baseloss_weight=base_w, sdfweighted_weight=sdf_w)
            loss = loss_fn(pred, target)

            assert torch.isfinite(loss), (
                f"Loss should be finite for weights ({base_w}, {sdf_w})"
            )

    def test_disco_loss_components(self):
        """Test that DiSCoLoss uses all components."""
        loss_fn = DiSCoLoss(baseloss_weight=1, sdfweighted_weight=1)

        # Verify that all sub-losses are created
        assert hasattr(loss_fn, "bceloss"), "Should have bceloss"
        assert hasattr(loss_fn, "diceloss"), "Should have diceloss"
        assert hasattr(loss_fn, "sdfwbce"), "Should have sdfwbce"
        assert hasattr(loss_fn, "sdfwdice"), "Should have sdfwdice"


class TestGradientFlow:
    """Tests for gradient flow through losses."""

    @pytest.mark.parametrize(
        "loss_class",
        [
            DiceLoss,
            SDFWeightedBCELoss,
            SDFWeightedDiceLoss,
            DiSCoLoss,
        ],
    )
    def test_gradient_flow(self, loss_class):
        """Test that gradients flow through the loss."""
        if loss_class == DiceLoss:
            loss_fn = loss_class(from_logits=True)
        else:
            loss_fn = loss_class()

        pred = torch.randn(2, 1, 8, 8, requires_grad=True)
        target = torch.randint(0, 2, (2, 1, 8, 8)).float()

        loss = loss_fn(pred, target)
        loss.backward()

        assert pred.grad is not None, (
            f"Gradients should flow through {loss_class.__name__}"
        )
        assert torch.isfinite(pred.grad).all(), (
            f"Gradients should be finite for {loss_class.__name__}"
        )


class TestEdgeCases:
    """Tests for edge cases."""

    def test_empty_mask(self):
        """Test with empty (all zeros) mask."""
        loss_fn = DiceLoss(from_logits=True, smooth=1.0)

        pred = torch.zeros(1, 1, 10, 10)
        target = torch.zeros(1, 1, 10, 10)

        loss = loss_fn(pred, target)
        assert torch.isfinite(loss), "Loss should be finite for empty masks"

    def test_full_mask(self):
        """Test with full (all ones) mask."""
        loss_fn = DiceLoss(from_logits=True, smooth=1.0)

        pred = torch.ones(1, 1, 10, 10) * 10.0
        target = torch.ones(1, 1, 10, 10)

        loss = loss_fn(pred, target)
        assert torch.isfinite(loss), "Loss should be finite for full masks"

    def test_single_pixel(self):
        """Test with single pixel mask."""
        loss_fn = SDFWeightedBCELoss()

        pred = torch.zeros(1, 1, 10, 10)
        pred[0, 0, 5, 5] = 5.0

        target = torch.zeros(1, 1, 10, 10)
        target[0, 0, 5, 5] = 1.0

        loss = loss_fn(pred, target)
        assert torch.isfinite(loss), "Loss should be finite for single pixel"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
