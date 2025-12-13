"""
Manage cache files that include correlation results, and images metadata.

It is recommended to use
`openflexure_stitching.pipeline.load_and_cache_correlated_image_set`
rather than the function in this sub-module directly.
"""

from typing import Optional
import os

from pydantic import BaseModel, RootModel, ValidationError

from openflexure_stitching.settings import CorrelationSettings
from openflexure_stitching.types import PairData
from .image import CachedOFSImage
from .image_sets import CachedCorrelatedImageSet


class CorrelationCache(BaseModel):
    """
    The pydantic model used to serialise and validate the cached files.
    """

    images: dict[str, CachedOFSImage]
    """A dictionary of the cached image metadata"""
    correlations: list[tuple[CorrelationSettings, list[PairData]]]
    """A list of tuples. Each tuple contains the correlation settings and the
    associated pair data for those settings."""

    def index_of_correlations(self, correlation_settings: CorrelationSettings) -> Optional[int]:
        """
        A helper method to find the index of the tuple with matching correlation settings

        :param correlation_settings: The correlation_settings to match.

        :return: The index of the tuple with these correlation settings or `None` if no index
        is found.
        """
        for i, (cached_settings, _) in enumerate(self.correlations):
            if cached_settings == correlation_settings:
                return i
        return None


def cache_path(folder: str) -> str:
    """The location where the cache is stored

    :param folder: the directory of the images being loaded.

    :return: the path to the cache for this folder of images.
    """
    return os.path.join(folder, "openflexure_stitching_cache.json")


def _write_cache(folder: str, data: CorrelationCache):
    """Save the cache to the default location"""
    with open(cache_path(folder), "w", encoding="utf-8") as file_obj:
        file_obj.write(RootModel[CorrelationCache](data).model_dump_json(indent=4))


def _read_cache(folder: str) -> Optional[CorrelationCache]:
    """Read the cache from the default location"""
    cache_filepath = cache_path(folder)
    if not os.path.exists(cache_filepath):
        return None

    try:
        with open(cache_filepath, "r", encoding="utf-8") as file_obj:
            return CorrelationCache.model_validate_json(file_obj.read())
    except ValidationError as e:
        raise CacheFailureException("The cache file had the wrong structure.") from e


def load_cached_correlated_image_set(
    folder: str, correlation_settings: Optional[CorrelationSettings]
) -> Optional[CachedCorrelatedImageSet]:
    """
    Load a `.CachedCorrelatedImageSet` with matching correlation settings from the
    cache on disk. If `None` is returned, then no cached data with the input settings is
    available.

    :param folder:  the directory of the images being loaded.
    :param correlation_settings: The correlation_settings to of the requested cached
    data

    :return: The CachedCorrelatedImageSet or None if not available.
    """
    if correlation_settings is None:
        correlation_settings = CorrelationSettings()
    full_cache = _read_cache(folder)
    if full_cache is None:
        return None
    index = full_cache.index_of_correlations(correlation_settings)
    if index is None:
        return None
    return CachedCorrelatedImageSet(
        images=full_cache.images,
        correlation_settings=full_cache.correlations[index][0],
        pairs=full_cache.correlations[index][1],
    )


def save_cached_correlated_image_set(
    folder: str, cached_image_set: CachedCorrelatedImageSet
) -> None:
    """
    save a `.CachedCorrelatedImageSet` to the cache on disk.

    :param folder: the directory the images were loaded from, and for the cache to be
    written to.
    :param cached_image_set: The `.CachedCorrelatedImageSet` containing the data to be
    cached.
    """
    full_cache = _read_cache(folder)

    # The cache saves correlations as a list of tuples of seetings and pair data. So multiple sets
    # of settings can be cached
    correlation_tuple = (cached_image_set.correlation_settings, cached_image_set.pairs)

    if full_cache is None:
        full_cache = CorrelationCache(
            images=cached_image_set.images, correlations=[correlation_tuple]
        )
    else:
        # Add the new images to the cache prioritising new data (See PEP 584 for |= syntax)
        full_cache.images |= cached_image_set.images
        index = full_cache.index_of_correlations(cached_image_set.correlation_settings)
        if index is None:
            full_cache.correlations.append(correlation_tuple)
        else:
            full_cache.correlations[index] = correlation_tuple
    _write_cache(folder, full_cache)


class CacheFailureException(Exception):
    """The exception raised if the cache cannot be parsed or validated"""
