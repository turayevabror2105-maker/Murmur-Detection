import numpy as np
import torch

from app.ml.features import compute_mel_spectrogram
from app.ml.model import build_demo_model


_MODEL = None


def get_model() -> torch.nn.Module:
    global _MODEL
    if _MODEL is None:
        _MODEL = build_demo_model()
    return _MODEL


def extract_features(mel_db: np.ndarray) -> torch.Tensor:
    mel_tensor = torch.tensor(mel_db, dtype=torch.float32)
    mean = mel_tensor.mean(dim=1)
    std = mel_tensor.std(dim=1)
    features = torch.cat([mean, std], dim=0)
    return features


def infer_murmur_and_timing(features: torch.Tensor, model: torch.nn.Module) -> tuple[float, float, float]:
    logits = model(features)
    murmur_logit = logits[0].item()
    timing_logit = logits[1].item()
    murmur_prob = torch.sigmoid(logits[0]).item()
    systolic_prob = torch.sigmoid(logits[1]).item()
    return murmur_prob, systolic_prob, murmur_logit


def sliding_window_segments(samples: np.ndarray, sample_rate: int) -> list[dict]:
    window_len_s = 2.0
    hop_s = 0.5
    window_len = int(window_len_s * sample_rate)
    hop_len = int(hop_s * sample_rate)
    segments = []
    model = get_model()
    model.eval()

    for start in range(0, max(len(samples) - window_len + 1, 1), hop_len):
        end = min(start + window_len, len(samples))
        window = samples[start:end]
        if len(window) < window_len:
            pad = np.zeros(window_len - len(window), dtype=window.dtype)
            window = np.concatenate([window, pad])
        mel = compute_mel_spectrogram(window, sample_rate)
        features = extract_features(mel)
        with torch.no_grad():
            murmur_prob, _, _ = infer_murmur_and_timing(features, model)
        segments.append({
            "t0": start / sample_rate,
            "t1": end / sample_rate,
            "murmur_prob": float(murmur_prob),
        })
    return segments


def run_model(samples: np.ndarray, sample_rate: int) -> dict:
    model = get_model()
    model.eval()
    mel = compute_mel_spectrogram(samples, sample_rate)
    features = extract_features(mel)
    with torch.no_grad():
        murmur_prob, systolic_prob, murmur_logit = infer_murmur_and_timing(features, model)
    diastolic_prob = 1.0 - systolic_prob
    return {
        "murmur_prob": murmur_prob,
        "systolic_prob": systolic_prob,
        "diastolic_prob": diastolic_prob,
        "murmur_logit": murmur_logit,
        "mel": mel,
        "features": features,
    }
