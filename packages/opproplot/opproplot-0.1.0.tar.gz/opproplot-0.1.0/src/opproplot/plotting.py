from __future__ import annotations

from typing import Optional

import matplotlib.pyplot as plt

from .core import compute_operating_profile


def operating_profile_plot(
    y_true,
    y_score,
    bins: int = 40,
    score_range=None,
    show_accuracy: bool = True,
    show_key: bool = True,
    key_location: str = "inside",
    show_grid: bool = False,
    grid_kwargs: Optional[dict] = None,
    title: Optional[str] = None,
    ax: Optional[plt.Axes] = None,
):
    """
    Plot an operating profile: stacked score histogram + TPR/FPR(/accuracy).

    Parameters
    ----------
    y_true : array-like of shape (n_samples,)
        Ground-truth binary labels.
    y_score : array-like of shape (n_samples,)
        Predicted scores or probabilities.
    bins : int, default=40
        Number of bins for the score histogram.
    score_range : tuple(float, float) or None, default=None
        Range for the score histogram. If None, inferred from scores.
    show_accuracy : bool, default=True
        Whether to plot accuracy as an additional dashed curve.
    show_key : bool, default=True
        Whether to display a combined key/legend for bars and metric lines.
    key_location : {"inside", "outside"}, default="inside"
        Placement of the key. "inside" uses a standard axis legend; "outside"
        docks the key to the right via fig.legend.
    show_grid : bool, default=False
        Whether to draw a background grid aligned to the metric axis.
    grid_kwargs : dict or None, default=None
        Passed to `ax_metric.grid`; useful keys include `alpha`, `color`,
        `linestyle`, and `linewidth`.
    title : str or None, default=None
        Title for the histogram axis. If None, uses "Opproplot: Operating Profile".
    ax : matplotlib.axes.Axes or None, default=None
        Axis to plot on. If None, a new figure and axis are created.

    Returns
    -------
    fig : matplotlib.figure.Figure
    ax_hist : matplotlib.axes.Axes
        Axis with the histogram (left y-axis).
    ax_metric : matplotlib.axes.Axes
        Axis with the metric curves (right y-axis).
    """
    profile = compute_operating_profile(
        y_true=y_true, y_score=y_score, bins=bins, score_range=score_range
    )

    if ax is None:
        fig, ax_hist = plt.subplots(figsize=(8, 4))
    else:
        fig = ax.get_figure()
        ax_hist = ax

    widths = profile.edges[1:] - profile.edges[:-1]
    ax_hist.bar(
        profile.mids,
        profile.neg_hist,
        width=widths,
        align="center",
        label="Negatives",
    )
    ax_hist.bar(
        profile.mids,
        profile.pos_hist,
        width=widths,
        align="center",
        bottom=profile.neg_hist,
        label="Positives",
        alpha=0.7,
    )

    ax_hist.set_xlabel("Score bins (threshold midpoints)")
    ax_hist.set_ylabel("Count per bin")

    ax_metric = ax_hist.twinx()
    ax_metric.plot(profile.mids, profile.tpr, label="TPR (Recall)")
    ax_metric.plot(profile.mids, profile.fpr, label="FPR")

    if show_accuracy:
        ax_metric.plot(profile.mids, profile.accuracy, label="Accuracy", linestyle="--")

    ax_metric.set_ylabel("Metric value")

    if show_key:
        color_handles = [
            ax_hist.containers[0].patches[0],
            ax_hist.containers[1].patches[0],
        ]
        color_labels = ["Negatives", "Positives"]

        line_handles = ax_metric.lines[: 3 if show_accuracy else 2]
        line_labels = ["TPR (Recall)", "FPR"] + (["Accuracy"] if show_accuracy else [])

        handles = color_handles + line_handles
        labels = color_labels + line_labels

        if key_location == "outside":
            fig.legend(
                handles,
                labels,
                loc="center left",
                bbox_to_anchor=(1.02, 0.5),
                frameon=False,
            )
        else:
            ax_metric.legend(handles, labels, loc="lower right")

    if show_grid:
        ax_metric.grid(True, **(grid_kwargs or {"alpha": 0.2, "linestyle": "--"}))

    if title is None:
        title = "Opproplot: Operating Profile"
    ax_hist.set_title(title)

    fig.tight_layout()
    return fig, ax_hist, ax_metric
