from __future__ import annotations
import numpy as np
from typing import NamedTuple, Tuple


class Crop2D(NamedTuple):
    data: np.ndarray
    bbox_ij: Tuple[int, int, int, int]   # (i0, i1, j0, j1)


def crop_above_threshold_2d(
    arr: np.ndarray,
    threshold: float,
    pad: int = 0,
    *,
    strict: bool = True
) -> Crop2D:
    """
    Crop a 2D NumPy array to the minimal bounding region where values
    are above (or >=) the threshold.

    Returns the cropped array and bounding box indices (i0, i1, j0, j1).
    """

    v = np.asarray(arr, dtype=float)
    if v.ndim != 2:
        raise ValueError(f"Array must be 2D, got shape={v.shape}")

    cmp = (v > threshold) if strict else (v >= threshold)
    mask = cmp & np.isfinite(v)

    if not mask.any():
        cond = ">" if strict else ">="
        raise ValueError(f"No pixels {cond} {threshold!r}")

    # Find rows & columns containing valid pixels
    rows = np.where(mask.any(axis=1))[0]
    cols = np.where(mask.any(axis=0))[0]

    i0, i1 = rows[0], rows[-1] + 1   # row start / end+1
    j0, j1 = cols[0], cols[-1] + 1   # col start / end+1

    # Padding
    if pad > 0:
        i0 = max(0, i0 - pad)
        j0 = max(0, j0 - pad)
        i1 = min(v.shape[0], i1 + pad)
        j1 = min(v.shape[1], j1 + pad)

    cropped = v[i0:i1, j0:j1].copy()

    return Crop2D(data=cropped, bbox_ij=(i0, i1, j0, j1))
