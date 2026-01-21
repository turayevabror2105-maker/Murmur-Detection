from typing import List, Optional
from pydantic import BaseModel


class ErrorResponse(BaseModel):
    error_code: str
    message: str
    hint: Optional[str] = None


class UploadResponse(BaseModel):
    run_id: int
    filename: str
    duration: float
    sample_rate: int


class QualityMetrics(BaseModel):
    duration: float
    clipping_rate: float
    silence_ratio: float
    snr_proxy: float
    amplitude_range: float


class QualityResult(BaseModel):
    pass_: bool
    metrics: QualityMetrics
    reasons: List[str]


class ExplanationResult(BaseModel):
    top_features: List[str]
    top_segments: List[dict]


class TriageResult(BaseModel):
    level: str
    rule_fired: str


class RiskResult(BaseModel):
    urgency_score: float
    category: str
    breakdown: List[str]


class RunPaths(BaseModel):
    report_url: str
    waveform_png_url: str


class RunResults(BaseModel):
    predicted_label: str
    calibrated_confidence: float
    raw_confidence: float
    quality: QualityResult
    explanation: ExplanationResult
    triage: TriageResult
    risk: RiskResult
    paths: RunPaths


class RunResponse(BaseModel):
    run_id: int
    status: str
    results: RunResults


class HistoryItem(BaseModel):
    run_id: int
    filename: str
    timestamp: str
    label: str
    triage: str
    quality_pass: bool


class TrainResponse(BaseModel):
    status: str
    message: str
