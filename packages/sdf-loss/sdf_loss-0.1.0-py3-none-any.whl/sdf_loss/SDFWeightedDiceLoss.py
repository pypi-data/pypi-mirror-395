from functools import partial
from .DiceLoss import DiceLoss
from .utils import sdf_difference_map


class SDFWeightedDiceLoss(DiceLoss):
    def __init__(
        self,
        from_logits=True,
        normalize=True,
        clip_negatives=False,
    ):
        super().__init__(
            weight_func=partial(
                sdf_difference_map, normalize=normalize, clip_negatives=clip_negatives
            ),
            from_logits=from_logits,
        )
