import io
import wave

import numpy as np


def make_wav_bytes(duration_s: float = 2.0, sr: int = 2000) -> bytes:
    t = np.linspace(0, duration_s, int(sr * duration_s), endpoint=False)
    samples = (0.2 * np.sin(2 * np.pi * 120 * t) * 32767).astype(np.int16)
    buf = io.BytesIO()
    with wave.open(buf, "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sr)
        wf.writeframes(samples.tobytes())
    return buf.getvalue()


def test_predict_schema(client):
    wav_bytes = make_wav_bytes()
    files = {"file": ("test.wav", wav_bytes, "audio/wav")}
    data = {
        "auscultation_site": "Aortic",
        "patient_id": "patient-1",
        "visit_label": "baseline",
    }
    response = client.post("/api/predict", files=files, data=data)
    assert response.status_code == 200
    payload = response.json()
    assert "request_id" in payload
    assert payload["input"]["patient_id"] == "patient-1"
    assert "murmur" in payload
    assert "quality" in payload
    assert "artifacts" in payload
