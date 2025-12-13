"""
This submodule handles loading images and image sets from directories (folders)

Images can be loaded as `OFSImage` objects, only metadata is stored in memory until
the image data is accessed. This can be optionally cached for later use.

A whole directory can be loaded into an `OFSImageSet` object, by initialising a
class. The image data is only loaded when as needed to minimise the memory overhead.

For stitching images based on positions optimised from comparing images (rather than
just stage coordinates), a child class `CorrelatedImageSet` can be used.

As the `CorrelatedImageSet` performs cross-correlations between each pair of images
on initialisation this can be slow to initialise. Both `OFSImageSet` and
`CorrelatedImageSet` can have their key data exported to a serialisable object
`CachedOFSImageSet` or  `CachedCorrelatedImageSet` and be reloaded from these.

OpenFlexure Stitching has a caching system for automatically loading and saving
`CorrelatedImageSets` to a cache in the image directory. See
`openflexure_stitching.pipeline.load_and_cache_correlated_image_set`
"""

__all__ = [
    "OFSImage",
    "OFSImageSet",
    "CorrelatedImageSet",
    "load_cached_correlated_image_set",
    "save_cached_correlated_image_set",
    "CachedOFSImage",
    "CachedOFSImageSet",
    "CachedCorrelatedImageSet",
    "MetaDataError",
]


from .image import OFSImage, CachedOFSImage, MetaDataError

from .image_sets import (
    OFSImageSet,
    CorrelatedImageSet,
    CachedOFSImageSet,
    CachedCorrelatedImageSet,
)

from .cache import load_cached_correlated_image_set, save_cached_correlated_image_set
