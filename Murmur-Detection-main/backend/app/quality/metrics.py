from dataclasses import dataclass

import numpy as np


@dataclass
class QualityResult:
    quality_score_0_100: int
    snr_db: float
    clipping_pct: float
    silence_pct: float
    retake_recommended: bool
    retake_reasons: list[str]


def compute_quality(samples: np.ndarray, sample_rate: int) -> QualityResult:
    if len(samples) == 0:
        return QualityResult(0, 0.0, 100.0, 100.0, True, ["No audio detected."])

    abs_samples = np.abs(samples)
    clipping_pct = float(np.mean(abs_samples > 0.99))
    rms = float(np.sqrt(np.mean(samples ** 2)))

    frame_len = int(0.1 * sample_rate)
    if frame_len <= 0:
        frame_len = 1
    frames = samples[: len(samples) - (len(samples) % frame_len)]
    if len(frames) == 0:
        frames = samples
    frame_energies = np.sqrt(np.mean(frames.reshape(-1, frame_len) ** 2, axis=1))
    silence_thresh = max(0.02, 0.5 * np.median(frame_energies))
    silence_pct = float(np.mean(frame_energies < silence_thresh))

    noise_floor = np.percentile(frame_energies, 10)
    noise_floor = max(noise_floor, 1e-6)
    snr_db = 20 * np.log10((rms + 1e-6) / noise_floor)

    score = 100.0
    if rms < 0.03:
        score -= 15
    if silence_pct > 0.3:
        score -= min(30, 60 * silence_pct)
    if clipping_pct > 0.01:
        score -= min(30, 600 * clipping_pct)
    if snr_db < 10:
        score -= min(30, (10 - snr_db) * 3)

    score = int(max(0, min(100, round(score))))

    reasons = []
    if score < 60:
        reasons.append("Overall quality is low for a confident screen.")
    if silence_pct > 0.4:
        reasons.append("Long silent sections detected.")
    if clipping_pct > 0.05:
        reasons.append("Audio clipping detected; reduce input gain.")
    if snr_db < 8:
        reasons.append("Background noise is high relative to the signal.")

    retake_recommended = score < 60 or silence_pct > 0.5 or clipping_pct > 0.08

    return QualityResult(
        quality_score_0_100=score,
        snr_db=float(snr_db),
        clipping_pct=clipping_pct * 100.0,
        silence_pct=silence_pct * 100.0,
        retake_recommended=retake_recommended,
        retake_reasons=reasons,
    )
