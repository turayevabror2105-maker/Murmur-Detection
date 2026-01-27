import io
import wave
from dataclasses import dataclass

import numpy as np

MIN_DURATION_S = 1.0


@dataclass
class AudioData:
    samples: np.ndarray
    sample_rate: int
    duration_s: float


def load_wav(file_bytes: bytes) -> AudioData:
    try:
        with wave.open(io.BytesIO(file_bytes), "rb") as wf:
            if wf.getnchannels() != 1:
                raise ValueError("Only mono WAV files are supported.")
            sample_rate = wf.getframerate()
            frames = wf.getnframes()
            if frames == 0 or sample_rate == 0:
                raise ValueError("WAV file contains no audio data.")
            raw = wf.readframes(frames)
            samples = np.frombuffer(raw, dtype=np.int16).astype(np.float32) / 32768.0
            duration_s = frames / float(sample_rate)
    except wave.Error as exc:
        raise ValueError("Invalid WAV file.") from exc

    if duration_s < MIN_DURATION_S:
        raise ValueError("Recording is too short for analysis.")

    return AudioData(samples=samples, sample_rate=sample_rate, duration_s=duration_s)


def is_wav_filename(filename: str) -> bool:
    return filename.lower().endswith(".wav")
