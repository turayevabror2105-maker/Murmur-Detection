from app.ml.quality import compute_quality_metrics, quality_gate
import numpy as np


def test_quality_gate_pass():
    audio = np.random.randn(12000).astype("float32") * 0.1
    metrics = compute_quality_metrics(audio, 2000)
    passed, _ = quality_gate(metrics)
    assert isinstance(passed, bool)
