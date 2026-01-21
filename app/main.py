from __future__ import annotations

import json
from pathlib import Path
from typing import List

import numpy as np
from fastapi import FastAPI, File, UploadFile, Depends, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from app.config import MAX_UPLOAD_MB, UPLOAD_DIR, RUNS_DIR
from app.db import init_db, get_session
from app.models import Run, Result
from app.schemas import UploadResponse
from app.utils import read_wav_bytes, save_waveform_plot, save_json
from app.ml.features import segment_audio, extract_segment_features
from app.ml.pipeline import (
    train_model,
    calibrate_model,
    save_artifacts,
    load_artifacts,
    featurize_audio,
    evaluate_model,
)
from app.ml.quality import compute_quality_metrics, quality_gate
from app.ml.explain import top_feature_names, segment_scores
from app.ml.risk import triage_rules, murmur_timing_proxy, urgency_score
from app.ml.report import save_report, render_pdf
from app.ml.synthetic import build_synthetic_dataset, generate_synthetic_pcg
from sqlmodel import Session, select

app = FastAPI(title="Murmur Screen API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"] ,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"] ,
)


@app.on_event("startup")
def on_startup():
    init_db()
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    RUNS_DIR.mkdir(parents=True, exist_ok=True)


def error_response(code: str, message: str, hint: str | None = None):
    return JSONResponse(status_code=400, content={"error_code": code, "message": message, "hint": hint})


def ensure_demo_file(path: Path) -> None:
    if path.exists():
        return
    audio = generate_synthetic_pcg(sr=2000, duration=6.0, murmur=True)
    from scipy.io.wavfile import write

    path.parent.mkdir(parents=True, exist_ok=True)
    write(path, 2000, (audio * 32767).astype(np.int16))


@app.post("/api/upload", response_model=UploadResponse)
async def upload_audio(file: UploadFile = File(...), session: Session = Depends(get_session)):
    if not file.filename.endswith(".wav"):
        return error_response("invalid_file", "Only .wav files are supported.", "Please upload a PCM WAV file.")
    content = await file.read()
    if len(content) > MAX_UPLOAD_MB * 1024 * 1024:
        return error_response("file_too_large", "File exceeds 20MB limit.", "Compress or trim the file before upload.")
    try:
        sr, audio = read_wav_bytes(content)
    except Exception as exc:
        return error_response("invalid_wav", str(exc), "Ensure the file is PCM WAV format.")

    run = Run(filename=file.filename, status="uploaded")
    session.add(run)
    session.commit()
    session.refresh(run)

    upload_path = UPLOAD_DIR / f"run_{run.id}.wav"
    upload_path.write_bytes(content)

    duration = float(audio.shape[0] / sr)
    return UploadResponse(run_id=run.id, filename=file.filename, duration=duration, sample_rate=sr)


@app.post("/api/run/{run_id}")
async def run_analysis(run_id: int, payload: dict, session: Session = Depends(get_session)):
    mode = payload.get("mode")
    if mode not in {"real", "demo"}:
        return error_response("invalid_mode", "mode must be 'real' or 'demo'", "Send {'mode':'demo'} for demo run.")

    run = session.exec(select(Run).where(Run.id == run_id)).first()
    if not run:
        return error_response("not_found", "Run ID not found.", "Upload a file first.")

    if mode == "demo":
        demo_path = UPLOAD_DIR / f"demo_{run_id}.wav"
        ensure_demo_file(demo_path)
        content = demo_path.read_bytes()
    else:
        upload_path = UPLOAD_DIR / f"run_{run_id}.wav"
        if not upload_path.exists():
            return error_response("missing_upload", "Uploaded file not found.", "Re-upload the file.")
        content = upload_path.read_bytes()

    sr, audio = read_wav_bytes(content)

    try:
        model, calibrator, config = load_artifacts()
    except Exception:
        model, calibrator, config = train_baseline()

    features = featurize_audio(audio, sr)
    raw_confidence = float(model.predict_proba(features)[0, 1])
    calibrated_confidence = float(calibrator.predict_proba(features)[0, 1])
    predicted_label = "Murmur" if calibrated_confidence >= 0.5 else "No Murmur"

    metrics = compute_quality_metrics(audio, sr)
    quality_pass, reasons = quality_gate(metrics)

    segments = segment_audio(audio, sr)
    segment_features = extract_segment_features(segments, sr)
    segment_probs = segment_scores(model, segment_features)
    top_indices = np.argsort(segment_probs)[::-1][:3]
    top_segments = []
    for idx in top_indices:
        start = idx * 1.0
        end = start + 2.0
        top_segments.append({"start": float(start), "end": float(end), "score": float(segment_probs[idx])})

    explanation = {
        "top_features": top_feature_names(model, 8),
        "top_segments": top_segments,
    }

    triage_level, rule_fired = triage_rules(calibrated_confidence, quality_pass)
    timing = murmur_timing_proxy(top_segments)
    urgency, category, breakdown = urgency_score(calibrated_confidence, triage_level, timing, quality_pass)

    waveform_path = save_waveform_plot(run_id, audio, sr, top_segments)
    payload = {
        "run_id": run_id,
        "status": "done",
        "results": {
            "predicted_label": predicted_label,
            "calibrated_confidence": calibrated_confidence,
            "raw_confidence": raw_confidence,
            "quality": {
                "pass": quality_pass,
                "metrics": metrics,
                "reasons": reasons,
            },
            "explanation": explanation,
            "triage": {"level": triage_level, "rule_fired": rule_fired},
            "risk": {"urgency_score": urgency, "category": category, "breakdown": breakdown},
            "paths": {
                "report_url": f"/api/report/{run_id}",
                "waveform_png_url": f"/api/run/{run_id}/waveform",
            },
        },
    }

    save_json(run_id, payload)
    report_path = save_report(run_id, payload)
    render_pdf(report_path)

    result = Result(
        run_id=run_id,
        predicted_label=predicted_label,
        confidence=calibrated_confidence,
        triage_level=triage_level,
        urgency_score=urgency,
        quality_pass=quality_pass,
        json_blob=json.dumps(payload),
    )
    session.merge(result)
    run.status = "done"
    session.add(run)
    session.commit()

    return payload


@app.get("/api/run/{run_id}")
async def get_run(run_id: int):
    json_path = RUNS_DIR / str(run_id) / "results.json"
    if not json_path.exists():
        return error_response("not_found", "Run results not found.", "Run analysis first.")
    return json.loads(json_path.read_text(encoding="utf-8"))


@app.get("/api/run/{run_id}/waveform")
async def get_waveform(run_id: int):
    path = RUNS_DIR / str(run_id) / "waveform.png"
    if not path.exists():
        return error_response("not_found", "Waveform image not found.", "Run analysis first.")
    return FileResponse(path)


@app.get("/api/history")
async def get_history(session: Session = Depends(get_session)):
    runs = session.exec(select(Run).order_by(Run.created_at.desc())).all()
    results = session.exec(select(Result)).all()
    result_map = {res.run_id: res for res in results}
    items = []
    for run in runs:
        res = result_map.get(run.id)
        items.append(
            {
                "run_id": run.id,
                "filename": run.filename,
                "timestamp": run.created_at.isoformat(),
                "label": res.predicted_label if res else "",
                "triage": res.triage_level if res else "",
                "quality_pass": res.quality_pass if res else False,
            }
        )
    return items


@app.post("/api/train")
async def train_endpoint():
    train_baseline()
    return {"status": "ok", "message": "Training complete"}


@app.post("/api/evaluate")
async def evaluate_endpoint():
    model, calibrator, config = load_artifacts()
    X, y = build_synthetic_dataset()
    X_feat = np.vstack([featurize_audio(sample, 2000) for sample in X])
    metrics = evaluate_model(model, X_feat, y)
    return {"status": "ok", "metrics": metrics}


@app.get("/api/plots/calibration")
async def calibration_plot():
    path = RUNS_DIR / "calibration.png"
    if not path.exists():
        return error_response("not_found", "Calibration plot not found.", "Run training/evaluation first.")
    return FileResponse(path)


@app.get("/api/report/{run_id}")
async def report(run_id: int):
    report_path = RUNS_DIR / str(run_id) / "report.html"
    if not report_path.exists():
        return error_response("not_found", "Report not found.", "Run analysis first.")
    return FileResponse(report_path, media_type="text/html")


@app.get("/api/report/{run_id}/pdf")
async def report_pdf(run_id: int):
    pdf_path = RUNS_DIR / str(run_id) / "report.pdf"
    if not pdf_path.exists():
        return error_response("not_found", "PDF not found.", "Generate report first.")
    return FileResponse(pdf_path, media_type="application/pdf")


def train_baseline():
    X, y = build_synthetic_dataset()
    sr = 2000
    X_feat = np.vstack([featurize_audio(sample, sr) for sample in X])
    split = int(0.8 * len(X_feat))
    X_train, X_val = X_feat[:split], X_feat[split:]
    y_train, y_val = y[:split], y[split:]
    model = train_model(X_train, y_train)
    calibrator = calibrate_model(model, X_val, y_val)

    config = {"feature_type": "log-mel", "sr": sr, "window_sec": 2.0, "hop_sec": 1.0}
    save_artifacts(model, calibrator, config)

    # Create calibration plot
    from sklearn.calibration import calibration_curve
    import matplotlib.pyplot as plt

    probs = calibrator.predict_proba(X_val)[:, 1]
    frac, mean = calibration_curve(y_val, probs, n_bins=5)
    fig, ax = plt.subplots()
    ax.plot(mean, frac, marker="o")
    ax.plot([0, 1], [0, 1], linestyle="--", color="gray")
    ax.set_xlabel("Mean predicted")
    ax.set_ylabel("Fraction positive")
    ax.set_title("Calibration curve")
    RUNS_DIR.mkdir(parents=True, exist_ok=True)
    fig.savefig(RUNS_DIR / "calibration.png")
    plt.close(fig)

    return model, calibrator, config
