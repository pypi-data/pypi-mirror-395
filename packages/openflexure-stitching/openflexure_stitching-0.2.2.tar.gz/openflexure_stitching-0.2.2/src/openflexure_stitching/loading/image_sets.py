"""
This submodule handles loading images from directories (folders), into ImageSets.

The public classes in this submodule are designed to be accessed via

openflexure_stitching.loading directly.
"""

from copy import copy
from typing import Optional, Literal, overload
import os

import numpy as np
from pydantic import BaseModel

from camera_stage_mapping.fft_image_tracking import high_pass_fourier_mask

from openflexure_stitching.types import PairKeys, PairData, XYDisplacementInPixels
from openflexure_stitching.settings import LoadingSettings, CorrelationSettings
from openflexure_stitching.correlation import displacement_from_crosscorrelation

from .image import OFSImage, CachedOFSImage


class CachedOFSImageSet(BaseModel):
    """
    A serialisable Pydantic model of the key information needed to
    reconstruct an `OFSImageSet`.

    See `OFSImageSet.data_for_caching`
    """

    images: dict[str, CachedOFSImage]


class CachedCorrelatedImageSet(BaseModel):
    """
    A serialisable Pydantic model of the key information needed to
    reconstruct a `CorrelatedImageSet`.

    See `CorrelatedImageSet.data_for_caching`
    """

    images: dict[str, CachedOFSImage]
    correlation_settings: CorrelationSettings
    pairs: list[PairData]


AnyCachedImageSet = CachedOFSImageSet | CachedCorrelatedImageSet
"""Type hint for CachedOFSImageSet or CachedCorrelatedImageSet"""


class OFSImageSet:
    """
    `OFSImageSet` is the main class for handling groups of images to be stitched.

    Usually its child class `CorrelatedImageSet` is used as this also contains
    the pairwise comparison of overlapping images.

    Both `OFSImageSet` and `CorrelatedImageSet` require all the images to be stitched
    to be in the same directory. The directory path is passed to the image set on
    initialisation. All images within the set can then be accessed by their filename:

    ```python
    image_set = OFSImageSet("my_scans/scan1/images")
    image1 = image_set["image_0_0.jpg"]
    ```
    In this case `image1` will be an `.image.OFSImage`

    The number of images of the image set can be found with `len(image_set)` and the
    set can be iterated over as:
    ```python
    for image in image_set:
        if image.from_openflexure:
            print("Great choice of microscope!")
    ```

    For a list of all `keys` (i.e. filenames for indexing) see `OFSImageSet.keys`

    """

    cache_stats: dict
    """Caching statistics in a dictionary. Useful for debugging and testing"""

    def __init__(
        self,
        folder: str,
        *,
        loading_settings: Optional[LoadingSettings] = None,
        cached: Optional[AnyCachedImageSet] = None,
    ):
        """Load images from the input folder, optionally load some from a cached object

        :param folder: The folder or directory to load the images from. Not that only the
        metadata is loaded into memory. Image data is not loaded until requested, it can be
        cached in memory once loaded, if required.

        :param loading_settings: *Optional* Override the default loading settings for
        each images. This can be used, for example, to set a camera to sample matrix for
        each image if one isn't included in their metadata.

        :param cached: *Optional* Cached data to speed up reloading images. Any images that
        are in the folder but not in the cache will be loaded from disk.
        """

        if loading_settings is None:
            loading_settings = LoadingSettings()

        self._folder = folder
        fnames = find_images(folder)
        if len(fnames) < 2:
            raise RuntimeError("Not enough images to stitch, check your file path")

        self._images: dict[str, OFSImage] = {}

        self.cache_stats = {"images_loaded_from_disk": 0, "images_loaded_from_cache": 0}

        for image_fname in fnames:
            if cached is not None and image_fname in cached.images:
                image = OFSImage(cached=cached.images[image_fname], cached_folder=folder)
                self.cache_stats["images_loaded_from_cache"] += 1
            else:
                filepath = os.path.join(folder, image_fname)
                image = OFSImage(filepath)
                self.cache_stats["images_loaded_from_disk"] += 1
            # Adjust after loading from cache as the chached CSM is the one loaded from file.
            image.adjust_camera_to_sample_matrix(
                new_csm=loading_settings.csm_matrix,
                new_width=loading_settings.csm_calibration_width,
            )
            self._images[image_fname] = image

        self._check_and_filter_images()

        self._sort_images()

    def __iter__(self):
        """
        Allow iteration over images
        """
        return iter(self._images.values())

    def __len__(self):
        """
        Allow the length of the set to be read.
        """
        return len(self._images)

    def __getitem__(self, key):
        return self._images[key]

    def keys(self):
        """
        List of all keys. This can be used to get an image by indexing the set.
        """
        return list(self._images.keys())

    @property
    def _first_image(self):
        """
        The first image. Used to get properties that should be the same through the set
        """
        # Use next and iter to get the first image
        return next(iter(self))

    @property
    def folder(self) -> str:
        """The directory the images are loaded from."""
        return self._folder

    @property
    def pixel_size_um(self) -> Optional[float]:
        """The size of one pixel in micrometres if known. Otherwise `None`"""
        return self._first_image.pixel_size_um

    @property
    def camera_to_sample_matrix(self) -> Optional[np.ndarray]:
        """The matrix that transforms from stage coordinates to image coordinates in
        pixels, if known.

        Note that most stages use an (x,y) convention but, image processing is performed
        image coordinates that use matrix index ordering which reverses x and y.

        If not known `None` is returned, in this case the matrix that will be used is
        ```
        np.array(
            [[0, 1],
             [1, 0]]
        )
        ```
        """
        return self._first_image.camera_to_sample_matrix

    @property
    def image_shape(self) -> tuple[int, int]:
        """The image shape in pixels as a tuple (height, width)"""
        return (self._first_image.height, self._first_image.width)

    def mean_stage_position_px(self) -> np.ndarray:
        """The mean position of all images from the reported stage position
        but converted into pixels with the `OFSImageSet.camera_to_sample_matrix`
        """
        positions_array = [image.stage_position_px for image in self]
        return np.mean(positions_array, axis=0)

    def stage_displacement_px_between(self, key1: str, key2: str) -> XYDisplacementInPixels:
        """Displacement in pixels between images key1 and key2 estimated from the reported
        stage positions."""
        return self[key1].stage_position_px - self[key2].stage_position_px

    def _check_and_filter_images(self):
        """Performed at setup to check image for consistency and to ensure only
        one image per x,y location"""
        csm = self.camera_to_sample_matrix
        height, width = self.image_shape
        xy_positions = []
        for image in self:
            if image.stage_position is None:
                raise RuntimeError(f"The image {image.filename} has no position set")
            if image.stage_position not in xy_positions:
                xy_positions.append(image.stage_position)

            if not np.allclose(image.camera_to_sample_matrix, csm):
                raise RuntimeError("The images do not have a consistent CSM.")

            if image.height != height or image.width != width:
                raise RuntimeError("The images do not have a consistent shape.")

        # If the length of the xy positions isn't the same as the length of the image
        # set then there are multiple images per xy position (i.e. a z-stack). This
        # needs filtering to only retain the sharpest image.
        if len(xy_positions) != len(self):
            self._filter_stack()

    def _sort_images(self):
        """Sort image list by capture_time if available; otherwise by file creation time."""

        # Check that all images have the capture time attribute
        has_all_capture_times = all(image.capture_time for image in self)

        if has_all_capture_times:
            # Use Exif capture time if all are available
            sorted_images = sorted(self, key=lambda image: image.capture_time)
        else:
            # Else, use file created time, which may be affected by OS operations
            sorted_images = sorted(self, key=lambda image: image.file_created_time)

        self._images = {img.filename: img for img in sorted_images}

    def _filter_stack(self):
        """
        Filter images so that only one remain per z-position
        """
        xy_groups = {}
        for image in self:
            pos = image.stage_position
            if pos not in xy_groups:
                xy_groups[pos] = []
            xy_groups[pos].append(image.filename)

        reduced_image_dict = {}
        for pos, image_keys in xy_groups.items():
            sizes = [self[key].file_size for key in image_keys]
            # Find sharpest by file size comparison
            sharpest_index = sizes.index(max(sizes))
            sharpest_image_key = image_keys[sharpest_index]
            reduced_image_dict[sharpest_image_key] = self[sharpest_image_key]

        # Once calculated the reduced set, replace self._images
        self._images = reduced_image_dict

    def find_overlapping_pairs(self, minimum_overlap: float) -> list[PairKeys]:
        """Identify pairs of images with significant overlap.

        Given the positions (in pixels) of a collection of images (of given size),
        calculate the fractional overlap (i.e. the overlap area divided by the area
        of one image) and return a list of images that have significant overlap.

        :param minimum_overlap: the minimum fraction of the area of the images overlapping
            for them to be returned.

        :return: A list of tuples, where each tuple contains the keys of two images that
        overlap.
        """

        keys = list(self.keys())

        tile_pairs: list[tuple[int, int, float]] = []
        pixel_positions = np.asarray([image.stage_position_px for image in self])
        image_size = np.asarray(self.image_shape)
        for i in range(len(self)):
            for j in range(i + 1, len(self)):
                overlap = image_size - np.abs(pixel_positions[i, :2] - pixel_positions[j, :2])
                overlap[overlap < 0] = 0
                tile_pairs.append((i, j, np.prod(overlap)))
        overlap_threshold = np.prod(image_size) * minimum_overlap
        overlapping_pairs: list[PairKeys] = [
            (keys[i], keys[j]) for i, j, o in tile_pairs if o > overlap_threshold
        ]

        # Sanity checks for the output list of pairs
        for pair in overlapping_pairs:
            if pair[1] == pair[0]:
                raise RuntimeError("An image has been linked to itself!")

        return overlapping_pairs

    def data_for_caching(self) -> AnyCachedImageSet:
        """Return a `CachedOFSImageSet` of the images.

        Subclasses may return other types of Cached Image Set. This can be serialised
        to json as
        ```
        json_str = image_set.data_for_caching().model_dump_json()
        ```

        :return: A `CachedOFSImageSet`, this could be passed into the `cached` parameter
        when creating a new OFSImageSet
        """
        return CachedOFSImageSet(
            images={key: value.data_for_caching() for key, value in self._images.items()}
        )

    def clear_image_memory_cache(self, retain: Optional[list[str]]) -> None:
        """Clear image data and FFTs from the memory cache

        Images can store their image data or their FFTs in memory for reuse. This
        instructs all images not on the retain list to clear their memory.

        :param retain: A list of the image keys for images that should retain their
        memory cached image data.
        """
        if retain:
            keys_to_retain = set(retain)
        else:
            keys_to_retain = set()

        # Disabling pylint warning as it is suggesting using items(). But this
        # class doesn't have items()
        for key in self.keys():  # pylint: disable=consider-using-dict-items
            if key not in keys_to_retain:
                self[key].clear_memory_cache()


class CorrelatedImageSet(OFSImageSet):
    """This class holds a set of images for stitching including the
    pairwise image correlations.

    Calling the constructor identifies overlaps based
    on the stage coordinates, and performs image correlation to
    determine relative displacements between images.

    The correlations can be slow for larger image sets. Caching
    can be used to improve performance. To automatically load from
    cache and save to cache one loaded see
    `openflexure_stitching.pipeline.load_and_cache_correlated_image_set`
    """

    def __init__(
        self,
        folder: str,
        *,
        loading_settings: Optional[LoadingSettings] = None,
        correlation_settings: Optional[CorrelationSettings] = None,
        cached: Optional[AnyCachedImageSet] = None,
    ):
        """
        Load the image set and then perform correlations


        Load images from the input folder, and then perform correlations. Optionally load some
        from a cached object

        :param folder: The folder or directory to load the images from. Not that only the
        metadata is loaded into memory. Image data is not loaded until requested, it can be
        cached in memory once loaded, if required.

        :param loading_settings: *Optional* Override the default loading settings for
        each images. This can be used, for example, to set a camera to sample matrix for
        each image if one isn't included in their metadata.

        :param correlation_settings: *Optional* Override the default correlation settings.
        This can be used, for example, to adjust the minimum overlap between images for them
        to be compared by cross-correlation, or to adjust the high-pass filter applied to
        images during cross-correlation.

        :param cached: *Optional* Cached data to speed up reloading images. Any images that
        are in the folder but not in the cache will be loaded from disk. Any pairs data for
        correlations that are not cached will be calculated.
        """

        if correlation_settings is None:
            self._correlation_settings = CorrelationSettings()
        else:
            self._correlation_settings = correlation_settings

        if (
            isinstance(cached, CachedCorrelatedImageSet)
            and self._correlation_settings != cached.correlation_settings
        ):
            raise ValueError(
                "Cached correlation values were calculated with different correlation settings"
            )

        super().__init__(folder, loading_settings=loading_settings, cached=cached)

        self.cache_stats["correlations_loaded_from_disk"] = 0
        self.cache_stats["correlations_loaded_from_cache"] = 0
        pairs = self._crosscorrelate_all(cached=cached)
        self._pairs = pairs
        # Save discrepancies to memory as they are needed multiple times
        self._pair_discrepancies = []
        self._norm_pair_discrepancies = []
        for pair in self._pairs:
            discrep = np.array(pair.image_displacement) - np.array(pair.stage_displacement)
            self._pair_discrepancies.append(discrep)
            self._norm_pair_discrepancies.append(float(np.linalg.norm(discrep)))

    @property
    def correlation_settings(self):
        """
        The correlation settings used to calculate the pair data in this set.
        """
        return self._correlation_settings

    @property
    def pairs(self) -> list[PairData]:
        """
        A list of PairData objects for each pair of overlapping images. This
        contains the keys of both images, their displacement in pixels as calculated
        from the reported stage position and from cross-correlation. It also contains
        metrics for assessing the quality of the cross-correlation peak.
        """
        return self._pairs

    def _crosscorrelate_all(self, cached: Optional[AnyCachedImageSet]) -> list[PairData]:
        """Estimate displacements between pairs of overlapping images using cross correlation

        For each pair of overlapping images, perform a cross-correlation to fine-tune the
        displacement between them. Return a list of PairData for the correlations
        """

        cached_pairs = cached.pairs if isinstance(cached, CachedCorrelatedImageSet) else []
        cached_pair_keys = [pair.keys for pair in cached_pairs]

        remaining_pairs = self.find_overlapping_pairs(self.correlation_settings.minimum_overlap)

        pair_data: list[PairData] = []

        cache_img_in_memory: bool = self.correlation_settings.priority == "time"

        # Load the first image, to determine size and allow us to calculate the Fourier
        # filter applied to each correlation
        example_fft = self._first_image.fft(
            resize=self.correlation_settings.resize,
            pad=self.correlation_settings.pad,
            cache_in_memory=False,
            cache_img_in_memory=cache_img_in_memory,
        )
        high_pass_filter = high_pass_fourier_mask(
            example_fft.shape, self.correlation_settings.high_pass_sigma
        )

        # Loop and pop this way we have the shortened list for checking remaining
        while remaining_pairs:
            # Pylint is concerned about the arguments for
            # self.stage_displacement_px_between being (key2, key1) not
            # (key1, key2), as this is the name of the definition arguments.
            # But this is correct, so disabling the warning locally.
            # pylint: disable=arguments-out-of-order

            key1, key2 = remaining_pairs.pop(0)

            # Load from cache if available
            if (key1, key2) in cached_pair_keys:
                cache_index = cached_pair_keys.index((key1, key2))
                cached_pair = cached_pairs[cache_index]
                # Recalculate stage displacement as loading settings are not cached
                # so CSM may have been adjusted.
                pair_data.append(
                    PairData(
                        keys=cached_pair.keys,
                        image_displacement=cached_pair.image_displacement,
                        stage_displacement=self.stage_displacement_px_between(key2, key1),
                        fraction_under_threshold=cached_pair.fraction_under_threshold,
                    )
                )
                self.cache_stats["correlations_loaded_from_cache"] += 1
                continue

            image_displacement, frac_under_thresh = displacement_from_crosscorrelation(
                self[key1],
                self[key2],
                correlation_settings=self.correlation_settings,
                precalculated_filter=high_pass_filter,
            )
            pair_data.append(
                PairData(
                    keys=(key1, key2),
                    image_displacement=image_displacement.tolist(),
                    stage_displacement=self.stage_displacement_px_between(key2, key1),
                    fraction_under_threshold=frac_under_thresh,
                )
            )
            self.cache_stats["correlations_loaded_from_disk"] += 1
            # delete images we don't need
            retain_keys = [key1 for key1, _ in remaining_pairs] + [
                key2 for _, key2 in remaining_pairs
            ]
            if cache_img_in_memory:
                self.clear_image_memory_cache(retain=retain_keys)
        return pair_data

    # Overloads for different return types
    @overload
    def position_discrepancies(self, normalise: Literal[False]) -> list[np.ndarray]: ...
    @overload
    def position_discrepancies(self, normalise: Literal[True]) -> list[float]: ...
    @overload
    def position_discrepancies(self) -> list[float]: ...

    def position_discrepancies(self, normalise: bool = True) -> list[float] | list[np.ndarray]:
        """Return a list of the position discrepancy (in pixels) for each pair of images.

        The position discrepancy is calculated as:
        correlation displacement - stage displacement

        Where the correlation_displacement is the relative position between the pair
        of images as estimated by cross-correlation
        and the stage displacement is the displacement as estimated from the stage
        data.

        :param normalise: Set True to normalise the discrepancy into one number, set False
        to return a the discrepancies as a list of numpy arrays corresponding to the x and y
        discrepancy in pixels

        :return: List of discrepancies in the same order as `pairs`
        """

        if normalise:
            return copy(self._norm_pair_discrepancies)
        return copy(self._pair_discrepancies)

    def correlation_peak_qualities(self) -> list[float]:
        """The quality of the correlation peak

        The quality is estimated as the fraction of points in the image that
        are above a threshold set 90% of the way from the lowest value to the highest
        value

        :return: List of discrepencies in the same order as `pairs`
        """
        return [pair.fraction_under_threshold[0.9] for pair in self.pairs]

    def filtered_pairs(
        self,
        peak_quality_threshold: Optional[float] = None,
        discrepancy_threshold: Optional[float] = None,
        get_accepted_pairs: bool = True,
    ) -> list[PairData]:
        """Filter pairs against thresholds for stage discrepancy and peak quality.

        :param peak_quality_threshold: The threshold for peak quality. Any pair with
        a peak quality value above this is "accepted" as a good fit. If None, all pairs
        are accepted.
        :param discrepancy_threshold: The threshold for position discrepancy (see
        `CorrelatedImageSet.position_discrepancies`). Any pair with a position
        discrepancy below this threshold is "accepted" as a good fit. If None, all pairs
        are accepted.
        :param get_accepted_pairs: If True "accepted" pairs with high peak qualities above
        the thresholds and position_discrepancies below the threshold. If False, the
        rejected pairs are returned. Default is True.

        :return: The list of pair data for the pairs meeting the above criteria.
        """
        discreps = self.position_discrepancies(normalise=True)
        peak_quals = self.correlation_peak_qualities()
        if peak_quality_threshold is None:
            peak_quality_threshold = float(min(peak_quals))
        if discrepancy_threshold is None:
            discrepancy_threshold = float(max(discreps))

        filtered_list = []
        for i, pair in enumerate(self.pairs):
            if peak_quals[i] >= peak_quality_threshold and discreps[i] <= discrepancy_threshold:
                if get_accepted_pairs:
                    filtered_list.append(pair)
            elif not get_accepted_pairs:
                filtered_list.append(pair)

        return filtered_list

    def images_from_pair(self, index: int) -> tuple[OFSImage, OFSImage]:
        """
        Return the two overlapping images that were used to calculate a pair.

        :param index: The index of the pair in the list `CorrelatedImageSet.pairs`

        :return: A tuple with the two images as OFSImage objects.
        """
        key1, key2 = self.pairs[index].keys
        return self[key1], self[key2]

    def data_for_caching(self) -> CachedCorrelatedImageSet:
        """Return a `CachedCorrelatedImageSet` of the images. This can be serialised to
        json as
        ```
        json_str = image_set.data_for_caching().model_dump_json()
        ```

        :return: A `CachedCorrelatedImageSet`, this could be passed into the `cached` parameter
        when creating a new `CorrelatedImageSet`
        """
        image_cache = super().data_for_caching()
        return CachedCorrelatedImageSet(
            images=image_cache.images,
            correlation_settings=self.correlation_settings,
            pairs=self.pairs,
        )


def find_images(folder_path: str) -> list[str]:
    """List all images in a folder, excluding ones that are output by OpenFlexure Stitching

    :param folder_path: The path to the folder containing images.

    :return: A list of filenames for the images in the input folder.
    """

    # Get a list of all images in the folder, excluding ones containing any of 'ignore_phrases'
    ignore_phrases = ["stitched", "comparison", "Fused", "stage", "stitching", "preview"]
    return [
        f
        for f in os.listdir(folder_path)
        if os.path.isfile(os.path.join(folder_path, f))
        and f.lower().endswith((".png", ".jpg", ".jpeg", ".tiff", ".bmp", ".gif"))
        and not any(phrase in f for phrase in ignore_phrases)
    ]
