import torch
import torch.nn as nn


class DiceLoss(nn.Module):
    """Diceloss

    Mod of SMP's dice loss with added weight function (allowing for dynamic pixel-wise weighting).
    """

    def __init__(self, weight_func=None, from_logits=True, smooth=0.0):
        super().__init__()
        self.weight_func = weight_func
        self.smooth = smooth
        self.eps = 1e-7
        self.from_logits = from_logits

    def forward(self, pred, target):
        assert pred.size() == target.size()
        if self.from_logits:
            pred = torch.sigmoid(pred)

        if self.weight_func is not None:
            w = self.weight_func(pred, target)
        else:
            w = 1.0
        num = 2 * (w * pred * target).sum() + self.smooth
        den = ((w * pred + w * target).sum() + self.smooth).clamp(min=self.eps)
        return 1.0 - (num / den)
