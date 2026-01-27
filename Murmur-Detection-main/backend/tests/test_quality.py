import numpy as np

from app.quality.metrics import compute_quality


def test_quality_metrics_bounds():
    samples = np.random.normal(0, 0.1, 4000).astype(np.float32)
    result = compute_quality(samples, 2000)
    assert 0 <= result.quality_score_0_100 <= 100
    assert 0 <= result.clipping_pct <= 100
    assert 0 <= result.silence_pct <= 100
