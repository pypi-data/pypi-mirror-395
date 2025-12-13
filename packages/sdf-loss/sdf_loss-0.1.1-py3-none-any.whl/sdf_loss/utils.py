from typing import Literal
from typing import Any

import numpy as np
import torch
from scipy.ndimage import distance_transform_edt as distance
from skimage.segmentation import find_boundaries
from torch import Tensor


def compute_sdf(binary_mask: Any, normalize=True) -> Tensor:
    """Compute the signed distance map of binary mask.

    :param input: segmentation, shape = (num_channels, x, y) or (x, y)
    :param output: the Signed Distance Map (SDM)
    :return: the Signed Distance Map (SDM). Result currently normalized sdf to [-1,1].

    :Notes: Inspired by source https://github.com/JunMa11/SegWithDistMap/blob/master/code/train_LA_MultiHead_SDF_L1.py .

    """
    binary_mask = np.asarray(binary_mask).astype(np.float64)

    ## if not binary mask, really makes trouble so raise error if not just 0 and 1
    if not np.all(np.isin(binary_mask, [0, 1])):
        raise ValueError(
            f"Binary mask should only contain 0 and 1. Found {np.unique(binary_mask)}"
        )

    sdf = np.zeros(binary_mask.shape)

    if len(binary_mask.shape) > 2:
        for b in range(binary_mask.shape[0]):
            sdf[b] = compute_sdf(binary_mask[b], normalize=normalize)
        ## convert to tensor if needed
        return torch.tensor(sdf, dtype=torch.float32)

    if np.all(binary_mask == 0):
        ## If empty mask, all pixels are outside (negative SDF)
        return -torch.ones(binary_mask.shape, dtype=torch.float32)
    elif np.all(binary_mask == 1):
        ## If full mask, all pixels are inside (positive SDF)
        return torch.ones(binary_mask.shape, dtype=torch.float32)

    negmask = 1 - binary_mask

    # ========== DTYPE FIX START ==========
    # - torch.tensor(distance(...)) was creating float64 tensors by default
    # + explicitly convert to float32 to match pred dtype and avoid "Found dtype Double but expected Float" error
    dist_to_background = torch.tensor(distance(binary_mask), dtype=torch.float32)
    dist_to_foreground = torch.tensor(distance(negmask), dtype=torch.float32)
    # ========== DTYPE FIX END ==========

    if normalize:
        dist_to_foreground_normalized = dist_to_foreground / torch.max(
            dist_to_foreground
        )
        dist_to_background_normalized = dist_to_background / torch.max(
            dist_to_background
        )
        ## Do normalization to [-1, 1] here - positive inside, negative outside
        sdf = dist_to_background_normalized - dist_to_foreground_normalized
    else:
        sdf = dist_to_background - dist_to_foreground

    ## Set boundary to 0 (usually, it is set to -1)
    boundary = torch.tensor(
        find_boundaries(binary_mask, mode="inner"), dtype=torch.float32
    )
    sdf[boundary == 1] = 0
    return sdf


def sdf_difference_weighted_bceloss_from_logits(
    pred,
    target,
    reduction: Literal["mean", "sum", "none"] = "mean",
    normalize: bool = True,
    clip_negatives=False,
):
    """
    Compute the weighted binary cross entropy loss with respect to the SDF.
    """
    bce_map = torch.nn.functional.binary_cross_entropy_with_logits(
        pred, target, reduction="none"
    )
    sdf_diff = sdf_difference_map(
        pred > 0, target, normalize=normalize, clip_negatives=clip_negatives
    )
    if reduction == "mean":
        return torch.mean(bce_map * sdf_diff)
    elif reduction == "sum":
        return torch.sum(bce_map * sdf_diff)
    elif reduction == "none":
        return bce_map * sdf_diff


def sdf_difference_map(mask1, mask2, normalize=True, clip_negatives=False):
    device = mask1.device
    # Binarize masks to handle both binary and probability inputs
    mask1_binary = (mask1 > 0.5).float()
    mask2_binary = (mask2 > 0.5).float()
    sdf1 = compute_sdf(mask1_binary.numpy(force=True), normalize=normalize)
    sdf2 = compute_sdf(mask2_binary.numpy(force=True), normalize=normalize)
    if clip_negatives:
        sdf1[sdf1 < 0] = 0
        sdf2[sdf2 < 0] = 0
    return torch.abs(sdf1 - sdf2).to(device)
