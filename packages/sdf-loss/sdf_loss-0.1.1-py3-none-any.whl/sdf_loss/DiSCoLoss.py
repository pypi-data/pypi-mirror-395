import torch

from .DiceLoss import DiceLoss
from .SDFWeightedBCELoss import SDFWeightedBCELoss
from .SDFWeightedDiceLoss import SDFWeightedDiceLoss


class DiSCoLoss(torch.nn.Module):
    def __init__(
        self,
        normalize=True,
        baseloss_weight=1,
        sdfweighted_weight=1,
        clip_negatives=True,
    ):
        """Distance-scaled combination loss putting heavier penalty on fp or fn objects. From logits."""
        super().__init__()
        self.baseloss_weight = baseloss_weight
        self.sdfweighted_weight = sdfweighted_weight
        self.bceloss = torch.nn.BCEWithLogitsLoss()
        self.diceloss = DiceLoss()
        self.sdfwbce = SDFWeightedBCELoss(
            reduction="mean", normalize=normalize, clip_negatives=clip_negatives
        )
        self.sdfwdice = SDFWeightedDiceLoss(
            from_logits=True, normalize=normalize, clip_negatives=clip_negatives
        )
        self.clip_negatives = clip_negatives

    def forward(self, pred, target):
        baseloss = self.bceloss(pred, target) + self.diceloss(pred, target)
        sdf_weighted_loss = self.sdfwbce(pred, target) + self.sdfwdice(pred, target)
        total_loss = (
            self.baseloss_weight * baseloss
            + self.sdfweighted_weight * sdf_weighted_loss
        )
        return total_loss
