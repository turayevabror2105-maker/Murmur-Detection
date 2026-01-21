from __future__ import annotations

import numpy as np


def compute_quality_metrics(audio: np.ndarray, sr: int) -> dict:
    duration = float(audio.shape[0] / sr)
    max_amp = float(np.max(np.abs(audio))) if audio.size else 0.0
    clipping_rate = float(np.mean(np.abs(audio) >= 0.98)) if audio.size else 0.0
    silence_ratio = float(np.mean(np.abs(audio) < 0.01)) if audio.size else 1.0
    rms = float(np.sqrt(np.mean(audio ** 2))) if audio.size else 0.0
    snr_proxy = float((rms + 1e-6) / (np.std(audio) + 1e-6)) if audio.size else 0.0
    amplitude_range = float(max_amp)
    return {
        "duration": duration,
        "clipping_rate": clipping_rate,
        "silence_ratio": silence_ratio,
        "snr_proxy": snr_proxy,
        "amplitude_range": amplitude_range,
    }


def quality_gate(metrics: dict) -> tuple[bool, list[str]]:
    reasons = []
    if metrics["duration"] < 5.0:
        reasons.append("Recording too short (<5s).")
    if metrics["clipping_rate"] > 0.01:
        reasons.append("Clipping detected; reduce input gain.")
    if metrics["silence_ratio"] > 0.6:
        reasons.append("Excessive silence; ensure proper stethoscope placement.")
    if metrics["snr_proxy"] < 0.8:
        reasons.append("Low signal-to-noise; re-record in a quieter room.")
    if metrics["amplitude_range"] < 0.1:
        reasons.append("Low amplitude; check microphone contact.")
    passed = len(reasons) == 0
    return passed, reasons
