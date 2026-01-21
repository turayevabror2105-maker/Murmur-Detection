from datetime import datetime
from typing import Optional
from sqlmodel import Field, SQLModel


class Run(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    filename: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    status: str = "uploaded"


class Result(SQLModel, table=True):
    run_id: int = Field(primary_key=True, foreign_key="run.id")
    predicted_label: str
    confidence: float
    triage_level: str
    urgency_score: float
    quality_pass: bool
    json_blob: str
