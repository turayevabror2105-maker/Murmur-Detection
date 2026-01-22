import base64
import io

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


def _fig_to_base64(fig: plt.Figure) -> str:
    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight", dpi=150)
    plt.close(fig)
    buf.seek(0)
    return base64.b64encode(buf.read()).decode("utf-8")


def plot_waveform(samples: np.ndarray, sample_rate: int) -> str:
    times = np.arange(len(samples)) / sample_rate
    fig, ax = plt.subplots(figsize=(6, 2))
    ax.plot(times, samples, color="#2563eb")
    ax.set_title("Waveform")
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Amplitude")
    ax.grid(True, alpha=0.3)
    return _fig_to_base64(fig)


def plot_spectrogram(mel_db: np.ndarray) -> str:
    fig, ax = plt.subplots(figsize=(6, 3))
    img = ax.imshow(mel_db, aspect="auto", origin="lower", cmap="magma")
    ax.set_title("Mel-Spectrogram")
    ax.set_xlabel("Frames")
    ax.set_ylabel("Mel bins")
    fig.colorbar(img, ax=ax, format="%+2.0f dB")
    return _fig_to_base64(fig)


def plot_timeline(segments: list[dict]) -> str:
    times = [(seg["t0"] + seg["t1"]) / 2 for seg in segments]
    probs = [seg["murmur_prob"] for seg in segments]
    fig, ax = plt.subplots(figsize=(6, 2))
    ax.plot(times, probs, marker="o", color="#ef4444")
    ax.set_ylim(0, 1)
    ax.set_title("Murmur Probability Timeline")
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Probability")
    ax.grid(True, alpha=0.3)
    return _fig_to_base64(fig)


def plot_explainability(mel_db: np.ndarray, heatmap: np.ndarray) -> str:
    fig, ax = plt.subplots(figsize=(6, 3))
    ax.imshow(mel_db, aspect="auto", origin="lower", cmap="magma")
    ax.imshow(heatmap, aspect="auto", origin="lower", cmap="cool", alpha=0.5)
    ax.set_title("Explainability Overlay")
    ax.set_xlabel("Frames")
    ax.set_ylabel("Mel bins")
    return _fig_to_base64(fig)
