import pytest

import openflexure_stitching.__main__ as ofs_main
import openflexure_stitching as ofs

FAKE_TEST_DIR = "fake/image/directory"


@pytest.fixture
def default_args():
    """
    The default args with just an image directory set to
    FAKE_TEST_DIR
    """
    return ofs_main._parse_tile_and_stitch_args([FAKE_TEST_DIR])


def test_loading_settings_default_cli(default_args):
    """Test the default Loading Settings are the
    same on CLI as they are if loaded programatically
    """
    loading_settings = ofs_main.loading_settings_from_args(default_args)
    assert ofs.LoadingSettings() == loading_settings


def test_correlation_settings_default_cli(default_args):
    """Test the default Correlation Settings are the
    same on CLI as they are if loaded programatically
    """
    correlation_settings = ofs_main.correlation_settings_from_args(default_args)
    assert ofs.CorrelationSettings() == correlation_settings


def test_tiling_settings_default_cli(default_args):
    """Test the default Tiling Settings are the
    same on CLI as they are if loaded programatically
    """
    tiling_settings = ofs_main.tiling_settings_from_args(default_args)
    assert ofs.TilingSettings() == tiling_settings


def test_output_settings_default_cli(default_args):
    """Test the default Output Settings are the
    same on CLI as they are if loaded programatically except for the
    output directory. This is the image dir when when calling from command line
    but when programming no image dir is known so it is the working dir
    """
    output_settings = ofs_main.output_settings_from_args(default_args)
    assert ofs.OutputSettings(output_dir=FAKE_TEST_DIR) == output_settings

    default_settings = ofs.OutputSettings()
    assert default_settings.output_dir == "."
