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


def test_history_flow(client):
    wav_bytes = make_wav_bytes()
    files = {"file": ("test.wav", wav_bytes, "audio/wav")}
    data = {
        "auscultation_site": "Mitral",
        "patient_id": "patient-2",
    }
    response = client.post("/api/predict", files=files, data=data)
    assert response.status_code == 200
    request_id = response.json()["request_id"]

    history = client.get("/api/history").json()
    assert any(entry["request_id"] == request_id for entry in history)

    detail = client.get(f"/api/history/{request_id}")
    assert detail.status_code == 200
    assert detail.json()["request_id"] == request_id
