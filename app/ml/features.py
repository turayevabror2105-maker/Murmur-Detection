from __future__ import annotations

import numpy as np
import librosa


def segment_audio(audio: np.ndarray, sr: int, window_sec: float = 2.0, hop_sec: float = 1.0) -> list[np.ndarray]:
    window = int(window_sec * sr)
    hop = int(hop_sec * sr)
    segments = []
    for start in range(0, max(len(audio) - window + 1, 1), hop):
        segment = audio[start : start + window]
        if segment.shape[0] < window:
            pad = np.zeros(window - segment.shape[0], dtype=audio.dtype)
            segment = np.concatenate([segment, pad])
        segments.append(segment)
    return segments


def extract_features(audio: np.ndarray, sr: int) -> np.ndarray:
    mel = librosa.feature.melspectrogram(y=audio, sr=sr, n_mels=40, fmin=20, fmax=800)
    log_mel = librosa.power_to_db(mel + 1e-6)
    mean = np.mean(log_mel, axis=1)
    std = np.std(log_mel, axis=1)
    return np.concatenate([mean, std])


def extract_segment_features(segments: list[np.ndarray], sr: int) -> np.ndarray:
    return np.vstack([extract_features(seg, sr) for seg in segments])
