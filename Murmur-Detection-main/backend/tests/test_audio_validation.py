import io
import wave

import numpy as np
import pytest

from app.utils.audio import load_wav


def make_wav_bytes(duration_s: float, sr: int = 2000) -> bytes:
    t = np.linspace(0, duration_s, int(sr * duration_s), endpoint=False)
    samples = (0.3 * np.sin(2 * np.pi * 100 * t) * 32767).astype(np.int16)
    buf = io.BytesIO()
    with wave.open(buf, "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sr)
        wf.writeframes(samples.tobytes())
    return buf.getvalue()


def test_load_wav_valid():
    data = make_wav_bytes(2.0)
    audio = load_wav(data)
    assert audio.duration_s >= 2.0
    assert audio.sample_rate == 2000


def test_load_wav_too_short():
    data = make_wav_bytes(0.5)
    with pytest.raises(ValueError):
        load_wav(data)


def test_load_wav_invalid():
    with pytest.raises(ValueError):
        load_wav(b"not a wav file")
