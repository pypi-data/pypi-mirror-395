"""The high level stitching algorithm, used to take a folder
path and other optional arguments, and perform the analysis,
correlations, optimisations and stitching of images"""

from typing import Optional
import warnings
import os

import numpy as np

from .loading import (
    OFSImageSet,
    CorrelatedImageSet,
    load_cached_correlated_image_set,
    save_cached_correlated_image_set,
)
from .settings import LoadingSettings, CorrelationSettings, TilingSettings, OutputSettings
from . import plotting
from .optimisation import (
    optimise_peak_and_discrepancy_thresholds,
    fit_positions_lstsq,
    manual_threshold,
)
from .stitching import (
    stitch_and_save,
    StitchGeometry,
    create_thumbnail,
    convert_jpeg_to_pyramidal_image,
)
from .transforms import apply_affine_transform, fit_affine_transform
from .types import PairData


ALL_CLI_STITCHING_MODES = ["all", "only_correlate", "preview_stitch", "stage_stitch"]
PYTHON_STITCHING_MODES = ["return_positions"]
ALL_STITCHING_MODES = ALL_CLI_STITCHING_MODES + PYTHON_STITCHING_MODES


def load_tile_and_stitch(
    folder: str,
    *,
    loading_settings: Optional[LoadingSettings] = None,
    correlation_settings: Optional[CorrelationSettings] = None,
    tiling_settings: Optional[TilingSettings] = None,
    output_settings: Optional[OutputSettings] = None,
) -> Optional[tuple[CorrelatedImageSet, dict[str, np.ndarray]]]:
    """Load images, correlate them together, and output stitched images to disk

    This is the top-level function that goes from a folder of input
    images to producing the final saved stitched images. It is the function
    called by the command line utility

    :param folder: The folder containing the input images. The cache and stitched
    images will be added to this folder
    :param loading_settings: *Optional* The settings for loading images. If not set
    the defaults specified in `openflexure_stitching.types.LoadingSettings` will be
    used.
    :param correlation_settings: *Optional* The settings for correlating images.
    If not set the defaults specified in `openflexure_stitching.types.CorrelationSettings`
    will be used.
    :param tiling_settings: *Optional* The settings for optimising image positions.
    If not set the defaults specified in `openflexure_stitching.types.TilingSettings`
    will be used.
    :param output_settings: *Optional* The settings for stitching images. If not set
    the defaults specified in `openflexure_stitching.types.OutputSettings` will be
    used.

    :return: If output_settings.stitching_mode == "return_positions", then the images
    as a CorrelatedImageSet and a dictionary of global image positions are returned.
    Else nothing is returned

    """

    if output_settings is None:
        output_settings = OutputSettings()
    if correlation_settings is None:
        correlation_settings = CorrelationSettings()
    if tiling_settings is None:
        tiling_settings = TilingSettings()

    if output_settings.stitching_mode not in ALL_STITCHING_MODES:
        raise ValueError(f"Not a valid stitching mode. Options are:\n{ALL_STITCHING_MODES}")

    if output_settings.legacy_mode:
        # This should only show in development mode not from CLI, CLI warns separately
        warnings.warn("Legacy mode will be removed soon", DeprecationWarning)

    # Create the output dir if it doesn't exist
    os.makedirs(output_settings.output_dir, exist_ok=True)

    # If "stage_stitch" or "only_correlate", don't run full pipeline, just run these
    # functions and return
    if output_settings.stitching_mode == "stage_stitch":
        image_set = OFSImageSet(folder, loading_settings=loading_settings)
        perform_stitch_from_stage(image_set, output_settings)
        return None
    if output_settings.stitching_mode == "only_correlate":
        # With caching on this will cache
        load_and_cache_correlated_image_set(
            folder, loading_settings=loading_settings, correlation_settings=correlation_settings
        )
        return None

    print("Finding a list of all overlapping images", flush=True)
    image_set = load_and_cache_correlated_image_set(
        folder, loading_settings=loading_settings, correlation_settings=correlation_settings
    )

    print("Getting all the image info ready to stitch", flush=True)

    # Don't plot the input locations if only running correlations
    if output_settings.stitching_mode != "only_correlate":
        print("Plotting the inputs to stitching", flush=True)
        f = plotting.plot_inputs(image_set)
        f.savefig(
            os.path.join(folder, "stitching_inputs.png"),
            dpi=250,
            bbox_inches="tight",
            facecolor="white",
        )
        f.clear()

    # Plot the thresholds and save only if using a CLI method
    plot_thresholds = output_settings.stitching_mode in ALL_CLI_STITCHING_MODES
    peak_qual_thresh, stage_discrep_thresh = determine_thresholds(
        image_set, tiling_settings=tiling_settings, plot=plot_thresholds
    )

    positions = perform_final_position_optimisation(
        image_set, peak_qual_thresh, stage_discrep_thresh
    )

    save_fiji_config(positions, output_settings=output_settings)

    if output_settings.stitching_mode == "return_positions":
        # If being run from python with return_positions simply return them
        # now rather than perform stitching
        return image_set, positions

    preview_path = save_preview(image_set, positions, output_settings=output_settings)
    create_thumbnail(preview_path)

    if output_settings.stitching_mode == "all":
        save_full_stitch(
            image_set,
            positions,
            output_settings=output_settings,
        )

    return None


def load_and_cache_correlated_image_set(
    folder: str,
    loading_settings: Optional[LoadingSettings],
    correlation_settings: Optional[CorrelationSettings],
) -> CorrelatedImageSet:
    """Load a `openflexure_stitching.loading.CorrelatedImageSet`
    with as much data as possible loaded from the json cache in
    ths supplied folder. Any images added since will be correlated.
    This is used to improve performance allowing the the set to be
    loaded from disk rather than regenerated. Once loaded the cache
    is updated.

    The cache is "keyed" on the correlation settings, so if these
    change, correlations are re-calculated. Previous settings are still
    kept in the cache, so it is possible to switch between settings without
    loosing cached data.

    :param folder: The folder containing the input images and cache
    :param loading_settings: *Optional* The settings for loading images. If not set
    the defaults specified in `openflexure_stitching.types.LoadingSettings` will be
    used.
    :param correlation_settings: *Optional* The settings for correlating images.
    If not set the defaults specified in `openflexure_stitching.types.CorrelationSettings`
    will be used.
    """
    cached = load_cached_correlated_image_set(folder, correlation_settings)
    image_set = CorrelatedImageSet(
        folder,
        loading_settings=loading_settings,
        correlation_settings=correlation_settings,
        cached=cached,
    )
    save_cached_correlated_image_set(folder, image_set.data_for_caching())
    return image_set


def save_preview(
    image_set: OFSImageSet, positions: dict[str, np.ndarray], output_settings: OutputSettings
) -> str:
    """Save the preview image. This is calculated from the optimised positions
    but each image is downsampled to give a final image 1000px wide.

    :param image_set: The set of images to be stitched
    :param positions: The dictionary of optimised image positions.
    :param output_settings: The output settings object. This can be used to set the output
    directory and if legacy_mode is True the preview is saved to "stitched_from_stage.jpg"
    rather than "preview.jpg" this is for compatibility with early pre-releases of v3 of
    the OpenFlexure Server. The mode will be removed soon.

    :return: The path to the saved preview JPEG
    """
    fname = "preview.jpg" if not output_settings.legacy_mode else "stitched_from_stage.jpg"
    fpath = os.path.join(output_settings.output_dir, fname)
    stitch_geometry = StitchGeometry(image_set, positions=positions, target_image_width=1000)
    stitch_and_save(fpath, stitch_geometry=stitch_geometry)
    return fpath


def save_full_stitch(
    image_set: OFSImageSet,
    positions: dict[str, np.ndarray],
    output_settings: OutputSettings,
) -> None:
    """Save the full stitched image to disk.

    :param image_set: The set of images to be stitched
    :param positions: The dictionary of optimised image positions.
    :param output_settings: The output settings object. This can be used to set the output
    directory, and whether a pyramidal TIFF or DZI is generated
    """
    prefix = choose_final_filename_prefix(image_set.folder)
    stitch_geometry = StitchGeometry(image_set, positions=positions)
    if stitch_geometry.downsample > 1:
        print(f"Downsampling by {stitch_geometry.downsample}")

    fpath = os.path.join(output_settings.output_dir, f"{prefix}_stitched.jpg")
    stitch_and_save(
        fpath, stitch_geometry=stitch_geometry, use_vips=True, tile_size=output_settings.tile_size
    )
    convert_jpeg_to_pyramidal_image(
        fpath,
        output_settings.dzi,
        output_settings.stitch_tiff,
        pixel_size_um=stitch_geometry.pixel_size_um,
    )


def save_fiji_config(
    positions: dict[str, np.ndarray],
    output_settings: OutputSettings,
) -> None:
    """Save a config file for Fiji  to stitch from

    The file save is called OFMTileConfiguration.txt and is saved into the
    output directory. Using Fiji allows for artificial smoothing
    """

    filename = os.path.join(output_settings.output_dir, "OFMTileConfiguration.txt")
    with open(filename, "w", encoding="utf-8") as fp:
        fp.write("# Define the number of dimensions used\n")
        fp.write("dim = 2\n\n# Define the image coordinates\n")

        for image, pos in positions.items():
            fp.write(f"{image}; ; {float(pos[1]), float(pos[0])} \n")


def determine_thresholds(
    image_set: CorrelatedImageSet,
    tiling_settings: TilingSettings,
    plot: bool = True,
) -> tuple[float, float]:
    """
    Determine the thresholds used for selecting correlations used in position optimisation

    :param image_set: The set of images. Must be a CorrelatedImageSet not a OFSImageSet
    :param tiling_settings: *Optional* The settings for optimising image positions.
    If not set the defaults specified in `openflexure_stitching.types.TilingSettings`
    will be used.
    :param plot: Set to True to save the stitching correlation plot to disk.

    :return: Tuple containing (peak quality threshold, stage discrepancy threshold)

    See `perform_final_position_optimisation`
    """
    manual = tiling_settings.thresholding_method == "manual"
    if not manual:
        print("Finding the optimal threshold", flush=True)
        peak_qual_thresh, stage_discrep_thresh = optimise_peak_and_discrepancy_thresholds(
            image_set, tiling_settings=tiling_settings
        )
    else:
        print('Displaying correlations as "stitching_correlations.png"', flush=True)
        if plot:
            f = plotting.plot_overlaps(image_set)
            f.savefig(os.path.join(image_set.folder, "stitching_correlations.png"))
        peak_qual_thresh, stage_discrep_thresh = manual_threshold()

    if plot:
        f = plotting.plot_overlaps(image_set, peak_qual_thresh, stage_discrep_thresh)
        f.savefig(os.path.join(image_set.folder, "stitching_correlations.png"))
    return peak_qual_thresh, stage_discrep_thresh


def perform_final_position_optimisation(
    image_set: CorrelatedImageSet, peak_qual_thresh: float, stage_discrep_thresh: float
) -> dict[str, np.ndarray]:
    """Return a dictionary of the final optimised positions for an image set

    :param image_set: The set of images. Must be a CorrelatedImageSet not a OFSImageSet
    :param peak_qual_thresh: The threshold for correlation peak quality, if the measured
    correlation peak quality for a pair is lower than this number than this then only
    the pair's stage positions will be used for placement.
    :param stage_discrep_thresh: The threshold for stage discrepancy. This is the
    difference between the displacement between two images as estimated from the stage
    and from correlation. If the discrepancy is above the set threshold then only
    the pair's stage positions will be used for placement.

    See also `determine_thresholds`
    """
    filtered_pairs = image_set.filtered_pairs(peak_qual_thresh, stage_discrep_thresh)

    print(
        f"Using {len(filtered_pairs)} of the {len(image_set.pairs)} pairs for final optimisation"
    )

    transform = perform_affine_transform_fit(filtered_pairs)
    rejected_pairs = [p for p in image_set.pairs if p not in filtered_pairs]

    if transform is not None:
        rejected_pairs = apply_affine_transform(rejected_pairs, transform)
        if image_set.camera_to_sample_matrix is not None:
            improved_csm = np.linalg.inv(
                np.linalg.inv(image_set.camera_to_sample_matrix) @ np.linalg.inv(transform)
            )
            improved_csm_str = format_csm_to_string(improved_csm)
            # Format arrays into single line strings, elements separated by a comma
            # and maintaining brackets

            starting_csm_str = format_csm_to_string(image_set.camera_to_sample_matrix)
            print(f"Starting csm is {starting_csm_str}", flush=True)
            print(
                f"A better starting estimate of the csm is {improved_csm_str}. ",
                flush=True,
            )

    positions = fit_positions_lstsq(image_set, filtered_pairs, stage_pairs=rejected_pairs)
    return positions


def format_csm_to_string(csm: np.ndarray) -> str:
    """Convert a CSM np array into a single-line string for printing.

    The np array will be turned into a string, with each element seperated
    by a comma and space. The new line will be removed, leaving a string of
    format '[[a, b], [c, d]]'
    """
    # precision=4 as 4 decimal places is precise enough while still readable
    # suppress_small prevents one small value causing all elements to be
    # formatted in scientific notation.
    csm_string = np.array2string(csm, separator=", ", precision=4, suppress_small=True)
    return csm_string.replace("\n", "")


def perform_affine_transform_fit(filtered_pairs: list[PairData]) -> Optional[np.ndarray]:
    """
    Fit an affine transform to the pairs that were within the threshold this
    is used to adjust the positions of the rejected pairs before final poistion
    optimisation.

    :param filtered_pairs: The pairs of images with correlations that met the determined
    quality thresholds. See `determine_thresholds`

    :return: The Affine transform as a numpy array
    """
    # Calculate from the filtered pairs the x and y displacements between images
    stage_displacements = np.array([x.stage_displacement for x in filtered_pairs])
    abs_x_disp = np.abs(stage_displacements[:, 0])
    abs_y_disp = np.abs(stage_displacements[:, 1])

    if np.all(abs_x_disp < 30) or np.all(abs_y_disp < 30):
        print(
            "After thresholding the only image pairs that remain are all vertical or "
            "all horizontally paired. Thresholding or other input settings need adjusting"
        )
        return None

    return fit_affine_transform(filtered_pairs)


def perform_stitch_from_stage(image_set: OFSImageSet, output_settings: OutputSettings):
    """
    For the given image set, stitch the images based only on stage coordinates
    not correlation an optimisation

    :param image_set: The set of images to stitch
    :param output_settings: The output settings object. This can be used to set the output
    directory
    """
    fpath = os.path.join(output_settings.output_dir, "stitched_from_stage.jpg")
    stitch_geometry = StitchGeometry(image_set, target_image_width=1000)
    stitch_and_save(fpath, stitch_geometry)


def choose_final_filename_prefix(folder: str) -> str:
    """Chooses a file name based on the path:

    Names it based on the containing folder, unless it's called "images" or "use"
    as these are automatically generated by the openflexure server inside a scan
    directory. In this case we take the name of the containing directory.

    :param folder: The filepath of the directory containing the images.

    :return: The prefix for output images.

    For example:
      - images_folder: /home/name/files/scans/my_pretty_scan/
        output_image: my_pretty_scan_stitched.jpg
      - images_folder: /home/name/files/scans/my_scan/images
        output_image: my_scan_stitched.jpg
      - images_folder: /home/name/files/scans/another_scan/use/images
        output_image: another_scan_stitched.jpg

    In the unlikely case that all directory names are "use" and "images"
    the result will be called scan
      - images_folder: /images/use/images/use/use/use/images/use/images/
        output_image: scan_stitched.jpg
    """
    scan_dir_path = os.path.abspath(folder)
    # Remove windows drive letters with splitdrive
    _, scan_dir_path = os.path.splitdrive(scan_dir_path)
    directories = scan_dir_path.split(os.sep)

    while directories:
        dir_name = directories.pop()
        if not dir_name:
            # Continue if empty (normpath should fix this unless we reach root)
            continue
        if dir_name not in ["images", "use"]:
            # return the first dir name that isn't use or images
            return dir_name
    return "scan"
