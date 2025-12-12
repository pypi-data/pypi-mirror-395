"""The OpenFlexure metadata has changed over development and
was poorly defined. As such we need to test in a somewhat
ad hoc fashion
"""

import os
import shutil
from tempfile import tempdir
import calendar
import time
import pytest
import numpy as np

from openflexure_stitching.types import ImageType
from openflexure_stitching.loading import OFSImage, CachedOFSImage, MetaDataError

THIS_DIR = os.path.dirname(os.path.realpath(__file__))

# Unit tests fail because when loading images into memory their time is converted to
# local Ctime in the local timezone (so it matches the file created time). This gives
# The local timezone in hours
LOCAL_TIMEZONE = round((calendar.timegm(time.localtime()) - time.time()) / 3600)


def test_load_ofm_v3_april_25():
    test_dir = os.path.join(THIS_DIR, "images")
    test_fpath = os.path.join(test_dir, "image_-6393_-26665.jpg")
    test_image = OFSImage(test_fpath)

    # dump to json string and reload
    json_str = test_image.data_for_caching().model_dump_json()
    cached_image = CachedOFSImage.model_validate_json(json_str)
    test_image_from_cache = OFSImage(cached=cached_image, cached_folder=test_dir)

    for image in [test_image, test_image_from_cache]:
        assert image.filepath == test_fpath
        assert image.filetype == ImageType.JPG
        assert image.width == 820
        assert image.height == 616
        assert image.exif_available
        assert image.usercomment_available
        assert image.from_openflexure
        assert image.csm_width == 820
        assert image.capture_time is None
        assert image.stage_position == (-6393, -26665)
        csm_md_int = np.array(image.camera_to_sample_matrix * 1e6, dtype=int)
        assert np.array_equal(csm_md_int, np.array([[-2220, 3397850], [3406378, 3936]]))
        stage_pos_px_int = np.array(image.stage_position_px, dtype=int)
        assert np.array_equal(stage_pos_px_int, np.array([-7845, -1881]))


def test_load_ofm_v3_april_25_wrong_pos():
    """Test that an image with stage position both in exif
    metadata and loaded from filename errors due to
    inconsistent stage positions
    """
    orig_fpath = os.path.join(THIS_DIR, "images", "image_-6393_-26665.jpg")
    tmp_fpath = os.path.join(tempdir, "image_0_0.jpg")
    shutil.copy(orig_fpath, tmp_fpath)
    # Stage pos shouldn't match any more throwing error
    with pytest.raises(MetaDataError):
        OFSImage(tmp_fpath)


def test_load_ofm_v3_with_timestamp():
    """
    These are from v3 brazil branch
    """
    test_fpath = os.path.join(THIS_DIR, "images", "v3_timestamped", "image_-332_1377.jpeg")
    test_image = OFSImage(test_fpath)
    assert test_image.from_openflexure
    assert test_image.exif_available
    assert test_image.usercomment_available
    # From Openflexure but csm_width is not 832 so it is being read correctly!
    assert test_image.from_openflexure
    assert test_image.csm_width == 820
    assert test_image.capture_time == 1736643059.0
    assert test_image.stage_position == (-332, 1377)


def test_load_ofm_v2_image():
    """Test the loading of an image from V2 of the microscope server,
    which had a different metadata format and CSM calibration width
    """
    test_dir = os.path.join(THIS_DIR, "images")
    test_fpath = os.path.join(test_dir, "v2_image_33818_24860_832.jpeg")
    test_image = OFSImage(test_fpath)

    # dump to json string and reload
    json_str = test_image.data_for_caching().model_dump_json()
    cached_image = CachedOFSImage.model_validate_json(json_str)
    test_image_from_cache = OFSImage(cached=cached_image, cached_folder=test_dir)

    for image in [test_image, test_image_from_cache]:
        assert image.filepath == test_fpath
        assert image.filetype == ImageType.JPG
        assert image.width == 832
        assert image.height == 624
        assert image.exif_available
        assert image.usercomment_available
        assert image.from_openflexure
        # This isn't set in the image, so it is correctly using the value of 832
        # As this is openflexure without it set (i.e. v2!)
        assert image.csm_width == 832
        assert round(image.capture_time) == 1726191296 - LOCAL_TIMEZONE * 3600
        assert image.stage_position == (33818, 24860)
        csm_md_int = np.array(image.camera_to_sample_matrix * 1e6, dtype=int)
        assert np.array_equal(csm_md_int, np.array([[-94986, -10508573], [-10473637, -96544]]))
        stage_pos_px_int = np.array(image.stage_position_px, dtype=int)
        assert np.array_equal(stage_pos_px_int, np.array([-2336, -3207]))


def test_load_from_cache_without_specifying_dir():
    """Attempt to cache an image from a folder, without specifying the
    folder which is being cached. Should raise a FileNotFoundError
    """
    test_dir = os.path.join(THIS_DIR, "images")
    test_fpath = os.path.join(test_dir, "image_-6393_-26665.jpg")
    test_image = OFSImage(test_fpath)

    # dump to json string and reload
    json_str = test_image.data_for_caching().model_dump_json()
    cached_image = CachedOFSImage.model_validate_json(json_str)

    # If no cached folder is set the image can't be found as it is not
    # in the working dir
    with pytest.raises(FileNotFoundError):
        OFSImage(cached=cached_image)


def test_load_no_metadata_with_stage_coords():
    """Test that an image that has been cropped and stripped of metadata
    loads with the basic data that we can load from any image. Filename
    contains a stage position, which is also loaded and tested
    """
    test_dir = os.path.join(THIS_DIR, "images", "cropped")
    test_fpath = os.path.join(test_dir, "img_334_334.jpg")
    test_image = OFSImage(test_fpath)

    # dump to json string and reload
    json_str = test_image.data_for_caching().model_dump_json()
    cached_image = CachedOFSImage.model_validate_json(json_str)
    test_image_from_cache = OFSImage(cached=cached_image, cached_folder=test_dir)

    for image in [test_image, test_image_from_cache]:
        assert image.filepath == test_fpath
        assert image.filetype == ImageType.JPG
        assert image.width == 666
        assert image.height == 666
        # Should be the basic data but everything that could be was stripped
        assert image.exif_available
        assert not image.usercomment_available
        assert image.capture_time is None
        assert image.stage_position == (334, 334)


def test_load_no_metadata_without_stage_coords():
    """
    Test that an image that has been cropped and stripped of metadata
    loads with the basic data that we can load from any image. Filename
    contains a stage position, which is also loaded and tested

    """
    test_dir = os.path.join(THIS_DIR, "images")
    test_fpath = os.path.join(test_dir, "ofm-c.jpg")
    test_image = OFSImage(test_fpath)

    # dump to json string and reload
    json_str = test_image.data_for_caching().model_dump_json()
    cached_image = CachedOFSImage.model_validate_json(json_str)
    test_image_from_cache = OFSImage(cached=cached_image, cached_folder=test_dir)

    for image in [test_image, test_image_from_cache]:
        assert image.filepath == test_fpath
        assert image.filetype == ImageType.JPG
        assert image.width == 1000
        assert image.height == 1000
        # Should be the basic data but everything that could be was stripped
        assert image.exif_available
        assert not image.usercomment_available
        assert image.capture_time is None
