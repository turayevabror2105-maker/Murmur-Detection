from __future__ import annotations

import json
import pickle
from pathlib import Path
from typing import Tuple

import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.calibration import CalibratedClassifierCV
from sklearn.metrics import accuracy_score, f1_score, confusion_matrix

from app.config import MODEL_PATH, CALIBRATOR_PATH, CONFIG_PATH
from app.ml.features import extract_features, extract_segment_features, segment_audio


def train_model(X: np.ndarray, y: np.ndarray) -> LogisticRegression:
    model = LogisticRegression(max_iter=1000)
    model.fit(X, y)
    return model


def calibrate_model(model: LogisticRegression, X_val: np.ndarray, y_val: np.ndarray) -> CalibratedClassifierCV:
    calibrator = CalibratedClassifierCV(model, method="isotonic", cv=3)
    calibrator.fit(X_val, y_val)
    return calibrator


def save_artifacts(model, calibrator, config: dict) -> None:
    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(MODEL_PATH, "wb") as f:
        pickle.dump(model, f)
    with open(CALIBRATOR_PATH, "wb") as f:
        pickle.dump(calibrator, f)
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2)


def load_artifacts() -> Tuple[LogisticRegression, CalibratedClassifierCV, dict]:
    with open(MODEL_PATH, "rb") as f:
        model = pickle.load(f)
    with open(CALIBRATOR_PATH, "rb") as f:
        calibrator = pickle.load(f)
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        config = json.load(f)
    return model, calibrator, config


def featurize_audio(audio: np.ndarray, sr: int) -> np.ndarray:
    return extract_features(audio, sr)[None, :]


def featurize_segments(audio: np.ndarray, sr: int):
    segments = segment_audio(audio, sr)
    features = extract_segment_features(segments, sr)
    return segments, features


def evaluate_model(model, X_test: np.ndarray, y_test: np.ndarray) -> dict:
    preds = model.predict(X_test)
    acc = accuracy_score(y_test, preds)
    f1 = f1_score(y_test, preds, average="macro")
    cm = confusion_matrix(y_test, preds).tolist()
    return {"accuracy": acc, "macro_f1": f1, "confusion_matrix": cm}
