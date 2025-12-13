"""
A collection of methods to plot data using matplotlib

Plotting is intentionally kept separate from the rest of
the stitching and tiling process to avoid hard dependencies
on matplotlib and make sure code can run headless.
"""

from typing import Optional

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib import patches

from openflexure_stitching.loading import CorrelatedImageSet


def plot_overlaps(
    image_set: CorrelatedImageSet,
    peak_qual_thresh: Optional[float] = None,
    stage_discrep_thresh: Optional[float] = None,
) -> Figure:
    """Plot the correlations between images"""
    f, ax = plt.subplots(1, 2)
    ax[0].set_yscale("log")
    peak_quals = image_set.correlation_peak_qualities()
    discrepancies = image_set.position_discrepancies(normalise=True)

    ax[0].plot(peak_quals, discrepancies, "o")
    if peak_qual_thresh:
        ax[0].axvline(peak_qual_thresh)
    if stage_discrep_thresh:
        ax[0].axhline(stage_discrep_thresh)
    if peak_qual_thresh and stage_discrep_thresh:
        ax[0].add_patch(
            patches.Rectangle(
                xy=(peak_qual_thresh, stage_discrep_thresh),  # point of origin.
                width=1 - peak_qual_thresh,
                height=-(stage_discrep_thresh),
                linewidth=0,
                fill=True,
                facecolor=(0, 1, 0, 0.3),
            )
        )
    ax[0].set_xlabel("Peak quality (higher is better)")
    ax[0].set_ylabel("Stage - correlation discrepancy /px \n (lower is better)")
    f.tight_layout()

    if peak_qual_thresh is not None and stage_discrep_thresh is not None:
        peak_quals_arr = np.asarray(peak_quals)
        discrepancies_arr = np.asarray(discrepancies)
        good_peaks = peak_quals_arr > peak_qual_thresh
        good_discreps = discrepancies_arr < stage_discrep_thresh
        mask = good_peaks & good_discreps
        n_good = np.sum(mask)

        ax[1].scatter(
            peak_quals_arr[mask], discrepancies_arr[mask], c=np.arange(n_good) % 10, cmap="tab10"
        )

        ax[1].axvline(peak_qual_thresh)
        ax[1].axhline(stage_discrep_thresh)
    f.tight_layout()
    return f


def plot_inputs(image_set: CorrelatedImageSet) -> Figure:
    """Plot the coordinates of images

    Note: because of the differing conventions between matplotlib and PIL,
    the y axis is in fact the **first** coordinate and the x axis is the
    **second**. Also, the y axis runs backwards. This is just to make the
    two match up, so the graph resembles the stitched image.
    """
    xs = [i.stage_position_px[1] for i in image_set]
    ys = [i.stage_position_px[0] for i in image_set]

    # Compute dx, dy and median step length
    dxs = np.diff(xs)
    dys = np.diff(ys)
    step_lengths = np.sqrt(dxs**2 + dys**2)

    median_step = np.median(step_lengths)

    # Choose scale factors
    head_width_factor = 0.15  # fraction of median movement
    head_length_factor = 0.25

    # Head size based on median step
    head_width = median_step * head_width_factor
    head_length = median_step * head_length_factor

    f, ax = plt.subplots(figsize=(12, 9))

    # Draw each movement as an arrow
    for x0, y0, x1, y1 in zip(xs[:-1], ys[:-1], xs[1:], ys[1:]):
        dx = x1 - x0
        dy = y1 - y0

        ax.arrow(
            x0,
            y0,
            dx,
            dy,
            length_includes_head=True,
            head_width=head_width,
            head_length=head_length,
            linewidth=1.5,
            color="C0",
        )

    # Draw a rectangle to represent each image
    shape = image_set.image_shape
    for image in image_set:
        centre_pos = [i - s / 2 for i, s in zip(image.stage_position_px, shape)]
        ax.add_patch(
            patches.Rectangle(
                tuple(reversed(centre_pos)),
                shape[1],
                shape[0],
                linewidth=1,
                edgecolor="b",
                facecolor=(0, 0, 1.0, 0.2),
            )
        )
    ax.invert_yaxis()
    ax.set_xlabel("Position element [1]/pixels", fontsize=16)
    ax.set_ylabel("Position element [0]/pixels", fontsize=16)
    ax.tick_params(labelsize=14)
    ax.set_aspect(1.0)
    return f


def plot_pairs(peak, img_i, img_j, corr, stage_displacement, conf) -> Figure:
    """Plot the correlations and proposed stitched image for a given pair of images"""
    fig, axs = plt.subplots(2, 3)
    axs[0, 0].imshow(img_i)
    axs[0, 0].scatter(peak[1], peak[0], edgecolors="red", facecolors="none")
    axs[0, 1].imshow(img_j)
    axs[1, 0].imshow(corr)
    axs[1, 0].scatter(peak[1], peak[0], edgecolors="red", facecolors="none")

    peak = np.asarray(peak).astype(int)
    starting_peak = peak.copy()

    canvas = np.zeros([int(abs(peak[0]) + img_i.shape[0]), int(abs(peak[1]) + img_i.shape[1]), 3])
    if peak[1] >= 0:
        if peak[0] >= 0:
            canvas[: img_i.shape[0], : img_i.shape[1]] = img_i
            canvas[peak[0] : peak[0] + img_i.shape[0], peak[1] : peak[1] + img_i.shape[1]] = img_j
        else:
            canvas[-peak[0] : -peak[0] + img_i.shape[0], : img_i.shape[1]] = img_i
            canvas[: img_i.shape[0], peak[1] : peak[1] + img_i.shape[1]] = img_j
    elif peak[0] >= 0:
        canvas[: img_i.shape[0], -peak[1] : -peak[1] + img_i.shape[1]] = img_i
        canvas[peak[0] : peak[0] + img_i.shape[0], : img_i.shape[1]] = img_j
    else:
        canvas[
            -peak[0] : -peak[0] + img_i.shape[0],
            -peak[1] : -peak[1] + img_i.shape[1],
        ] = img_i
        canvas[: img_i.shape[0], : img_i.shape[1]] = img_j
    axs[1, 1].imshow(canvas.astype(np.uint8))

    axs[1, 0].set_xlabel(
        f"{stage_displacement}, {peak}, \n"
        f"{[stage_displacement[i] - peak[i] for i in range(len(stage_displacement))]}, {conf}"
    )

    offsets = np.abs([stage_displacement[i] - peak[i] for i in range(len(stage_displacement))])
    axis = np.argmax(offsets)
    peak = starting_peak.copy()
    peak[axis] -= img_i.shape[axis]

    canvas = np.zeros([int(abs(peak[0]) + img_i.shape[0]), int(abs(peak[1]) + img_i.shape[1]), 3])

    if peak[1] >= 0:
        if peak[0] >= 0:
            canvas[: img_i.shape[0], : img_i.shape[1]] = img_i
            canvas[peak[0] : peak[0] + img_i.shape[0], peak[1] : peak[1] + img_i.shape[1]] = img_j
        else:
            canvas[-peak[0] : -peak[0] + img_i.shape[0], : img_i.shape[1]] = img_i
            canvas[: img_i.shape[0], peak[1] : peak[1] + img_i.shape[1]] = img_j
    elif peak[0] >= 0:
        canvas[: img_i.shape[0], -peak[1] : -peak[1] + img_i.shape[1]] = img_i
        canvas[peak[0] : peak[0] + img_i.shape[0], : img_i.shape[1]] = img_j
    else:
        canvas[
            -peak[0] : -peak[0] + img_i.shape[0],
            -peak[1] : -peak[1] + img_i.shape[1],
        ] = img_i
        canvas[: img_i.shape[0], : img_i.shape[1]] = img_j
    axs[1, 2].imshow(canvas.astype(np.uint8))

    peak = starting_peak.copy()
    offsets = np.abs([stage_displacement[i] - peak[i] for i in range(len(stage_displacement))])
    axis = np.argmax(offsets)
    peak[axis] += img_i.shape[axis]

    canvas = np.zeros([int(abs(peak[0]) + img_i.shape[0]), int(abs(peak[1]) + img_i.shape[1]), 3])

    if peak[1] >= 0:
        if peak[0] >= 0:
            canvas[: img_i.shape[0], : img_i.shape[1]] = img_i
            canvas[peak[0] : peak[0] + img_i.shape[0], peak[1] : peak[1] + img_i.shape[1]] = img_j
        else:
            canvas[-peak[0] : -peak[0] + img_i.shape[0], : img_i.shape[1]] = img_i
            canvas[: img_i.shape[0], peak[1] : peak[1] + img_i.shape[1]] = img_j
    elif peak[0] >= 0:
        canvas[: img_i.shape[0], -peak[1] : -peak[1] + img_i.shape[1]] = img_i
        canvas[peak[0] : peak[0] + img_i.shape[0], : img_i.shape[1]] = img_j
    else:
        canvas[
            -peak[0] : -peak[0] + img_i.shape[0],
            -peak[1] : -peak[1] + img_i.shape[1],
        ] = img_i
        canvas[: img_i.shape[0], : img_i.shape[1]] = img_j
    axs[0, 2].imshow(canvas.astype(np.uint8))

    return fig
