from __future__ import annotations

import numpy as np


def generate_synthetic_pcg(sr: int, duration: float, murmur: bool) -> np.ndarray:
    t = np.linspace(0, duration, int(sr * duration), endpoint=False)
    heart_rate = 1.2
    base = 0.2 * np.sin(2 * np.pi * heart_rate * t) + 0.05 * np.sin(2 * np.pi * 2 * heart_rate * t)
    noise = 0.02 * np.random.randn(t.size)
    signal = base + noise
    if murmur:
        murmur_noise = 0.08 * np.sin(2 * np.pi * 180 * t) * (np.sin(2 * np.pi * heart_rate * t) > 0)
        signal += murmur_noise
    return signal.astype(np.float32)


def build_synthetic_dataset(n_samples: int = 40, sr: int = 2000, duration: float = 6.0):
    X = []
    y = []
    for i in range(n_samples):
        murmur = i % 2 == 0
        audio = generate_synthetic_pcg(sr, duration, murmur)
        X.append(audio)
        y.append(1 if murmur else 0)
    return np.array(X, dtype=object), np.array(y)
