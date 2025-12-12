import numpy as np

from opproplot import compute_operating_profile


def test_operating_profile_shapes():
    rng = np.random.default_rng(0)
    y_true = rng.integers(0, 2, size=1000)
    scores = rng.random(size=1000)

    profile = compute_operating_profile(y_true, scores, bins=20)

    assert profile.mids.shape == (20,)
    assert profile.pos_hist.shape == (20,)
    assert profile.neg_hist.shape == (20,)
    assert profile.tpr.shape == (20,)
    assert profile.fpr.shape == (20,)
    assert profile.accuracy.shape == (20,)
