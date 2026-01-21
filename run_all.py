from __future__ import annotations

from pathlib import Path
import json

import numpy as np

from app.ml.pipeline import train_model, calibrate_model, save_artifacts, evaluate_model
from app.ml.synthetic import build_synthetic_dataset
from app.ml.features import extract_features


def main():
    X, y = build_synthetic_dataset()
    sr = 2000
    X_feat = np.vstack([extract_features(sample, sr) for sample in X])
    split = int(0.8 * len(X_feat))
    X_train, X_val = X_feat[:split], X_feat[split:]
    y_train, y_val = y[:split], y[split:]

    model = train_model(X_train, y_train)
    calibrator = calibrate_model(model, X_val, y_val)
    save_artifacts(model, calibrator, {"sr": sr, "feature_type": "log-mel"})

    metrics = evaluate_model(model, X_val, y_val)
    Path("artifacts").mkdir(exist_ok=True)
    Path("artifacts/metrics.json").write_text(json.dumps(metrics, indent=2), encoding="utf-8")
    print("Training + evaluation done. Metrics:")
    print(json.dumps(metrics, indent=2))


if __name__ == "__main__":
    main()
