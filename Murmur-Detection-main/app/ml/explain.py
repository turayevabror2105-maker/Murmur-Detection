from __future__ import annotations

import numpy as np


def top_feature_names(model, feature_count: int = 5) -> list[str]:
    if hasattr(model, "coef_"):
        coef = model.coef_[0]
        idx = np.argsort(np.abs(coef))[::-1][:feature_count]
        return [f"feature_{i}" for i in idx]
    if hasattr(model, "feature_importances_"):
        idx = np.argsort(model.feature_importances_)[::-1][:feature_count]
        return [f"feature_{i}" for i in idx]
    return []


def segment_scores(model, features: np.ndarray) -> np.ndarray:
    if hasattr(model, "predict_proba"):
        return model.predict_proba(features)[:, 1]
    scores = model.decision_function(features)
    scores = (scores - scores.min()) / (scores.max() - scores.min() + 1e-6)
    return scores
