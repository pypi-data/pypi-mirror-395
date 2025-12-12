"""
This submodule contains custom data types.

Some datatypes are Annotated for more clear typing within the codebase
others use Pydantic to ease serialising for caching to disk.
"""

from typing import Annotated
from enum import IntEnum

import numpy as np
from pydantic import BeforeValidator, BaseModel, PlainSerializer, RootModel


class ImageType(IntEnum):
    """An enum for image types OFSImage.filetype"""

    JPG = 0
    TIFF = 1
    PNG = 2
    GIF = 3
    BMP = 4


# Type annotations to help with serialising numpy vectors and matrices.
_Number = int | float
_NestedListOfNumbers = _Number | list[_Number] | list[list[_Number]]


class _NestedListOfNumbersModel(RootModel):
    root: _NestedListOfNumbers


def _np_to_listoflists(arr: np.ndarray) -> _NestedListOfNumbers:
    """Convert a numpy array to a list of lists

    Note: this will not be quick! Large arrays will be much better
    serialised by dumping to base64 encoding or similar.
    """
    return arr.tolist()


def _listoflists_to_np(lol: _NestedListOfNumbers) -> np.ndarray:
    """Convert a list of lists to a numpy array"""
    return np.asarray(lol)


NDArray = Annotated[
    np.ndarray,
    BeforeValidator(_listoflists_to_np),
    PlainSerializer(_np_to_listoflists, when_used="json-unless-none"),
]
"""Define an annotated type so Pydantic can serialise and validate with numpy arrays"""


PairKeys = tuple[str, str]
"""A tuple of two image keys a pair of images"""


XYDisplacementInPixels = tuple[float, float]
"""A tuple of the xy displacement between two image in pixels"""


class PairData(BaseModel):
    """The results of correlating images together

    For convenience this also includes an estimate of the displacement between
    images as estimated from the stage coordinates and the transform matrix.
    """

    keys: PairKeys
    image_displacement: XYDisplacementInPixels
    stage_displacement: XYDisplacementInPixels
    # The proportion of pixels in the correlation image beneath a threshold
    fraction_under_threshold: dict[float, float]
