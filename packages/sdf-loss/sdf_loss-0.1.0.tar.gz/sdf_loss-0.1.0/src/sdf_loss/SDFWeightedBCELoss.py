import torch
from typing import Literal
from .utils import sdf_difference_weighted_bceloss_from_logits


class SDFWeightedBCELoss(torch.nn.Module):
    """
    Compute binary cross entropy loss, pixel wise weighted by the absolute difference
    of the signed distance function of the prediction and the label.

    Args:
        reduction: Specifies the reduction to apply to the output: 'none' | 'mean' | 'sum'.
        normalize: If True, the SDF is normalized to the range [-1, 1] where 0 is along the object boundaries.
    """

    def __init__(
        self,
        reduction: Literal["mean", "sum", "none"] = "mean",
        normalize: bool = True,
        clip_negatives=False,
    ):
        super().__init__()
        self.reduction = reduction
        self.normalize = normalize
        self.clip_negatives = clip_negatives

    def forward(self, pred, target):
        return sdf_difference_weighted_bceloss_from_logits(
            pred,
            target,
            reduction=self.reduction,
            normalize=self.normalize,
            clip_negatives=self.clip_negatives,
        )
