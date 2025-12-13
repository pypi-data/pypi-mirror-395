"""
This submodule provides functionallity for applying and fitting affine
transforms
"""

import numpy as np

from openflexure_stitching.types import PairData


def apply_affine_transform(
    pairs: list[PairData],
    transform: np.ndarray,
) -> list[PairData]:
    """Apply an affine transform to the stage coordinates in pair data"""
    inverse_transform = np.linalg.inv(transform)
    return [
        PairData(
            keys=p.keys,
            image_displacement=p.image_displacement,
            stage_displacement=tuple(np.dot(p.stage_displacement, inverse_transform)),
            fraction_under_threshold=p.fraction_under_threshold,
        )
        for p in pairs
    ]


def fit_affine_transform(
    correlations: list[PairData],
):
    """Find an affine transform to convert from stage positions to pixel.

    Find an affine tranform (i.e. 2x2 matrix) that, when applied to the
    stage coordinates (in `correlations`), matches the measured pair-wise
    displacements in `correlations` as closely as possible.
    This can be used to refine the camera-stage-mapping matrix.

    Arguments:
    Result: numpy.ndarray, numpy.ndarray
        A 2x2 matrix that transforms the given stage coordinates to match the
        pixel positions.
    """
    image_displacements = np.array([c.image_displacement for c in correlations])
    stage_displacements = np.array([c.stage_displacement for c in correlations])

    affine_transform = np.linalg.lstsq(image_displacements, stage_displacements, rcond=-1)[0]

    return affine_transform
