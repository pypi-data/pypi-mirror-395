"""
This submodule contains the top level settings for controlling how the program
runs.
"""

from typing import Literal, Optional
from pydantic import BaseModel, ConfigDict


class LoadingSettings(BaseModel):
    """Settings that affect how images and their metadata are loaded"""

    csm_matrix: Optional[list[list[float]]] = None
    """Specifies the camera to sample matrix, will override any set in file"""
    csm_calibration_width: Optional[int] = None
    """Sets width of the images used to calibrate the camera to sample matrix
    this is needed if the csm matrix was calculated with a different size image
    to the images to be stitched.
    """
    model_config = ConfigDict(extra="forbid")
    """This is a Pydantic BaseModel variable. It doesn't need to be altered."""


class TilingSettings(BaseModel):
    """The settings for tiling  i.e. position optimisation once correlations
    have been calculated
    """

    thresholding_method: Literal["automatic", "manual"] = "automatic"
    """Used to chage from the default automatic thresholding to a manual mode
    where the execution pauses for user input.
    """
    max_stage_discrepancy: Optional[float] = None
    """Set the starting threshold for stage discrepancy."""
    min_peak_quality: Optional[float] = None
    """Set the starting threshold for peak quality."""
    model_config = ConfigDict(extra="forbid")
    """This is a Pydantic BaseModel variable. It doesn't need to be altered."""


class CorrelationSettings(BaseModel):
    """Input parameters that affect the estimation of image-to-image displacements
    as calculated by cross correlation.
    """

    pad: bool = True
    """"Zero-pad before Fourier transforming if  True (default).
    
    Zero padding disambiguates peaks in cross-correlation, but is slower
    """

    resize: float = 1.0
    """"Images are scaled by this factor before performing FFT."""

    high_pass_sigma: float = 10.0
    """"Strength of the high pass filter to apply (larger _Number = more low frequencies cut)"""

    minimum_overlap: float = 0.2
    """Minimum overlap area to count as overlapping, as a fraction of the image"""

    priority: Literal["time", "memory"] = "time"
    """Optimise for minimal memory usage, or shortest time (default).
    
    By default images that need to be used again are cached memory. "memory" option
    disables this.
    """
    model_config = ConfigDict(extra="forbid")
    """This is a Pydantic BaseModel variable. It doesn't need to be altered."""


class OutputSettings(BaseModel):
    """Settings that affect how images stitched and saved once positions have been
    calculated

    This only affects the full pipeline:
    `openflexure_stitching.pipeline.load_tile_and_stitch`
    """

    output_dir: str = "."
    """The output directory for stitched files."""
    stitching_mode: str = "all"
    """The stitching mode. See pipeline docs for more details"""
    stitch_tiff: bool = False
    """
    Set true to save a pyramidal TIFF
    """
    dzi: bool = False
    """
    Set true to save a pyramidal DZI
    """
    legacy_mode: bool = False
    """Legacy mode is set true to enable legacy behaviour where preview images
    were named "stitched_from_stage.jpg" even though they were calculated from
    the optimisation.
    """
    tile_size: int | Literal["auto"] = "auto"
    """If stitching with pyvips, what tile size to use to produce the composite
    image. If a float, will be used in both x and y. Using a power of two is
    strongly recommended, with memory implications explained in stitch.py.
    'Auto' will use free memory to choose a tile size.
    """
    model_config = ConfigDict(extra="forbid")
    """This is a Pydantic BaseModel variable. It doesn't need to be altered."""
