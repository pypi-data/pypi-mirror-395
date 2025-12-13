"""
The core functionality for the stitching submodule.
"""

from typing import Optional, Literal, cast
import os
from math import ceil
import tempfile

import numpy as np
from PIL import Image
import psutil


from openflexure_stitching.types import PairData
from openflexure_stitching.loading import OFSImage, OFSImageSet

from .utils import (
    overlap_slices,
    arange_from_slice,
    downsample_image,
    regions_overlap,
    RegionOfInterest,
)
from .vips_stitch import convert_tiles_to_jpeg


class StitchGeometry:
    """
    A class that contains the data for the position and image properties of
    images to be stitched together
    """

    files: list[str]
    downsample: int
    image_size: tuple[int, int]
    positions: list[np.ndarray]
    output_size: tuple[int, int]
    output_centre: tuple[float, float]
    _pixel_size_um: Optional[float] = None
    _downsampled_image_size = None

    def __init__(
        self,
        image_set: OFSImageSet | list[OFSImage],
        positions: Optional[dict[str, np.ndarray]] = None,
        target_image_width: Optional[int] = None,
        mem_limit: Optional[int] = None,
    ):
        """Calculate where each image should go in the stitched image

        Determine the size of the output image, and the position of each
        image within that.

        :param image_set: The set of images to be stitched
        :param positions: *Optional* A dictionary of optimised positions for each image
        in the set. If `None` their input stage positions are used instead.
        :param target_image_width: The desired width of the output image in pixels.
        If None no downsampling will be used unless a memory limit is set.
        :param mem_limit: The limit in MB that the stitched image should take in RAM. This
        parameter is ignored if `target_image_width` is set.
        """

        self.files = [image.filepath for image in image_set]
        if isinstance(image_set, OFSImageSet):
            self.image_size = image_set.image_shape
        else:
            self.image_size = (image_set[0].height, image_set[0].width)
        if positions is None:
            stage_positions: list[np.ndarray | None]
            stage_positions = [image.stage_position_px for image in image_set]
            if any(pos is None for pos in stage_positions):
                raise ValueError("One or more images has no stage position")
            # Cast the type now we have checked for a lack of Nones
            self.positions = cast(list[np.ndarray], stage_positions)
        else:
            self.positions = [positions[image.filename] for image in image_set]

        min_pos = np.min(self.positions, axis=0)
        max_pos = np.max(self.positions, axis=0)
        full_output_size = max_pos - min_pos + self.image_size

        self.downsample = 1
        if target_image_width is not None:
            self.downsample = max([1, ceil(full_output_size[1] / target_image_width)])
        elif mem_limit is not None:
            print(f"Size of the undownsampled image would be {full_output_size}")
            projected_size = full_output_size[0] * full_output_size[1] * 3 / 1024 / 1024
            if projected_size > mem_limit:
                self.downsample = ceil(projected_size / mem_limit)

        self.output_size = tuple(np.round(full_output_size / self.downsample))
        self.output_centre = tuple((max_pos + min_pos) / 2)

        self.centres, self.top_lefts = self._all_image_centres_and_top_left_corners()
        self.quant_top_lefts = np.ceil(self.top_lefts).astype(int)

        self._filter_duplicate_positions()

        if isinstance(image_set, OFSImageSet) and image_set.pixel_size_um:
            self._pixel_size_um = self.downsample * image_set.pixel_size_um

    def _filter_duplicate_positions(self):
        """Check for, and filter out, any images which would occupy the same pixel position as another"""
        scaled_positions = [np.array(pos) / self.downsample for pos in self.positions]

        keep_indices = []
        removed_indices = set()

        for pos_index, pos in enumerate(scaled_positions):
            if pos_index in removed_indices:
                continue  # already removed as too close to an earlier image

            # If not in the list to remove, add the current image
            keep_indices.append(pos_index)
            for j in range(pos_index + 1, len(scaled_positions)):
                if j in removed_indices:
                    continue

                # Compute distance between image positions
                dist = np.abs(pos - scaled_positions[j])
                # Within 2 pixels of another image in both x and y.
                # Note: For large scans this is called millions of times so not using
                # linalg.norm or np.any has significant speed up.
                if dist[0] < 2 and dist[1] < 2:
                    # Add this index to the set of indices to skip
                    removed_indices.add(j)

        # Filter positions and files to keep only those not removed
        self.positions = [self.positions[i] for i in keep_indices]
        self.files = [self.files[i] for i in keep_indices]

    def _all_image_centres_and_top_left_corners(self) -> tuple[np.ndarray, np.ndarray]:
        """Precalculate centres and top left of each image."""
        centres = np.zeros((self.n_images, 2))
        top_lefts = np.zeros((self.n_images, 2))

        output_centre = np.array(self.output_centre)
        half_output_size = np.array(self.output_size) / 2.0
        half_ds_image_size = np.array(self.image_size) / 2.0 / self.downsample

        for i in range(self.n_images):
            pos = np.array(self.positions[i])
            centres[i, :] = (pos - output_centre) / self.downsample + half_output_size
            top_lefts[i, :] = centres[i, :] - half_ds_image_size
        return centres, top_lefts

    def image_shift(self, index: int) -> np.ndarray:
        """The distance in pixels image should be shifted during downsampling

        The input images are placed into the output at integer pixel positions: if the calculated
        position is not an integer, the image needs shifting during downsampling, to get
        sub-pixel positioning.
        """
        return (self.quant_top_lefts[index, :] - self.top_lefts[index, :]) * self.downsample

    @property
    def downsampled_image_size(self) -> tuple[int, int]:
        """The size of the downsampled images"""
        if not self._downsampled_image_size:
            self._downsampled_image_size = (
                self.image_size[0] // self.downsample - 1,
                self.image_size[1] // self.downsample - 1,
            )
        return self._downsampled_image_size

    @property
    def n_images(self):
        """The number of input images"""
        return len(self.files)

    @property
    def indexes(self):
        """A range that will enumerate the images"""
        return range(self.n_images)

    @property
    def pixel_size_um(self) -> Optional[float]:
        """The size of a pixel in um. If not known this will be None."""
        return self._pixel_size_um


def stitch_and_save(
    filepath: str,
    stitch_geometry: StitchGeometry,
    use_vips: bool = False,
    tile_size: int | Literal["auto"] = "auto",
):
    """Stitch images together and save to a file

    :param filepath: The path to save the image to
    :param stitch_geometry: The object containing information for how to stitch the images
    :param use_vips: Whether to use vips to produce the JPEG image, default False uses PIL
    :param tile_size: The image tile size in pixels when using VIPS. Can be an integer or
        the string "auto" (default), which automatically selects a size based on free memory.
    """

    if not use_vips:
        img = Image.fromarray(stitch_images(stitch_geometry, method="nearest"))
        img.save(filepath, quality=95)
    else:
        if tile_size == "auto":
            auto_tile_size = determine_tile_size()
            output_tile_size = (auto_tile_size, auto_tile_size)
            print(
                f"Based on remaining RAM, will stitch with image of size {output_tile_size} pixels",
                flush=True,
            )
        else:
            output_tile_size = (tile_size, tile_size)
        with tempfile.TemporaryDirectory() as tile_dir:
            stitch_geometry_to_tiles(
                tile_dir, stitch_geometry=stitch_geometry, tile_size=output_tile_size
            )
            convert_tiles_to_jpeg(tile_dir, filepath)


def determine_tile_size():
    """Use the current free memory to decide the file size of tiles to use, as larger tiles
    greatly increase the speed of stitching.

    :return: The pixel width and height of the tile suggested by memory available

    The fastest tile sizes are orders of two. The size of each option in memory is:
    - [1024, 1024] -> 3MB
    - [2048, 2048] -> 12MB
    - [4096, 4096] -> 48MB
    - [8192, 8192] -> 192MB
    - [16384, 16384] -> 768MB
    - [32768, 32768] -> 3072MB
    """
    # For future reference, can use sys.getsizeof()
    # or height * width * channels to get size in bytes, as dtype is uint8
    remaining_ram = psutil.virtual_memory().available / 1024 / 1024
    print(f"Remaining RAM is {round(remaining_ram)}MB", flush=True)

    # keep a buffer of 400MB
    ram_for_stitching = remaining_ram - 400

    if ram_for_stitching > 3072:
        return 32768
    if ram_for_stitching > 768:
        return 16384
    if ram_for_stitching > 192:
        return 8192
    if ram_for_stitching > 48:
        return 4096
    if ram_for_stitching > 12:
        return 2048
    # Below this, even this program will struggle to stitch in a sensible amount of time
    # Return a minimum tile size
    return 1024


def stitch_pair(image_set: OFSImageSet, pair: PairData, by_correlation: bool = True) -> np.ndarray:
    """Stitch a pair of images and return as a np.array

    :param image_set: The image set the images are in
    :param pair: The pair of images to stitch
    :param by_correlation: If True stitch by the value calculated by cross correlation,
    if false stitch by stage position

    :return: The stitched image as a numpy array.
    """
    key1, key2 = pair.keys
    image1 = image_set[key1]
    image2 = image_set[key2]
    if by_correlation:
        positions = {key1: np.array((0, 0)), key2: np.array(pair.image_displacement)}
    else:
        positions = {key1: np.array((0, 0)), key2: np.array(pair.stage_displacement)}
    geometry = StitchGeometry([image1, image2], positions)
    return stitch_images(geometry)


def stitch_images(
    stitch_geometry: StitchGeometry,
    method: Literal["nearest", "latest"] = "nearest",
    region_of_interest: Optional[RegionOfInterest] = None,
) -> np.ndarray:
    """Merge images together, using supplied positions (in pixels).

    Place images into a combined image whole. The order of the images
    determines which image is on top, i.e. we will use the last image
    that overlaps each point, not the closest.

    This method is fastest, but will not produce the best stitched images
    as the quality is generally better in the middle of each tile.


    :param stitch_geometry: a StitchGeometry object initialised with the tile filenames
        and positions.
    :param method: One of "nearest", "latest".
    * "nearest" each pixel in the final image comes from the tile with the centre
    closest to that pixel, i.e. we use the middle part of each image.
    * "latest", images are place in whole, in timestamp order. This is faster but
    uses the edges of later images rather than the centre of each image resulting
    in a less uniform image.
    :param region_of_interest: An optional tuple of (x, y), (width, height)), if
    specified only a subset of the output image will be calculated.

    :return: The stitched image as a numpy array.

    **Note**:

    stitch_geometry.downsample: int=3
        The size of the stitched image will be reduced by this amount in each
        dimension, to save on resources.  Note: currently it decimates rather than
        taking a mean, for speed - in the future a mean may be an option.
        Images are downsampled after taking into account their position, i.e.
        if you downsample by a factor of 5, you'll still be within 1 original
        pixel, not within 5, of the right position.  Currently we don't do
        any sub-pixel shifting.

    Returns: (stitched_image, stitched_centre, image_centres)
        (numpy.ndarray, numpy.ndarray, numpy.ndarray)
        An MxPx3 array containing the stitched image, a 1D array of length
        2 containing the coordinates of the centre of the image in non-
        downsampled pixel coordinates, and an Nx2 array of the positions of the
        source images (their centres) relative to the top left of the stitched
        image, in downsampled pixels.
    """
    if not region_of_interest:
        region_of_interest = ((0, 0), stitch_geometry.output_size)
    canvas_origin = np.array(region_of_interest[0]).astype(int)
    canvas_size = np.array(region_of_interest[1]).astype(int)
    stitched_image = np.zeros(tuple(canvas_size) + (3,), dtype=np.uint8)
    for i, filename in enumerate(stitch_geometry.files):
        image_roi = (
            tuple(stitch_geometry.top_lefts[i, :]),
            stitch_geometry.downsampled_image_size,
        )
        if not regions_overlap(region_of_interest, image_roi):
            continue  # Don't load images we don't need.
        img = downsample_image(
            np.array(Image.open(filename)),
            stitch_geometry.downsample,
            shift=stitch_geometry.image_shift(i),
        )
        tl = stitch_geometry.quant_top_lefts[i, :] - canvas_origin  # top left, relative to the ROI
        br = tl + np.array(img.shape[:2])  # bottom right, relative to the ROI
        canvas_slices = tuple(  # This is the region of the canvas that overlaps with img
            slice(max(0, tl[d]), min(canvas_size[d], br[d])) for d in range(2)
        )
        img_slices = tuple(  # This is the region of img that overlaps with the canvas
            slice(max(0, -tl[d]), min(canvas_size[d], br[d]) - tl[d]) for d in range(2)
        )
        if method == "latest":
            stitched_image[canvas_slices] = img[img_slices]
        elif method == "nearest":
            mask_image(img, i, stitch_geometry)
            stitched_image[canvas_slices] += img[img_slices]
    return stitched_image


def crop_roi(roi: RegionOfInterest, canvas_size: tuple[int, int]):
    """Crop a region of interest so it fits inside a canvas

    Region of interest is a tuple of ((x, y), (width, height))
    """
    pos, size = roi
    if any(pos[d] > canvas_size[d] for d in range(2)):
        raise ValueError("The region of interest is outside the canvas!")
    new_size = tuple(  # Crop the ROI so it fits inside the canvas
        min(size[d], canvas_size[d] - pos[d]) for d in range(2)
    )
    return pos, new_size


def stitch_geometry_to_tiles(
    output_folder: str,
    stitch_geometry: StitchGeometry,
    tile_size: tuple[int, int] = (4096, 4096),
):
    """Stitch the image and write a series of tiles to a folder, in JPEG format"""
    if not os.path.isdir(output_folder):
        os.mkdir(output_folder)
    tile_rois = [
        crop_roi(((i * tile_size[0], j * tile_size[1]), tile_size), stitch_geometry.output_size)
        for i in range(int(np.ceil(stitch_geometry.output_size[0] / tile_size[0])))
        for j in range(int(np.ceil(stitch_geometry.output_size[1] / tile_size[1])))
    ]
    for roi in tile_rois:
        tile = Image.fromarray(stitch_images(stitch_geometry, region_of_interest=roi))
        tile.save(os.path.join(output_folder, f"{roi[0][0]}_{roi[0][1]}.jpeg"), quality=95)


def mask_image(img: np.ndarray, index: int, stitch_geometry: StitchGeometry):
    """Set pixels in an image to zero if the centre of another image is closer

    This will result in the edges of an image being set to zero. This means
    that when all images are summed in place, only one image at any point will
    be nonzero.

    WARNING: `img` will be modified.
    """
    centre = stitch_geometry.centres[index, :]
    q_top_left = stitch_geometry.quant_top_lefts[index, :]
    for j in stitch_geometry.indexes:
        other_centre = stitch_geometry.centres[j, :]
        # Calculate the (x, y) difference between the top left corners of the images.
        difference = stitch_geometry.quant_top_lefts[j, :] - q_top_left
        # Note: this code may be called a few million times for large scans with
        # thousands of images. The overhead of np.any rather than checking each
        # dimension using `or` can add up to a significant delay.
        if np.abs(difference[0]) > img.shape[0] or np.abs(difference[1]) > img.shape[1]:
            # ignore images that don't overlap with this one
            continue
        xr, yr = overlap_slices(difference, img.shape[:2])
        if xr is None or yr is None:
            continue
        # Calculate the midpoint between image centres, relative to the
        # top left of img.
        # This is relative to the quantized top left position.
        midpoint = (other_centre + centre) / 2.0 - q_top_left
        x_slices = arange_from_slice(xr)[:, np.newaxis] * difference[0]
        y_slices = arange_from_slice(yr)[np.newaxis, :] * difference[1]

        # On the off chance that images are perfectly aligned to the nearest pixel
        # On the overlapping line the mask needs to choose one image or the other
        # Calculate the angle of the difference
        angle = np.arctan2(difference[0], difference[1])
        # Take the border from the image in with an angle from -45 to +135
        choose_border = -np.pi / 4 < angle <= 3 * np.pi / 4
        if choose_border:
            mask = (x_slices + y_slices) > np.dot(midpoint, difference)
        else:
            mask = (x_slices + y_slices) >= np.dot(midpoint, difference)
        img[xr, yr][mask] = 0


def create_thumbnail(filepath: str):
    """Create a maximum 400x400 pixel thumbnail of the stitch,
    and save it as 'stitched_thumbnail.jpg'

    :param filepath: The path to the stitched image to create a thumbnail of.

    :raises: FileNotFoundError if the image does not exist.
    """
    target_size = (400, 400)

    if not os.path.isfile(filepath):
        raise FileNotFoundError("Stitched image was not saved correctly.")

    stitched_image = Image.open(filepath)

    containing_folder = os.path.dirname(filepath)
    stitched_image.thumbnail(target_size)
    stitched_image.save(os.path.join(containing_folder, "stitched_thumbnail.jpg"))
