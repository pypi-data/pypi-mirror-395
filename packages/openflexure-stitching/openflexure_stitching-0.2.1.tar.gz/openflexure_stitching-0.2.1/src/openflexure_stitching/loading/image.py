"""
Module for loading images from file.

It supports some OpenFlexure metadata reading, it could be extensible
to read other metadata too.

openflexure_stitching.loading directly.
"""

from typing import Any, Optional
import json
import os
import re
import time

import numpy as np
import piexif
from PIL import Image
from pydantic import BaseModel, ConfigDict
import psutil

from camera_stage_mapping.fft_image_tracking import grayscale_and_padding

from openflexure_stitching.types import NDArray, ImageType


class MetaDataError(RuntimeError):
    """The exception if Contradictory metadata found"""


class CachedOFSImage(BaseModel):
    """
    A pydantic model that can be used to cache and reload the OFSImage class

    This is most of the metadata except the stage position in pixels and the
    filetype. No image data or FFT data is cached.

    Note: The filename is cached not the full filepath as the relationship
    between the images directory and the working directory may not be the same
    when reloaded.

    To generate a `CachedOFSImage` use `OFSImage.data_for_caching()`
    """

    model_config = ConfigDict(arbitrary_types_allowed=True)
    filename: str
    """The image filename"""
    width: int
    """The width of the image in pixels"""
    height: int
    """The height of image in pixels"""
    exif_available: bool
    """True if EXIF data is available (EXIF may be available but empty)"""
    usercomment_available: bool
    """True if a JSON user comment string is available in the EXIF data"""
    file_created_time: float
    """The time the file was created (as a C time float). Note this may be
    when it was last copied on disk
    """
    file_size: int
    """The size of the file in Bytes"""
    from_openflexure: bool
    """True if the image contains OpenFlexure specific metadata"""
    capture_time: Optional[float]
    """The time the image was captured (as a C time float) if this information
    is available in the EXIF data. If not `None`
    """
    stage_position: Optional[tuple[int, int]]
    """The position of the stage as read from either EXIF data or from the file name.
    The relationship between these coordinates and the image coordinates in pixels is
    determined by the camera_to_sample_matrix
    """
    camera_to_sample_matrix: Optional[NDArray]
    """
    The matrix used to convert stage position to image position. See
    `OFSImage.camera_to_sample_matrix` for more detail. The cached matrix
    is the matrix as read from the file, unadjusted by user settings.

    **Note:** this is a numpy array. The huge type hint allows Pydantic to 
    serialise and cache the array as a list of numbers rather than binary.
    """
    csm_width: Optional[int]
    """
    The width of images usd to calibrate the camera_to_sample_matrix. See
    `OFSImage.csm_width` for more detail. The cached width is as read from
    the file, unadjusted by user settings.
    """
    pixel_size_um: Optional[float]
    """The conversion from pixels to micrometres if known"""


class _MemoryCache:
    """
    For OFSImage to cache Images and FFTs in memory.
    """

    _image_dsize: Optional[tuple[int, int]] = None
    _image_data: Optional[np.ndarray] = None
    _fft_data: Optional[np.ndarray] = None
    _fft_pad: Optional[bool] = None

    def get_image(self, dsize: tuple[int, int]) -> Optional[np.ndarray]:
        """
        Load image from the memory cache if available in the input size

        :param dsize: The size of the required numpy array.

        :return: A numpy array or None if the required image is not cached
        """
        if self._image_data is not None and dsize == self._image_dsize:
            return self._image_data
        return None

    def save_image(self, image: np.ndarray, dsize: tuple[int, int]):
        """
        Save image data to the memory cache if available memory is available.
        If less than 0.3GB of memory is available the image will not cache.
        No error is thrown as OFSImage will automatically handle loading it
        from disk when it is next requested.

        :param image: The image data to save as a numpy array.
        :param dsize: The size of the input numpy array.
        """
        if psutil.virtual_memory().available / (1024.0**3) > 0.3:
            self._image_dsize = dsize
            self._image_data = image

    def get_fft(self, image_dsize: tuple[int, int], pad: bool) -> Optional[np.ndarray]:
        """
        Load FFT from the memory cache if available in the input size with
        matching padding

        :param image_dsize: The size of the image used to generate the requested FFT
        :param pad: True if the FFT should be generated from a padded image.

        :return: A numpy array or None if the required FFT is not cached
        """
        if (
            self._fft_data is not None
            and image_dsize == self._image_dsize
            and pad == self._fft_pad
        ):
            return self._fft_data
        return None

    def save_fft(self, fft_data: np.ndarray, image_dsize: tuple[int, int], pad: bool):
        """
        Save fft data to the memory cache if available memory is available.
        If less than 0.3GB of memory is available the fft will not cache.
        No error is thrown as OFSImage will automatically handle loading it
        from disk when it is next requested.

        :param fft_data: The fft data to save as a numpy array.
        :param image_dsize: The size of the image used to generate the input FFT
        :param pad: True if the FFT was generated from a padded image.
        """
        if psutil.virtual_memory().available / (1024.0**3) > 0.3:
            if self._image_dsize != image_dsize:
                # If we are saving and the current image is a different
                # size, uncached it
                self._image_data = None
                self._image_dsize = image_dsize
            self._fft_data = fft_data
            self._fft_pad = pad

    def clear(self):
        """
        Clear this memory cache
        """
        self._image_dsize = None
        self._image_data = None
        self._fft_data = None
        self._fft_pad = None


class OFSImage:
    """
    A class that stores all the data about an image to be used for stitching

    When initialised the metadata is loaded but the image data is not loaded until
    requested.

    When image data is requested by default it will not be cached in memory. If requested
    the OFS Image will cache images and/or FFT data in memory. Only one size of the image
    will be cached.
    """

    _filepath: str
    _filetype: ImageType
    _width: int
    _height: int
    _exif_available: bool
    _usercomment_available: bool
    _file_created_time: float
    _file_size: int
    _from_openflexure: bool
    _capture_time: Optional[float] = None
    _stage_position: Optional[tuple[int, int]] = None
    # _file_csm and _file_csm_width are the original unaltered
    # camera stage mapping information from the file. They are used
    # for caching so that the loading settings don't affect the cache
    _file_csm: Optional[np.ndarray] = None
    _file_csm_width: Optional[int] = None
    _camera_to_sample_matrix: Optional[np.ndarray] = None
    _csm_width: Optional[int] = None
    _pixel_size_um: Optional[float] = None
    _stage_position_px: Optional[np.ndarray] = None
    _mem_cache: _MemoryCache

    def __init__(
        self,
        filepath: Optional[str] = None,
        *,
        cached: Optional[CachedOFSImage] = None,
        cached_folder: Optional[str] = None,
    ):
        """
        Create an OFSImage. Either the filepath or cached data should be supplied but not both.

        :param filepath: *Optional* The full filepath of the image to be loaded.
        :param cached: *Optional* Cached data (metadata) for this image.
        :param cached_folder: *Optional* The folder the cached data was loaded from.
        """
        self._mem_cache = _MemoryCache()
        if filepath is None:
            if cached is None:
                raise ValueError(
                    "Either a filepath or a CachedOFSImage must be provided to create an OFSImage"
                )
            self._load_from_cached(cached, cached_folder)
            return

        # Filename is set!
        if cached is not None:
            raise ValueError(
                "Do not set both a filepath and a CachedOFSImage when creating an OFSImage"
            )
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"The image {filepath} was not found.")
        self._filepath = filepath
        self._filetype = get_img_type_from_filepath(self._filepath)
        self._file_created_time = os.path.getmtime(self._filepath)
        self._file_size = os.path.getsize(self._filepath)
        exif: Optional[dict] = None
        if self._filetype in {ImageType.JPG, ImageType.TIFF}:
            exif = piexif.load(self._filepath)
        self._exif_available = exif is not None
        usercomment = get_exif_usercomment_json(exif)
        self._usercomment_available = usercomment is not None

        self._width, self._height = get_img_size(self._filepath, exif)
        self._capture_time = get_capture_time(exif)
        self._stage_position = get_stage_position(self.imagename, usercomment)

        self._file_csm = get_csm(usercomment)
        # If the CSM is set, then it is from custom openflexure image data:
        self._from_openflexure = self._file_csm is not None

        self._file_csm_width = get_csm_width(usercomment, from_openflexure=self._from_openflexure)
        self._csm_width = self._file_csm_width
        self._pixel_size_um = get_um_per_px(usercomment)

        # use set_csm to apply scaling to the csm and to set stage_position_px
        self.set_csm(self._file_csm, scale_to_width=True)

    def _load_from_cached(self, cached: CachedOFSImage, cached_folder: Optional[str]):
        """
        Load from the cache
        """
        if cached_folder is None:
            self._filepath = cached.filename
        else:
            self._filepath = os.path.join(cached_folder, cached.filename)
        if not os.path.exists(self._filepath):
            raise FileNotFoundError(
                f"The image {self._filepath} was not found. Did you set the correct cached folder?"
            )
        self._filetype = get_img_type_from_filepath(self._filepath)
        self._width = cached.width
        self._height = cached.height
        self._exif_available = cached.exif_available
        self._usercomment_available = cached.usercomment_available
        self._file_created_time = cached.file_created_time
        self._file_size = cached.file_size
        self._from_openflexure = cached.from_openflexure
        self._capture_time = cached.capture_time
        self._stage_position = cached.stage_position
        self._file_csm = cached.camera_to_sample_matrix
        self._file_csm_width = cached.csm_width

        self._csm_width = self._file_csm_width
        self._pixel_size_um = cached.pixel_size_um

        # Run set_csm but don't apply scaling to the csm
        # This will also set stage_position_px
        self.set_csm(self._file_csm, scale_to_width=True)

    @property
    def filename(self) -> str:
        """The name of the file (not the full filepath)"""
        return os.path.basename(self._filepath)

    @property
    def imagename(self) -> str:
        """The name of the image, this is the filename without the file extension"""
        return os.path.splitext(self.filename)[0]

    @property
    def filepath(self) -> str:
        """The filepath to the image."""
        return self._filepath

    @property
    def filetype(self) -> ImageType:
        """The file type of the image.

        This will be one of: `ImageType.JPG`, `ImageType.TIFF`, `ImageType.PNG`, `ImageType.GIF`, `ImageType.BMP`
        """
        return self._filetype

    @property
    def width(self) -> int:
        """The width of the image in pixels"""
        return self._width

    @property
    def height(self) -> int:
        """The height of image in pixels"""
        return self._height

    @property
    def exif_available(self) -> bool:
        """True if EXIF data is available (EXIF may be available but empty)"""
        return self._exif_available

    @property
    def usercomment_available(self) -> bool:
        """True if a JSON user comment string is available in the EXIF data"""
        return self._usercomment_available

    @property
    def file_created_time(self) -> float:
        """The time the file was created (as a C time float). Note this may be
        when it was last copied on disk
        """
        return self._file_created_time

    @property
    def file_size(self) -> int:
        """The size of the file in Bytes"""
        return self._file_size

    @property
    def capture_time(self) -> Optional[float]:
        """The time the image was captured (as a C time float) if this information
        is available in the EXIF data. If not `None`
        """
        return self._capture_time

    @property
    def from_openflexure(self) -> bool:
        """True if the image contains OpenFlexure specific metadata"""
        return self._from_openflexure

    @property
    def stage_position(self) -> Optional[tuple[int, int]]:
        """The position of the stage as read from either EXIF data or from the file name.
        The relationship between these coordinates and the image coordinates in pixels is
        determined by the camera_to_sample_matrix
        """
        return self._stage_position

    @property
    def stage_position_px(self) -> Optional[np.ndarray]:
        """Stage position after converting to pixels using the camera to sample matrix"""
        return self._stage_position_px

    @property
    def camera_to_sample_matrix(self) -> Optional[np.ndarray]:
        """
        The matrix that transforms between stage position in the input coordinates
        and stage position px.

        Note that most stages use an (x,y) convention but, image processing is performed
        image coordinates that use matrix index ordering which reverses x and y.

        If not set `None` is returned, in this case the matrix that will be used is
        ```
        np.array(
            [[0, 1],
             [1, 0]]
        )
        """
        if self._camera_to_sample_matrix is None:
            return np.array([[0, 1], [1, 0]])
        return self._camera_to_sample_matrix

    @property
    def csm_width(self) -> Optional[int]:
        """The width of images usd to calibrate the camera_to_sample_matrix

        This can be set to allow an input camera_to_sample_matrix that was calculated
        using images with a different resolution to this image.
        """
        return self._csm_width

    @property
    def pixel_size_um(self) -> Optional[float]:
        """The conversion from pixels to micrometres if known"""
        return self._pixel_size_um

    def set_csm(self, input_csm: Optional[np.ndarray], scale_to_width: bool = False) -> None:
        """
        Set the camera to sample matrix

        :param input_csm: the value to set camera to sample matrix to
        :param scale_to_width: Set to true to scale `input_csm` by the
                `csm_width` parameter before saving.

        See also `OFSImage.adjust_camera_to_sample_matrix`
        """

        if scale_to_width and self._csm_width is not None:
            scaling_width = self._csm_width
        else:
            scaling_width = None

        if input_csm is None:
            self._camera_to_sample_matrix = None
        elif scaling_width is None:
            self._camera_to_sample_matrix = input_csm
        else:
            scale = self.width / scaling_width
            self._camera_to_sample_matrix = input_csm / scale
        # If adjusting csm update stage_position px
        self._update_stage_position_px()

    def _update_stage_position_px(self) -> None:
        """
        Use the camera_to_sample_matrix and the _stage_position to estimate
        the stage (or generally, input) position in pixels
        """
        if self._stage_position is None or self.camera_to_sample_matrix is None:
            self._stage_position_px = None
            return

        pos_array = np.array(self._stage_position, dtype=float)
        self._stage_position_px = np.dot(pos_array, np.linalg.inv(self.camera_to_sample_matrix))

    def adjust_camera_to_sample_matrix(
        self, new_csm: Optional[np.ndarray | list], new_width: Optional[int]
    ):
        """Adjust camera stage mapping matrix

        This can be used with the data from `openflexure_stitching.types.LoadingSettings`

        This function is primarily designed to be called from OFSImageSet

        :param new_csm: *Optional* The updated camera to sample matrix.
        :param new_width: *Optional* TThe updated width that the camera to sample matrix
        was calibrated

        How this works depends on which parameters are input.

        * If both are input - The matrix is scaled before saving. The new width value is saved
        * If only the new_csm is input - This is treated as the correct matrix. The csm_width
        value for the image is set to None. This new_scm becomes the csm.
        * If only the new_width - the current CSM is updated.
        """
        if new_width is None:
            if new_csm is None:
                # Both none, nothing to do.
                return

            # Only new_csm set update
            self._csm_width = None
            self.set_csm(np.asarray(new_csm), scale_to_width=False)
        elif new_csm is None:
            # New function if only the width changed as it gets confusing.
            self._update_csm_width(new_width)
        else:
            # Both input, update width then set csm with scaling on
            self._csm_width = new_width
            self.set_csm(np.asarray(new_csm), scale_to_width=True)

    def _update_csm_width(self, new_width):
        """Update the csm width taking into account previous scaling.

        :param new_width: the new csm_width
        """
        current_csm = self.camera_to_sample_matrix
        if self._csm_width is None:
            # previously not scaled!
            self._csm_width = new_width
            self.set_csm(current_csm, scale_to_width=True)
            return

        old_scale = self.width / self._csm_width
        original_csm = current_csm * old_scale
        self._csm_width = new_width
        self.set_csm(original_csm, scale_to_width=True)

    def image_data(self, resize: float = 1.0, cache_in_memory: bool = False) -> np.ndarray:
        """Return the image data for this image as a numpy array

        :param resize: Resize the image by this factor.
        :param cache_in_memory: Cache this array in memory so it can be loaded again without
        reloading from disk. This will be ignored if the remaining RAM is below 0.3GB.
        """

        dsize = (round(self.width * resize), round(self.height * resize))

        if (image := self._mem_cache.get_image(dsize)) is not None:
            return image

        if resize == 1.0:
            image = np.array(Image.open(self.filepath))
        else:
            image = np.array(Image.open(self.filepath).resize(dsize))

        if cache_in_memory:
            self._mem_cache.save_image(image, dsize)
        return image

    def fft(
        self,
        resize: float = 1.0,
        pad: bool = True,
        cache_in_memory: bool = False,
        cache_img_in_memory: bool = False,
    ) -> np.ndarray:
        """Return the FFT of this image as a numpy array

        :param resize: Resize the image by this factor before performing the FFT
        :param pad: Pad the image to twice its size before performing the FFT
        :param cache_in_memory: Cache this array in memory so it can be loaded again without
        reloading from disk. This will be ignored if the remaining RAM is below 0.3GB.
        :param cache_img_in_memory: Cache the image used to generate this array in memory so
        it can be loaded again without reloading from disk. This will be ignored if the
        remaining RAM is below 0.3GB.
        """

        image_dsize = (round(self.width * resize), round(self.height * resize))

        if (fft := self._mem_cache.get_fft(image_dsize, pad)) is not None:
            return fft

        image = self.image_data(resize=resize, cache_in_memory=cache_img_in_memory)
        image, fft_shape = grayscale_and_padding(image, pad)
        fft_data = np.fft.rfft2(image, s=fft_shape)

        if cache_in_memory:
            self._mem_cache.save_fft(fft_data, image_dsize, pad)
        return fft_data

    def clear_memory_cache(self):
        """Clear the memory cache for this image"""
        self._mem_cache.clear()

    def data_for_caching(self) -> CachedOFSImage:
        """Return a `CachedOFSImage` of the key image metadata. This can be serialised to json as
        ```
        json_str = image.data_for_caching().model_dump_json()
        ```

        :return: A `CachedOFSImage`, this could be passed into the `cached` parameter
        when creating a new OFSImage
        """
        return CachedOFSImage(
            filename=self.filename,
            width=self.width,
            height=self.height,
            exif_available=self.exif_available,
            usercomment_available=self.usercomment_available,
            file_created_time=self.file_created_time,
            file_size=self.file_size,
            from_openflexure=self.from_openflexure,
            capture_time=self.capture_time,
            stage_position=self.stage_position,
            camera_to_sample_matrix=self._file_csm,
            csm_width=self._file_csm_width,
            pixel_size_um=self.pixel_size_um,
        )


def get_img_type_from_filepath(filepath: str) -> ImageType:
    """
    Determine the file type from the file name.

    :param filepath: The filepath of the image

    :return: The file type as one of This will be one of: `ImageType.JPG`, `ImageType.TIFF`,
    `ImageType.PNG`, `ImageType.GIF`, `ImageType.BMP`
    """
    file_ext = os.path.splitext(filepath)[1].lower()
    if file_ext in {".jpg", ".jpeg"}:
        return ImageType.JPG
    if file_ext == ".tiff":
        return ImageType.TIFF
    if file_ext == ".png":
        return ImageType.PNG
    if file_ext == ".gif":
        return ImageType.GIF
    if file_ext == ".bmp":
        return ImageType.BMP
    raise ValueError(f"Image type {file_ext} not supported.")


def get_img_size(filepath: str, exif: Optional[dict] = None) -> tuple[int, int]:
    """Return the height and width of the image

    :param filepath: The filepath of the image
    :param exif: The image exif data as a dictionary if available

    :return: Tuple of (width, height)
    """

    if exif is not None:
        try:
            width = exif["Exif"][piexif.ExifIFD.PixelXDimension]
            height = exif["Exif"][piexif.ExifIFD.PixelYDimension]
            return width, height
        except KeyError:
            # If there is no exif data for the dimension a key error is
            # raised. Treat this the same as no exif data
            pass

    # Load from the file directly. PIL is significantly faster than cv2
    img = Image.open(filepath)
    width = img.size[0]
    height = img.size[1]
    return width, height


def get_capture_time(exif: Optional[dict]) -> Optional[float]:
    """
    Return the time the image was captured if recorded in the exif data.

    :param exif: The image exif data as a dictionary if available

    :return: The time as a C time float, or `None` if not known
    """
    encoded_time = nested_get(exif, ["0th", piexif.ImageIFD.DateTime])

    if encoded_time is None:
        return None

    decoded_time = encoded_time.decode()
    if isinstance(decoded_time, str):
        try:
            time_struct = time.strptime(decoded_time, "%Y:%m:%d %H:%M:%S")
            return time.mktime(time_struct)
        except ValueError:
            # EXIF always expects %Y:%m:%d %H:%M:%S, a value error is thrown otherwise
            print(f"Could not read timestamp {decoded_time}")
    print(f"Could not read timestamp of type {type(decoded_time)}")
    return None


def get_stage_position(
    imagename: str, usercomment: Optional[dict] = None
) -> Optional[tuple[int, int]]:
    """
    Return stage position from the image name or the usercomment in the EXIF data
    or None if neither are set

    :param imagename: The filename of the image with the extension removed
    :param usercomment: The usercomment JSON loaded as a dict from EXIF if available.

    :return: Tuple of (x-position, y-position)

    :raises: MetaDataError if both are set but have different values.
    """
    position_from_exif = nested_get(usercomment, ["/stage/", "position"])

    if position_from_exif is not None:
        # if key is found pull out "x", "y"
        try:
            position_from_exif = tuple(int(position_from_exif[dim]) for dim in ("x", "y"))
        except (KeyError, TypeError):
            print("Stage position found in exif data, but it couldn't be read.")
            # Set to none and try file name
            position_from_exif = None

    position_from_filename = _read_stage_position_from_imagename(imagename)

    if position_from_exif is None:
        # This will return None if neither are set
        return position_from_filename
    if position_from_filename is None:
        return position_from_exif

    if position_from_filename != position_from_exif:
        raise MetaDataError("Position is set in both EXIF data and filename but do not match.")
    # Identical return either!
    return position_from_exif


def _read_stage_position_from_imagename(imagename: str) -> Optional[tuple[int, int]]:
    """Return the stage positions (x,y) from image name, or None if not found
    Expected coordinates in the file name with pattern `*x_y*` or `*x_y_z*`
    """

    matches = re.match(r"^.*?(-?\d+)_(-?\d+)(?:_(-?\d+))?$", imagename)
    if matches is None:
        return None
    # ignore z if found
    return (int(matches.group(1)), int(matches.group(2)))


def get_csm(usercomment: Optional[dict] = None) -> Optional[np.ndarray]:
    """Return the camera to sample matrix if stored in user comment.

    :param usercomment: The usercomment JSON loaded as a dict from EXIF if available.

    :return: numpy array of the camera to sample matrix or None if not set.
    """
    # These are they nested dictionary keys for where the CSM may be stored
    csm_nested_key_options = [
        [
            "instrument",
            "settings",
            "extensions",
            "org.openflexure.camera_stage_mapping",
            "image_to_stage_displacement",
        ],
        ["/camera_stage_mapping/", "image_to_stage_displacement_matrix"],
    ]

    for key_list in csm_nested_key_options:
        csm = nested_get(usercomment, key_list)
        if csm is not None:
            # If found return it, if not try more options
            return np.array(csm)
    # All options tried return None
    return None


def get_csm_width(usercomment: Optional[dict], from_openflexure: bool = False) -> Optional[int]:
    """Return the width the camera to sample matrix was calibrated at if stored in user comment.

    :param usercomment: The usercomment JSON loaded as a dict from EXIF if available.
    :param from_openflexure: Set True if the image is from an OpenFlexure Microscope
    This is needed for some old OpenFlexure Microscopes that used a csm_width of 832
    but didn't write it in the settings. (Default False)

    :return: the width of the calibration image in pixels or None if not set.
    """
    csm_width = nested_get(usercomment, ["/camera_stage_mapping/", "image_resolution", 1])
    if csm_width is None:
        if from_openflexure:
            # Correct for old OpenFlexure Microscopes not setting csm width but
            # always using 832
            return 832
        return None
    # Coerce to int before returning if set.
    return int(csm_width)


def get_um_per_px(usercomment: Optional[dict]) -> Optional[float]:
    """Return the conversion from micrometers to pixels

    :param usercomment: The usercomment JSON loaded as a dict from EXIF if available.

    :return: the conversion factor or None if not set.
    """
    return nested_get(
        usercomment, ["instrument", "settings", "extensions", "usafcal", "um_per_px"]
    )


def get_exif_usercomment_json(exif: Optional[dict[str, Any]]) -> Optional[dict]:
    """Extract the OpenFlexure metadata from a usercomment dict if available

    :param exif: The image exif data as a dictionary if available

    :return: The usercomment JSON loaded as a dict from EXIF if available.
    """
    if exif is None or "Exif" not in exif:
        return None

    if piexif.ExifIFD.UserComment in exif["Exif"]:
        return json.loads(exif["Exif"][piexif.ExifIFD.UserComment].decode())

    return None


def nested_get(nested: Optional[dict | list], key_list: list[Any]) -> Any:
    """
    Return value from a nested dictionary or list or None if it is not found.

    :param nested: The nested dictionaries or lists. Can be None, None will
    always be returned
    :param key_list: The list of dictionary keys or list indexes

    :return: The value if exists or None if not found.
    """
    if nested is None:
        return None

    if not key_list:
        raise ValueError("key_list can't be empty")

    # Loop through keys updating the value
    value = nested
    for key in key_list:
        # Try to get next value from key in dict or index in list
        if isinstance(value, dict) and key in value:
            value = value[key]
        elif isinstance(value, list) and isinstance(key, int):
            try:
                value = value[key]
            except IndexError:
                # That index isn't in the list
                return None
        else:
            # Return None if it can't be found.
            return None
    # All keys found, return value
    return value
