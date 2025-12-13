"""OpenFlexure Stitching

This package takes  a collection of images with metadata about the stage
position (i.e. image translation) and uses it to produce a stitched image
suitable for histopathology slides, or other microscopic imaging
applications requiring a large field of view. It is optimised to be
memory-efficient (occasionally offering a trade-off between speed and
memory footprint) and to work with low cost translation stages.

The general pattern for use is:

* Load images and metadata
* Identify overlapping images
* Cross-correlate them
* Filter the correlations to remove errors
* Optimise the position of images
* Stitch the images into the final output

An [example notebook showing how to debug is also available](./DebuggingExample.html).

"""

from openflexure_stitching.settings import (
    LoadingSettings,
    CorrelationSettings,
    TilingSettings,
    OutputSettings,
)
from openflexure_stitching.pipeline import load_tile_and_stitch
from openflexure_stitching.loading import OFSImage, OFSImageSet, CorrelatedImageSet

from openflexure_stitching import correlation
from openflexure_stitching import stitching
