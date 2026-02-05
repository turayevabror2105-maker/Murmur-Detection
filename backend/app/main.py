from datetime import datetime, timezone
import json
import uuid

from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.calibration.temperature import CALIBRATION_EXPLANATION, TemperatureScaler
from app.db.crud import create_analysis, delete_analysis, get_analysis, list_history
from app.db.init_db import init_db
from app.db.models import Analysis
from app.db.session import get_session_maker
from app.explainability.saliency import saliency_heatmap
from app.ml.pipeline import run_model, sliding_window_segments
from app.quality.metrics import compute_quality
from app.uncertainty.estimate import mc_dropout_uncertainty
from app.utils.audio import is_wav_filename, load_wav
from app.utils.plots import plot_explainability, plot_spectrogram, plot_timeline, plot_waveform
from app.utils.risk import assess_risk


class InputInfo(BaseModel):
    filename: str
    patient_id: str
    visit_label: str | None
    auscultation_site: str
    duration_s: float
    sample_rate: int


class MurmurResult(BaseModel):
    label: str
    raw_probability: float
    calibrated_probability: float
    uncertainty_score: float


class TimingResult(BaseModel):
    label: str
    systolic_probability: float
    diastolic_probability: float


class QualityResult(BaseModel):
    quality_score_0_100: int
    snr_db: float
    clipping_pct: float
    silence_pct: float
    retake_recommended: bool
    retake_reasons: list[str]


class RiskResult(BaseModel):
    screening_concern_level: str
    rationale: str


class SegmentResult(BaseModel):
    t0: float
    t1: float
    murmur_prob: float


class ArtifactsResult(BaseModel):
    waveform_png_base64: str
    spectrogram_png_base64: str
    timeline_png_base64: str
    explainability_png_base64: str


class PredictResponse(BaseModel):
    request_id: str
    created_at: str
    input: InputInfo
    murmur: MurmurResult
    timing: TimingResult
    quality: QualityResult
    risk: RiskResult
    safe_advice: list[str]
    segments: list[SegmentResult]
    artifacts: ArtifactsResult


SAFE_ADVICE = [
    "Keep the stethoscope steady and avoid rubbing the microphone.",
    "Record in a quiet room and minimize background noise.",
    "If the recording quality is low, try a second recording.",
    "For any health concerns, consult a qualified clinician.",
]


AUSCULTATION_SITES = {"Aortic", "Pulmonic", "Tricuspid", "Mitral", "Unknown"}


def create_app(db_url: str | None = None) -> FastAPI:
    app = FastAPI(title="Murmur Screening Demo", version="1.0")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["https://murmur-detection-frontend.onrender.com"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    SessionLocal = get_session_maker(db_url)
    init_db(db_url)

    def get_db() -> Session:
        return SessionLocal()

    @app.get("/api/health")
    def health():
        return {"ok": "True"}

    @app.post("/api/predict", response_model=PredictResponse)
    async def predict(
        file: UploadFile = File(...),
        auscultation_site: str = Form(...),
        patient_id: str = Form(...),
        visit_label: str | None = Form(None),
    ):
        if not is_wav_filename(file.filename):
            raise HTTPException(status_code=400, detail="Only WAV files are supported.")
        if auscultation_site not in AUSCULTATION_SITES:
            raise HTTPException(status_code=400, detail="Invalid auscultation site.")

        file_bytes = await file.read()
        try:
            audio = load_wav(file_bytes)
        except ValueError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc

        model_result = run_model(audio.samples, audio.sample_rate)
        segments = sliding_window_segments(audio.samples, audio.sample_rate)

        quality = compute_quality(audio.samples, audio.sample_rate)

        temperature = TemperatureScaler()
        raw_prob = model_result["murmur_prob"]
        logit = float(model_result["murmur_logit"])
        calibrated_prob = temperature.calibrate_probability(logit)

        from app.ml.pipeline import get_model

        model = get_model()
        _, uncertainty_score = mc_dropout_uncertainty(model, model_result["features"], passes=20)

        murmur_label = "murmur" if calibrated_prob >= 0.5 else "normal"
        systolic_prob = model_result["systolic_prob"]
        diastolic_prob = model_result["diastolic_prob"]
        if max(systolic_prob, diastolic_prob) < 0.55:
            timing_label = "uncertain"
        else:
            timing_label = "systolic" if systolic_prob >= diastolic_prob else "diastolic"

        risk = assess_risk(calibrated_prob, uncertainty_score, quality.quality_score_0_100)

        mel = model_result["mel"]
        heatmap = saliency_heatmap(get_model(), mel)

        response_payload = {
            "request_id": str(uuid.uuid4()),
            "created_at": datetime.now(timezone.utc).isoformat(),
            "input": {
                "filename": file.filename,
                "patient_id": patient_id,
                "visit_label": visit_label,
                "auscultation_site": auscultation_site,
                "duration_s": audio.duration_s,
                "sample_rate": audio.sample_rate,
            },
            "murmur": {
                "label": murmur_label,
                "raw_probability": float(raw_prob),
                "calibrated_probability": float(calibrated_prob),
                "uncertainty_score": float(uncertainty_score),
            },
            "timing": {
                "label": timing_label,
                "systolic_probability": float(systolic_prob),
                "diastolic_probability": float(diastolic_prob),
            },
            "quality": {
                "quality_score_0_100": quality.quality_score_0_100,
                "snr_db": quality.snr_db,
                "clipping_pct": quality.clipping_pct,
                "silence_pct": quality.silence_pct,
                "retake_recommended": quality.retake_recommended,
                "retake_reasons": quality.retake_reasons,
            },
            "risk": {
                "screening_concern_level": risk.screening_concern_level,
                "rationale": f"{risk.rationale} Explainability note: model focused on mid-frequency bands during high-probability segments.",
            },
            "safe_advice": SAFE_ADVICE + [CALIBRATION_EXPLANATION],
            "segments": segments,
            "artifacts": {
                "waveform_png_base64": plot_waveform(audio.samples, audio.sample_rate),
                "spectrogram_png_base64": plot_spectrogram(mel),
                "timeline_png_base64": plot_timeline(segments),
                "explainability_png_base64": plot_explainability(mel, heatmap),
            },
        }

        summary = {
            "murmur_label": murmur_label,
            "concern_level": risk.screening_concern_level,
            "quality_score": quality.quality_score_0_100,
        }

        db = get_db()
        try:
            create_analysis(
                db,
                Analysis(
                    request_id=response_payload["request_id"],
                    created_at=datetime.fromisoformat(response_payload["created_at"]),
                    patient_id=patient_id,
                    visit_label=visit_label,
                    auscultation_site=auscultation_site,
                    summary=json.dumps(summary),
                    response_json=response_payload,
                ),
            )
        finally:
            db.close()

        return response_payload
from fastapi import HTTPException
import json

@app.get("/api/history")
def history(patient_id: str | None = None):
    db = get_db()
    try:
        entries = list_history(db, patient_id) or []
        return [
            {
                "request_id": entry.request_id,
                "created_at": entry.created_at.isoformat(),
                "patient_id": entry.patient_id,
                "visit_label": entry.visit_label,
                "auscultation_site": entry.auscultation_site,
                "summary": json.loads(entry.summary),
            }
            for entry in entries
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()

    @app.get("/api/history/{request_id}")
    def history_detail(request_id: str):
        db = get_db()
        try:
            entry = get_analysis(db, request_id)
            if not entry:
                raise HTTPException(status_code=404, detail="Entry not found.")
            return entry.response_json
        finally:
            db.close()

    @app.delete("/api/history/{request_id}")
    def delete_history(request_id: str):
        db = get_db()
        try:
            deleted = delete_analysis(db, request_id)
            if not deleted:
                raise HTTPException(status_code=404, detail="Entry not found.")
            return {"deleted": True}
        finally:
            db.close()

    return app


app = create_app()
