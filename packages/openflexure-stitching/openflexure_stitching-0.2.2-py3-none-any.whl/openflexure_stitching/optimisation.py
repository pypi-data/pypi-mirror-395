"""
Methods to optimise the global position of images from correlation data.
"""

import gc
import time
from typing import Optional
from math import ceil
import numpy as np
import scipy
import scipy.sparse
from scipy.sparse import coo_matrix

from openflexure_stitching.settings import TilingSettings
from openflexure_stitching.types import PairData
from openflexure_stitching.loading import CorrelatedImageSet


def pair_displacements(
    pairs: list[PairData],
    positions: dict[str, np.ndarray],
) -> np.ndarray:
    """Calculate the displacement between each pair of positions specified.


    :param pairs: A list of tuples, where each tuple describes two images that overlap.
    :param positions: An Nx2 array, giving the 2D position in pixels of each image.

    :return: The 2D displacement between each pair of images.
    """

    return np.array([positions[p.keys[1]] - positions[p.keys[0]] for p in pairs])


def fully_connected(accepted_pairs: list[PairData], all_pairs: list[PairData]) -> bool:
    """Determine whether the pairs connect all N images"""
    all_keys_pairs = [i.keys for i in all_pairs]
    all_keys = set([key for key_pair in all_keys_pairs for key in key_pair])
    total_images = len(all_keys)
    assert total_images > 0
    connected_images = set()
    previous_n_connected = 0
    connected_images.add(all_keys_pairs[0][0])
    # Each iteration, add any images that are connected to
    # the set - stop when no more images are added.
    while len(connected_images) > previous_n_connected:
        previous_n_connected = len(connected_images)
        for pair in accepted_pairs:
            for i in range(2):
                if pair.keys[i] in connected_images:
                    connected_images.add(pair.keys[1 - i])
    return len(connected_images) == total_images


def rms_error_position_discrepancy(
    accepted_pairs: list[PairData],
    positions: dict[str, np.ndarray],
    all_pairs: list[PairData],
    print_err: bool = False,
) -> float:
    """Find the RMS error in image positions vs correlated displacements


    :param accepted_pairs: The output from correlating pairs of images, filtered by thresholds
    :param positions: The global position of each image in pixels, relative to the mean, as
    optimised by least squares
    :param all_pairs: Every pair of overlapping images, unfiltered
    :param print_err:  If true, print the RMS error to the console.

    :return: The RMS difference between the displacements between paired images calculated from:
    * From the global positions of each image as optimised by least squares
    * From the displacement estimated from cross-correlation

    """
    # Over constrained fit, not enough values
    if len(accepted_pairs) <= len(positions) - 1:
        return float("infinity")
    # Check that every tile in the image is connceted to every other tile by some path.
    if not fully_connected(accepted_pairs, all_pairs):
        # if not return an infinite RMS error
        return float("infinity")

    displacements = np.array([p.image_displacement for p in accepted_pairs])
    # Note we are taking stdev of an array with 2*N elements, if we have N pairs.
    rms_err = np.std(
        pair_displacements(accepted_pairs, positions) - displacements,
        ddof=2 * len(positions) - 2,
    )
    # We then fit 2*len(positions)-2 parameters
    if print_err:
        print(f"RMS Error: {round(rms_err, 2)} pixels")
    return rms_err


def images_in_pairs_list(pairs: list[PairData]) -> list[str]:
    """Find all images mentioned in a list of pairs"""
    return list(set(key for p in pairs for key in p.keys))


def fit_positions_lstsq(
    image_set: CorrelatedImageSet,
    accepted_pairs: list[PairData],
    stage_pairs: Optional[list[PairData]] = None,
    stage_weighting: float = 0.1,
) -> dict[str, np.ndarray]:
    """Find the least squares solution for image placement.

    Placing N images such that the pair-wise displacements match those measured
    can be formulated as a linear least squares problem, because for each
    measured displacement, it can be written as a dot product between a vector
    with exactly two nonzero elements (one +1 and one -1) and the position
    vector.

    This function calculates a matrix A such that each row of A is such a vector,
    and then uses that, together with the measured displacements, to recover the
    positions. In order to make sure the problem is constrained, we add an
    extra two rows, constraining the mean position to be zero. We could trivially
    modify this to set an arbitrary mean position.

    If `pairs` does not connect all the images, this will be ill-posed and we'll
    have a problem. `fallback_pairs` allows us to pass in additional pair data
    that will be used with a low weighting (`fallback_weighting`) to break the
    ambiguity. Typically this is generated from stage coordinates, for images
    that otherwise would be left floating.

    :param image_set: The set of images to optimise the positions of
    :param accepted_pairs: The pairs of images that are within the thresholding and
    will be positioned by their correlated displacements
    :param stage_pairs: Optional, The remaining pairs outside the threshold to be
    positioned with a low weighting
    :param stage_weighting: The weighting of stage displacements in the minimisation

    :returns: dictionary of the position for each image key
    """
    if stage_pairs is None:
        stage_pairs = []

    paired_image_keys = images_in_pairs_list(accepted_pairs + stage_pairs)

    # Reorder based on the order in the original image_set:
    paired_image_keys = [key for key in image_set.keys() if key in paired_image_keys]
    # Create dictionary for fast lookup
    key_to_index = {k: i for i, k in enumerate(paired_image_keys)}

    paired_images_count = len(paired_image_keys)
    pairs_count = len(accepted_pairs + stage_pairs)

    displacements = np.array([p.image_displacement for p in accepted_pairs])
    stage_displacements = np.array([p.stage_displacement for p in stage_pairs])
    # Flatten displacements
    d = np.concatenate(
        [
            np.reshape(displacements, 2 * len(accepted_pairs)),
            np.reshape(stage_displacements, 2 * len(stage_pairs)) * stage_weighting,
            np.array([0, 0]),
        ]
    )

    rows = []
    cols = []
    vals = []

    for i, pair in enumerate(accepted_pairs):
        a, b = (key_to_index[ind] for ind in pair.keys)
        for j in range(2):
            row = 2 * i + j
            rows += [row, row]
            cols += [2 * a + j, 2 * b + j]
            vals += [-1.0, 1.0]

    i0 = len(accepted_pairs)
    for i, pair in enumerate(stage_pairs):
        a, b = (key_to_index[ind] for ind in pair.keys)
        for j in range(2):
            row = 2 * (i + i0) + j
            rows += [row, row]
            cols += [2 * a + j, 2 * b + j]
            vals += [-stage_weighting, stage_weighting]

    # Add mean constraint rows
    for j in range(2):
        for i in range(paired_images_count):
            rows.append(2 * pairs_count + j)
            cols.append(2 * i + j)
            vals.append(1 / paired_images_count)

    # Build matrix
    matrix_shape = (2 * pairs_count + 2, 2 * paired_images_count)
    vals_and_coords = (np.array(vals), (np.array(rows), np.array(cols)))
    pairs_matrix = coo_matrix(vals_and_coords, shape=matrix_shape).tolil()

    # Solve least squares
    pairs_csr = pairs_matrix.tocsr()
    # Predefine as array so MyPy doesn't complain about reshaping.
    fitted_positions: np.ndarray
    fitted_positions = scipy.sparse.linalg.lsqr(pairs_csr, d)[0]
    fitted_positions = fitted_positions.reshape(paired_images_count, 2)

    # return a dictionary
    all_positions = {}
    for i, key in enumerate(paired_image_keys):
        all_positions[key] = fitted_positions[i, :]
    return all_positions


def test_fit_with_thresholds(
    image_set: CorrelatedImageSet,
    peak_qual_thresh: float,
    stage_discrep_thresh: float,
    cache: Optional[dict[int, float]],
) -> tuple[float, int]:
    """Evaluate the RMS error when we use a particular threshold

    Optionally, a cache dictionary can be supplied, in which case
    we'll use it to avoid solving for any subset of the pairs more
    than once.
    """
    accepted_pairs = image_set.filtered_pairs(peak_qual_thresh, stage_discrep_thresh)

    if len(accepted_pairs) == 0:
        return float("infinity"), 0  # Clearly we can't throw away all the pairs!
    cache_key = hash(str(tuple(p.keys for p in accepted_pairs)))
    if cache and cache_key in cache:
        return cache[cache_key], len(accepted_pairs)
    positions = fit_positions_lstsq(image_set, accepted_pairs)
    rms_err = rms_error_position_discrepancy(accepted_pairs, positions, image_set.pairs)
    if cache is not None:
        cache[cache_key] = rms_err
    return rms_err, len(accepted_pairs)


def manual_threshold():
    """Let the user set the x and y thresholds for stitching"""
    print("\n\nPlease set thresholds based on the data in stitching_correlations.png:\n")
    peak_qual_thresh = float(input("Insert min_peak_quality threshold (x-axis): "))
    stage_discrep_thresh = float(input("Insert max_stage_discrepancy threshold (y-axis): "))
    return peak_qual_thresh, stage_discrep_thresh


def resample_and_sort_list(
    input_list: list, indicative_length: int = 60, reverse: bool = False
) -> list:
    """
    Sort and resample a list.

    This is used to reduce the number of possible thresholds we compare against.

    :param input_list: The list to resample and sort
    :param indicative_length: above this length the input list is resampled (Default=60)
    :param reverse: Sort in reverse order if True (Default=False)

    :return: The resampled and sorted list

    The resampling algorithm is to take the number of point above the indicative_length
    and calculate the square root of a 3rd of this number. We resample to this rounded
    up.

    As such for lists approximately equal in length to indicative_length the resampling
    keeps them a similar size. For arrays that are much larger in length the length
    approaches the square root of a 3rd of the total length.

    This is chosen to speed up stitching approximately proportionally to the radius of the
    a circular scan.
    """
    sorted_list = sorted(input_list, reverse=reverse)

    if len(sorted_list) <= indicative_length:
        return sorted_list

    root_of_third_of_extra = np.sqrt(len(sorted_list) - indicative_length) / 3
    resample_factor = ceil(root_of_third_of_extra)
    return sorted_list[::resample_factor]


def optimise_peak_and_discrepancy_thresholds(
    image_set: CorrelatedImageSet, tiling_settings: Optional[TilingSettings] = None
) -> tuple[float, float]:
    """
    Optimise the peak quality and stage discrepancy thresholds.

    Optimise the peak quality and stage discrepancy thresholds by repeatedly performing
    the fit with stricter threasholds. The RMS error will decrease as poor quality pairings
    are removed. However once too many points are excluded the RMS error will increase.

    Return the thresholds that produce the minimum RMS error
    """
    if tiling_settings is None:
        tiling_settings = TilingSettings()
    max_stage_discrepancy = tiling_settings.max_stage_discrepancy
    min_peak_quality = tiling_settings.min_peak_quality

    # The possible threshold values for peak quality are calculated from all the unique values
    # for the quality. These are quantised because they are calculated from the division of
    # two integers
    unique_peak_quals = list(set(image_set.correlation_peak_qualities()))

    # Possible threshold for stage discrepancy is any stage discrepany point.
    all_stage_discreps = image_set.position_discrepancies(normalise=True)

    print(
        f"Starting with {len(unique_peak_quals)} possible peak quality thresholds and "
        f"{len(all_stage_discreps)} possible stage discrepancy thresholds",
        flush=True,
    )

    # Filter based on user input if appropriate
    if min_peak_quality is not None:
        unique_peak_quals = [i for i in unique_peak_quals if i > min_peak_quality]

    # Setting a maximum discrepency between stage and correlation before sampling
    if max_stage_discrepancy is not None:
        all_stage_discreps = [i for i in all_stage_discreps if i < max_stage_discrepancy]

    unique_peak_quals = resample_and_sort_list(unique_peak_quals)
    # Reverse this to start with maximum
    all_stage_discreps = resample_and_sort_list(all_stage_discreps, reverse=True)

    print(
        f"After filtering and resampling {len(unique_peak_quals)} peak quality thresholds "
        f"and {len(all_stage_discreps)} stage discrepancy thresholds will be trialed for "
        "fit quality.",
        flush=True,
    )

    # Perform the fits!
    test_values = fit_with_all_thresholds_until_turnaround(
        image_set, unique_peak_quals, all_stage_discreps
    )

    # Unpack the tuple
    peak_qual_thresholds, stage_discrep_thresholds, rms_errors, n_pairs = test_values

    not_infinite_rms = np.min(rms_errors) < float("infinity")
    min_i = np.argmin(rms_errors) if not_infinite_rms else np.argmax(n_pairs)

    chosen_peak_qual_thresh = peak_qual_thresholds[min_i]
    chosen_stage_discrep_thresh = stage_discrep_thresholds[min_i]

    return chosen_peak_qual_thresh, chosen_stage_discrep_thresh


def fit_with_all_thresholds_until_turnaround(
    image_set, peak_quality_thresholds, stage_discrep_thresholds
):
    """
    Perform a least squares fit for image placement with increasingly severe thresholds until
    RMS error increases.

    Start with all pairs of correlations contributing to the fit (Except those filtered by
    min_peak_quality or max_stage_discrepancy). Iterate over all threshold combinations
    until the RMS error increases
    """
    tested = []
    cached_errors: dict[int, float] = {}
    start = time.time()
    total_tests = len(peak_quality_thresholds) * len(stage_discrep_thresholds)

    # Starting with the laxest thresholds

    for peak_qual_thresh in peak_quality_thresholds:
        rms_err_for_this_peak_thresh = []
        for stage_discrep_thresh in stage_discrep_thresholds:
            rms_err, n_pairs = test_fit_with_thresholds(
                image_set, peak_qual_thresh, stage_discrep_thresh, cache=cached_errors
            )

            tested.append([peak_qual_thresh, stage_discrep_thresh, rms_err, n_pairs])

            if rms_err == float("infinity"):
                if stage_discrep_thresh == stage_discrep_thresholds[0]:
                    # If the rms error is infinte then we have reduced the number of points so low
                    # that no more fits will pass. Testing complete, return the tested results.
                    # See comment on final return.
                    return zip(*tested)
                break

            rms_err_for_this_peak_thresh.append(rms_err)

            # Manually running garbage collection helps stop the memory filling up
            gc.collect()
            if time.time() - start > 30:
                print(
                    f"Still finding suitable thresholds, done {len(tested)} out of {total_tests}",
                    flush=True,
                )
                start = time.time()

    # re zip the lists to return a tuple of the following lists:
    # peak_qual_thresholds, stage_discrep_thresholds, errors, n_pairs
    return zip(*tested)
