from __future__ import annotations

import io
import json
from pathlib import Path
from typing import Tuple

import numpy as np
from scipy.io import wavfile
import matplotlib.pyplot as plt

from app.config import RUNS_DIR


def validate_wav_header(content: bytes) -> None:
    if not content.startswith(b"RIFF") or b"WAVE" not in content[:16]:
        raise ValueError("Invalid WAV header; only PCM WAV is supported.")


def read_wav_bytes(content: bytes) -> Tuple[int, np.ndarray]:
    validate_wav_header(content)
    with io.BytesIO(content) as buf:
        sr, data = wavfile.read(buf)
    if data.dtype.kind in {"i", "u"}:
        max_val = np.iinfo(data.dtype).max
        audio = data.astype(np.float32) / max_val
    else:
        audio = data.astype(np.float32)
    if audio.ndim > 1:
        audio = np.mean(audio, axis=1)
    return sr, audio


def save_waveform_plot(run_id: int, audio: np.ndarray, sr: int, segments: list[dict]) -> Path:
    times = np.linspace(0, len(audio) / sr, len(audio))
    fig, ax = plt.subplots(figsize=(10, 3))
    ax.plot(times, audio, color="#2563eb", linewidth=1)
    for seg in segments:
        ax.axvspan(seg["start"], seg["end"], color="#f59e0b", alpha=0.3)
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Amplitude")
    ax.set_title("Waveform with highlighted segments")
    fig.tight_layout()
    run_dir = RUNS_DIR / str(run_id)
    run_dir.mkdir(parents=True, exist_ok=True)
    out_path = run_dir / "waveform.png"
    fig.savefig(out_path)
    plt.close(fig)
    return out_path


def save_json(run_id: int, payload: dict) -> Path:
    run_dir = RUNS_DIR / str(run_id)
    run_dir.mkdir(parents=True, exist_ok=True)
    path = run_dir / "results.json"
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return path
