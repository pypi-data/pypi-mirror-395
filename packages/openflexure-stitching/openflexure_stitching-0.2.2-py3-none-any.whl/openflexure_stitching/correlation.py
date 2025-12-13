r"""
Functions for cross-correlating overlapping images to estimate their displacements.

For speed cross-correlations are performed using fast Fourier Transforms. Denoting the
cross-correlation as $\star$, the Fourier Transform as $\mathcal{F}$. The for functions
$I$ and $J$ the cross-correlation can be calculated as
$$I \star J = \mathcal{F}^{-1}\left(\overline{\mathcal{F}(I)}\mathcal{F}(J)\right)$$
where $\overline{\mathcal{F}(I)}$ represents the complex conjugate of ${\mathcal{F}(I)}$,
and $\star$ represents the cross-correlation.

In the case where $I$ and $J$ are finite images rather than functions. The above formula
results in a circular-cross correlation. Leading to an ambiguity in the peak positions.

This module supports padding images to twice the size to mitigate this, (though with a
memory cost) or if no padding is further processing is performed can be used to
disambiguate peaks.

When performing cross correlations a high-pass Fourier filter is used to remove low
frequency image components.
"""

from typing import Optional

import numpy as np
from camera_stage_mapping.fft_image_tracking import (
    background_subtracted_centre_of_mass,
    high_pass_fourier_mask,
)

from openflexure_stitching.settings import CorrelationSettings

# Import from image.py directly not the loading.__init__.py to avoid circular dependency
from openflexure_stitching.loading.image import OFSImage


def fraction_under_threshold(corr: np.ndarray) -> dict[float, float]:
    """Measure the quality of a peak

    Use the fraction of the image below a threshold value as a measure of
    the quality of the correlation.

    Fractional thresholds are scaled such that 0 means the minimum value of
    the correlation image and 1 is the maximum. By default a single threshold
    of 0.9 is used.

    Return the fraction of nonzero pixels in the correlation image that
    are below the threshold, i.e. a greater number means a sharper peak.
    """

    frac_under_thresh: dict[float, float] = {}
    for thresh in [0.9]:  # previously [0.5, 0.75, 0.9, 0.95]:
        # The threshold is scaled such that 0 means min(corr) and
        # 1 means max(corr), and we count the fraction of pixels in
        # corr (the correlation result) beneath this value.

        corr_size = np.prod(corr.shape)
        abs_thresh = np.min(corr) + thresh * (np.max(corr) - np.min(corr))
        under_thresh = np.count_nonzero(corr < abs_thresh)
        frac_under_thresh[thresh] = under_thresh / corr_size
    return frac_under_thresh


def crosscorrelate_images(
    image1: OFSImage,
    image2: OFSImage,
    correlation_settings: CorrelationSettings,
    *,
    precalculated_filter: Optional[np.ndarray] = None,
    shift: bool = True,
    mask_width: int = 45,
) -> np.ndarray:
    """For the input pair of images, perform a cross-correlation

    :param image1: the first image as an OFSImage object
    :param image2: the second image as an OFSImage object
    :param correlation_settings: the correlation settings as a CorrelationSettings object
    :param precalculated_filter:  *Optional*, A np.ndarray containing the a pre-calculated
    copy of the Fourier high-pass filter this can be used to speed up correlating multiple
    images in a loop
    :param shift: If True a np.fftshift is applied to the image to shift zero displacement
    to the centre of the returned array
    :param mask_width: And area 2*mask_width x 2*mask width is blanked off in the centre of
    the image (or mask_width x mask width in each corner if not shifted). This is to blank
    out the false correlation values resulting from spectral leakage in the fast Fourier
    transforms used to calculate the cross correlation

    :return: The cross correlation, note this hasn't been shifted
    """

    cache_img_in_memory: bool = correlation_settings.priority == "time"

    fft1c = np.conj(
        image1.fft(
            resize=correlation_settings.resize,
            pad=correlation_settings.pad,
            cache_in_memory=False,
            cache_img_in_memory=cache_img_in_memory,
        )
    )
    fft2 = image2.fft(
        resize=correlation_settings.resize,
        pad=correlation_settings.pad,
        cache_in_memory=False,
        cache_img_in_memory=cache_img_in_memory,
    )

    if precalculated_filter is None:
        high_pass_filter = high_pass_fourier_mask(fft2.shape, correlation_settings.high_pass_sigma)
    else:
        high_pass_filter = precalculated_filter

    corr = np.fft.irfft2(fft1c * high_pass_filter * fft2)
    mean_corr = np.mean(corr)
    corr[0:mask_width, 0:mask_width] = mean_corr
    corr[-mask_width:, 0:mask_width] = mean_corr
    corr[-mask_width:, -mask_width:] = mean_corr
    corr[0:mask_width, -mask_width:] = mean_corr

    if shift:
        corr = np.fft.fftshift(corr)
    return corr


def displacement_from_crosscorrelation(
    image1: OFSImage,
    image2: OFSImage,
    correlation_settings: CorrelationSettings,
    *,
    precalculated_filter: Optional[np.ndarray] = None,
) -> tuple[np.ndarray, dict[float, float]]:
    """Estimate displacements between a pair of overlapping images using cross correlation

    :param image1: the first image as an OFSImage object
    :param image2: the second image as an OFSImage object
    :param correlation_settings: the correlation settings as a CorrelationSettings object
    :param precalculated_filter:  *Optional*, A np.ndarray containing the a pre-calculated
    copy of the Fourier high-pass filter this can be used to speed up correlating multiple
    images in a loop

    :return: A tuple containing:
    * The xy displacement in pixels as a numpy array
    * The fraction of pixels in the cross correlation under a threshold (0.9 of max)
    """

    corr = crosscorrelate_images(
        image1=image1,
        image2=image2,
        correlation_settings=correlation_settings,
        precalculated_filter=precalculated_filter,
        shift=False,
    )

    trial_peak = background_subtracted_centre_of_mass(
        corr, fractional_threshold=0.02, quadrant_swap=True
    )

    peak_loc = np.array(np.unravel_index(np.argmax(corr), np.array(corr).shape))
    if not correlation_settings.pad:
        # Use images to break ambiguity in cross correlation if performed
        # without padding. Images should be cached.
        trial_peak = _break_ties(
            image1.image_data(resize=correlation_settings.resize),
            image2.image_data(resize=correlation_settings.resize),
            peak_loc,
        )
    trial_peak *= -1
    displacement = trial_peak / correlation_settings.resize

    return (displacement, fraction_under_threshold(corr))


def _break_ties(
    overlay_image: np.ndarray,
    base_image: np.ndarray,
    peak_loc: np.ndarray,
) -> np.ndarray:
    """Evaluate the correlation of two images at four positions, to break FFT ambiguity"""
    # Ensure peak_loc is a 2-element array, between 0 and the image shape
    # peak_loc may be negative - if that's the case we flip it round
    size = np.array(base_image.shape[:2])

    peak_loc = np.array(peak_loc, dtype=np.int_) % size
    candidates = []
    # Every FFT correlation corresponds to four possible values - except if either
    # element is zero, at which point there's no ambiguity.
    # The comprehension below sets the quadrants we need to investigate.
    # `False` means a positive shift, `True` means a shift of `peak_loc[i]-size[i]`.
    quadrants = [
        [x_negative, y_negative]
        for x_negative in ([True, False] if peak_loc[0] != 0 else [False])
        for y_negative in ([True, False] if peak_loc[1] != 0 else [False])
    ]
    for quadrant in quadrants:
        score = _correlation_coefficient(
            base_image[_quadrant_slices(peak_loc, quadrant)],
            overlay_image[_quadrant_slices(-peak_loc, quadrant)],
        )
        candidates.append(
            {
                "score": score,
                "loc": peak_loc - size * np.array(quadrant),
                "quadrant": quadrant,
            }
        )

    best_candidate = np.argmax([c["score"] for c in candidates])
    return candidates[best_candidate]["loc"]


def _correlation_coefficient(patch1, patch2):
    """Calculate how well two patches of image correlate, i.e. their similarity"""
    if np.prod(patch1.shape) == 0 or np.prod(patch2.shape) == 0:
        return 0
    product = np.mean((patch1 - patch1.mean()) * (patch2 - patch2.mean()))
    stds = patch1.std() * patch2.std()
    if stds == 0:
        return 0
    product /= stds
    return product


def _quadrant_slices(split_point, quadrant):
    """XY slices to select a quadrant of an image

    This function returns a tuple of two slices, which will select
    one quadrant of an image, with its corner at `split_point`.

    `split_point` should be a 2 element array of integers between 0 and
    the image size.

    `quadrant` should be a 2 element array of booleans. `False` means
    we take the part of the image starting at `split_point` until the
    end of the axis - `True` will take the image from 0 up to
    `split_point`.

    If either element of `split_point` is negative, we flip the corresponding
    `quadrant` element - so `_quadrant_slices([-100, 100], [False, False])`
    will return `[slice(None, -100), slice(100, None)]`.
    """
    slices = []
    for sp, negative in zip(split_point, quadrant):
        if sp < 0:
            # If the split point <0 we will be indexing from the end of
            # the axis - so we flip the quadrant as well.
            negative = not negative
        if negative:
            slices.append(slice(None, sp))
        else:
            slices.append(slice(sp, None))
    return tuple(slices)
