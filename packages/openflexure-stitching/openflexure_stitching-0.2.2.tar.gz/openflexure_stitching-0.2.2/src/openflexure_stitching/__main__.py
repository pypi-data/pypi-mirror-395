"""
A collection of functions to run openflexure-stitching from the command line

Accepts arguments to affect how images are loaded, processed and stitched,
calling openflexure-stitching with any relevant arguments. Any non-specified
arguments are auto-populated with their default values in this file, which are
not guaranteed to match the defaults if running openflexure-stitching from
Python. To compare the defaults, compare this file against types.py
"""

from typing import Optional
import sys
import textwrap
from argparse import ArgumentParser, Namespace, BooleanOptionalAction, HelpFormatter
import ast
import openflexure_stitching as ofs
from openflexure_stitching.pipeline import ALL_CLI_STITCHING_MODES


class _SmartFormatter(HelpFormatter):
    """
    A class to modify the help formatter for argpase so that
    explicit new lines in help text are formatted.

    This allows us to space out complex help strings to draw
    attention to options. Note that double new lines are not
    as argparse swallows the space.

    Inspired by:
    https://stackoverflow.com/questions/3853722/how-to-insert-newlines-on-argparse-help-text
    but this didn't wrap the text. Text wrapping follows the same
    functions used in argparse itself.

    """

    def _split_lines(self, text, width):
        """Override default function for formatting argument information

        :param text: The text for a specific argument or block of text in
        the help string
        :param width: The width of the terminal in characters.

        :return: A list of individual lines of text that are short enough
        not not get auto-wrapped by the terminal.
        """
        returned_lines = []
        for line in text.splitlines():
            returned_lines += textwrap.wrap(line, width)
        return returned_lines


def load_tile_and_stitch_cli():
    """
    This is the program that runs when `openflexure-stitch is
    run from commandline.
    """
    args = _parse_tile_and_stitch_args()
    loading_settings = loading_settings_from_args(args)
    correlation_settings = correlation_settings_from_args(args)
    tiling_settings = tiling_settings_from_args(args)
    output_settings = output_settings_from_args(args)
    ofs.load_tile_and_stitch(
        folder=args.input_folder,
        loading_settings=loading_settings,
        correlation_settings=correlation_settings,
        tiling_settings=tiling_settings,
        output_settings=output_settings,
    )


def _parse_tile_and_stitch_args(input_args: Optional[list[str]] = None):
    """
    Parse the input arguments.

    Leave input args as None to parse with the CLI arguments from __main__, this
    is here to allow testing
    """
    parser = ArgumentParser(
        description="Tile together a folder of microscope images.", formatter_class=_SmartFormatter
    )

    parser.add_argument("input_folder", help="A folder containing images to tile.")

    # Note that the output arguments are not added by a separate function
    # So we can force --stitching_mode to the front as it is the most important user input
    # but keep --stitch_tiff and --stitch_dzi at the end.

    # Note also that 'only_stage_stitch' is now an undocumented legacy argument for v3
    # compatibility. See output_settings_from_args
    parser.add_argument(
        "-o",
        "--output_dir",
        type=str,
        default=None,
        help=(
            "The folder to save resulting images. Will be created if needed. Default behaviour "
            "is to use the folder containing the images to be stitched."
        ),
    )
    parser.add_argument(
        "--stitching_mode",
        type=str,
        default="all",
        help=(
            "Valid options are: 'all', 'preview_stitch', 'stage_stitch', 'only_correlate'\n"
            "'all' - run the full stitching algorithm with correlations, and output "
            "a stitched image.\n"
            "'preview_stitch' - run the full stitching algorithm, but only output a 1000px wide "
            "preview of the stitch.\n"
            "'stage_stitch' - output a stitched image based only on image coordinates.\n"
            "'only_correlate' - calculate the correlation between overlapping pairs of images "
            "and save this to speed up a future run of all. No image is produced."
        ),
    )
    add_loading_args(parser)
    add_tiling_args(parser)
    add_correlation_args(parser)
    parser.add_argument(
        "--stitch_tiff",
        default=False,
        action=BooleanOptionalAction,
        help=("Produce a pyramidal TIFF (default: False).This requires VIPs to be installed."),
    )
    parser.add_argument(
        "--stitch_dzi",
        default=False,
        action=BooleanOptionalAction,
        help="Produce a pyramidal DZI (default: False).",
    )
    parser.add_argument(
        "--tile_size",
        default="auto",
        help=(
            "Tile size to use when stitching images with Pyvips.\n"
            "Specify a number (recommended to be a power of two) or use 'auto' to "
            "automatically select a tile size based on available memory.\n"
            "'auto' selects the largest tile size that leaves at least 400MB of free RAM.\n"
            "Note: Tile size cannot be changed mid-run. If system memory availability changes "
            "significantly after processing starts, 'auto' will not adapt.\n"
            "When setting a numeric tile size manually, using powers of two is advised.\n"
            "Approximate memory usage for common sizes:\n"
            "- 1024   → ~3MB\n"
            "- 2048   → ~12MB\n"
            "- 4096   → ~48MB\n"
            "- 8192   → ~192MB\n"
            "- 16384  → ~768MB\n"
            "- 32768  → ~3072MB"
        ),
    )
    return parser.parse_args(input_args)


def add_tiling_args(parser: ArgumentParser):
    """Add arguments associated with optimising the image positions from correlation data"""

    parser.add_argument(
        "--thresholding_method",
        type=str,
        default="automatic",
        help=(
            "The method to identify thresholds for tiling.\n"
            "Valid options are: 'automatic' or 'manual'\n"
            "'automatic' (default) is slower\n"
            "'manual' is quicker, but the program pauses for the user to "
            "interpret the graph in stitching_correlations.png and to provide "
            "cut-offs for max_stage_discrepancy and min_peak_quality."
        ),
    )
    parser.add_argument(
        "--max_stage_discrepancy",
        type=float,
        default=None,
        help=(
            "Set a hard limit on the maximum disagreement (in pixels) between "
            "the stage position and the position suggested by the correlations. "
            "Default is to let the program automatically optimise this value "
            " without a hard limit."
        ),
    )
    parser.add_argument(
        "--min_peak_quality",
        type=float,
        default=None,
        help=(
            "Set a hard limit on the minimum peak quality on a scale of (0-1). "
            "Default is to let the program automatically optimise this value."
        ),
    )


def add_loading_args(parser: ArgumentParser):
    """Add arguments associated with loading the images"""
    parser.add_argument(
        "--csm_matrix",
        type=str,
        default=None,
        help=(
            "This matrix that converts any input coordinates into pixels "
            "The matrix can be generated by the OpenFlexure python package "
            "camera-stage-mapping.\n"
            "For images from an OpenFlexure Microscope this should be loaded in "
            "automatically from image metadata\n"
            "By default no matrix is loaded and no metadata is available any input "
            "coordinates are treated as being in pixels.\n"
            "The matrix should be entered in the form [[0,1],[1,0]]"
        ),
    )
    parser.add_argument(
        "--csm_calibration_width",
        type=float,
        default=None,
        help=(
            "The width of the images used to calibrate the --csm_matrix. "
            "This is used if the csm_matrix was calculated from a different "
            "resolution than the input images.\n"
            "Note: If this is not set and it is detected that the image came from "
            "an OpenFlexure Microscope then the default is 832. Otherwise the CSM is "
            "left unscaled.\n"
            "To not adjust the matrix enter 0\n"
        ),
    )


def add_correlation_args(parser: ArgumentParser):
    """Add arguments associated with image correlation"""

    parser.add_argument(
        "--pad",
        default=True,
        action=BooleanOptionalAction,
        help="Zero-pad images to remove ambiguity when correlating (default: True).",
    )
    parser.add_argument(
        "--high_pass_sigma",
        type=float,
        default=10,
        help=(
            "Strength of the high pass filter applied before cross-correlation. "
            "This is the standard deviation of a Gaussian, in units of FFT "
            "pixels, i.e. larger number = stronger high pass filter. Default is "
            "10."
        ),
    )
    parser.add_argument(
        "--resize",
        type=float,
        default=1.0,
        help=(
            "The factor (0-1) to resize images for correlation. This will increase correlation "
            "speed, but can reduce reliability. Default is 1.0"
        ),
    )
    parser.add_argument(
        "--minimum_overlap",
        type=float,
        default=0.2,
        help=(
            "The minimum fractional overlap (as calculated from input positions) "
            "between two images for them to be correlated. If this is set to low "
            "unreliable correlations for images with very minimal overlap will be "
            "calculated.\n"
            "Default value is 0.2. This is calculated as the area of the overlap "
            "divided by the area of one image."
        ),
    )
    parser.add_argument(
        "--priority",
        type=str,
        default="time",
        help=(
            "Valid options are: 'time' or 'memory'\n"
            "'time' - cache images as long as possible for fastest stitching\n"
            "'memory' - load images from the filesystem each time they are required."
        ),
    )


def loading_settings_from_args(args: Namespace) -> ofs.LoadingSettings:
    """Process loading-related arguments and return settings"""
    csm = None if args.csm_matrix is None else ast.literal_eval(args.csm_matrix)
    return ofs.LoadingSettings(
        csm_matrix=csm,
        csm_calibration_width=args.csm_calibration_width,
    )


def correlation_settings_from_args(args: Namespace) -> ofs.CorrelationSettings:
    """Process correlation-related arguments and return settings"""
    return ofs.CorrelationSettings(
        pad=args.pad,
        resize=args.resize,
        high_pass_sigma=args.high_pass_sigma,
        minimum_overlap=args.minimum_overlap,
        priority=args.priority,
    )


def tiling_settings_from_args(args: Namespace) -> ofs.TilingSettings:
    """Process tiling-related arguments and return settings"""
    return ofs.TilingSettings(
        thresholding_method=args.thresholding_method,
        max_stage_discrepancy=args.max_stage_discrepancy,
        min_peak_quality=args.min_peak_quality,
    )


def output_settings_from_args(args: Namespace) -> ofs.OutputSettings:
    """Process loading-related arguments and return settings"""

    output_dir = args.input_folder if args.output_dir is None else args.output_dir

    legacy_mode = False
    if args.stitching_mode not in ALL_CLI_STITCHING_MODES:
        if args.stitching_mode == "only_stage_stitch":
            print(
                "\n\nWARNING! Using deprecated mode only_stage_stitch this will be "
                "removed soon.\n\n"
            )
            args.stitching_mode = "preview_stitch"
            legacy_mode = True
        else:
            # Use printing and an exit code for CLI input errors rather than a
            # python error with traceback
            print(f"Incorrect stitching mode {args.stitching_mode}, valid options are:\n")
            print(f"{ALL_CLI_STITCHING_MODES}")
            sys.exit(1)
    return ofs.OutputSettings(
        output_dir=output_dir,
        stitching_mode=args.stitching_mode,
        stitch_tiff=args.stitch_tiff,
        dzi=args.stitch_dzi,
        tile_size=args.tile_size,
        legacy_mode=legacy_mode,
    )


if __name__ == "__main__":
    load_tile_and_stitch_cli()
