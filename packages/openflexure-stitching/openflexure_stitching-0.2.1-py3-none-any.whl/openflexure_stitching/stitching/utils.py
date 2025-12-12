"""Utility functions used by the stitching methods"""

from typing import Optional
import numpy as np


def overlap_slice(shift: int, width: int) -> Optional[slice]:
    """Return a range over which two images overlap in 1D

    shift should be the centre-to-centre shift of two windows, which
    have a width of `width`. This will return a range, giving the
    coordinates in the first window that are overlapped.

    If there is no overlap, we get None.
    """
    if np.abs(shift) >= width:
        return None
    if shift > 0:
        return slice(int(shift), int(width))
    return slice(0, int(shift) + int(width))


def overlap_slices(displacement, size) -> list[slice | None]:
    """Return ranges for the overlapping region of an image

    Given a 2D centre to centre displacement, and a 2D size,
    return two ranges for the overlaps.
    """
    return [overlap_slice(displacement[i], size[i]) for i in range(2)]


def arange_from_slice(s: slice) -> np.ndarray:
    """Convert a slice to a np.arange"""
    return np.arange(s.start, s.stop, s.step, dtype=float)


def downsample_image(tile: np.ndarray, downsample: int, shift=(0, 0)) -> np.ndarray:
    """Crudely downsample an image

    This picks every `downsample`-th pixel, i.e. does no averaging.
    """
    width, height, dims = tile.shape
    img = np.zeros((width // downsample - 1, height // downsample - 1, dims), dtype=int)
    img = tile[
        int(shift[0]) : int(shift[0] + downsample * img.shape[0]) : downsample,
        int(shift[1]) : int(shift[1] + downsample * img.shape[1]) : downsample,
        :,
    ]
    return img


RegionOfInterest = tuple[tuple[int, int], tuple[int, int]]


def regions_overlap(a: RegionOfInterest, b: RegionOfInterest) -> bool:
    """Determine whether two regions overlap

    Regions are tuples of ((x, y), (width, height))
    """
    for d in range(2):
        if a[0][d] >= b[0][d] + b[1][d]:
            # the ROI a starts after ROI b finishes
            return False
        if b[0][d] >= a[0][d] + a[1][d]:
            # the ROI b starts after ROI a finishes
            return False
    return True
