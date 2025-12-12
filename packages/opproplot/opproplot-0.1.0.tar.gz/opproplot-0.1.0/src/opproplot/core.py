from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Tuple

import numpy as np


@dataclass
class OperatingProfile:
    """
    Operating profile data for a binary classifier.

    Attributes
    ----------
    edges : np.ndarray
        Bin edges along the score axis, shape (bins + 1,).
    mids : np.ndarray
        Bin midpoints (used as thresholds), shape (bins,).
    pos_hist : np.ndarray
        Counts of positive examples per bin, shape (bins,).
    neg_hist : np.ndarray
        Counts of negative examples per bin, shape (bins,).
    tpr : np.ndarray
        True positive rate (recall) at each bin midpoint threshold, shape (bins,).
    fpr : np.ndarray
        False positive rate at each bin midpoint threshold, shape (bins,).
    accuracy : np.ndarray
        Accuracy at each bin midpoint threshold, shape (bins,).
    """

    edges: np.ndarray
    mids: np.ndarray
    pos_hist: np.ndarray
    neg_hist: np.ndarray
    tpr: np.ndarray
    fpr: np.ndarray
    accuracy: np.ndarray


def compute_operating_profile(
    y_true: np.ndarray,
    y_score: np.ndarray,
    bins: int = 40,
    score_range: Optional[Tuple[float, float]] = (0.0, 1.0),
) -> OperatingProfile:
    """
    Compute an operating profile for a binary classifier.

    Parameters
    ----------
    y_true : array-like of shape (n_samples,)
        Ground-truth binary labels (0/1 or False/True).
    y_score : array-like of shape (n_samples,)
        Predicted scores or probabilities (higher = more likely positive).
    bins : int, default=40
        Number of bins to use along the score axis.
    score_range : tuple(float, float) or None, default=(0.0, 1.0)
        Range for the score histogram. If None, uses (min(y_score), max(y_score)).

    Returns
    -------
    OperatingProfile
        Dataclass containing histogram info and TPR/FPR/accuracy vs threshold.

    Notes
    -----
    This implementation is vectorized:

    * The histogram layer uses np.histogram by class.
    * The threshold-dependent metrics are computed by:
      - sorting scores once in descending order,
      - computing cumulative TP/FP,
      - mapping each bin midpoint to a position in that sorted array.

    This makes it O(n log n + bins) rather than O(n * bins).
    """
    y_true = np.asarray(y_true).astype(int)
    y_score = np.asarray(y_score).astype(float)

    if y_true.shape != y_score.shape:
        raise ValueError("y_true and y_score must have the same shape.")

    if score_range is None:
        score_range = (float(np.min(y_score)), float(np.max(y_score)))

    # Histogram by class (for the stacked bars)
    pos_scores = y_score[y_true == 1]
    neg_scores = y_score[y_true == 0]

    pos_hist, edges = np.histogram(pos_scores, bins=bins, range=score_range)
    neg_hist, _ = np.histogram(neg_scores, bins=edges)

    mids = 0.5 * (edges[:-1] + edges[1:])

    # Sort once by score (descending)
    order = np.argsort(-y_score)
    y_score_sorted = y_score[order]
    y_true_sorted = y_true[order]

    pos = (y_true_sorted == 1).astype(int)
    neg = 1 - pos

    TP_cum = np.cumsum(pos)
    FP_cum = np.cumsum(neg)

    P = int(pos.sum())
    N = int(neg.sum())

    if P == 0 or N == 0:
        raise ValueError("Both positive and negative examples are required.")

    TN_cum = N - FP_cum

    # Map bin midpoints to indices (thresholds);
    # we want y_score_sorted >= t, so search on -y_score_sorted.
    thresholds = mids
    search_space = -y_score_sorted
    idx = np.searchsorted(search_space, -thresholds, side="left")
    idx = np.clip(idx, 0, len(y_score_sorted) - 1)

    TP = TP_cum[idx]
    FP = FP_cum[idx]
    TN = TN_cum[idx]

    eps = 1e-12
    tpr = TP / (P + eps)           # recall
    fpr = FP / (N + eps)
    accuracy = (TP + TN) / (P + N + eps)

    return OperatingProfile(
        edges=edges,
        mids=mids,
        pos_hist=pos_hist,
        neg_hist=neg_hist,
        tpr=tpr,
        fpr=fpr,
        accuracy=accuracy,
    )
