from sqlalchemy import Column, DateTime, String, Text
from sqlalchemy.dialects.sqlite import JSON
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Analysis(Base):
    __tablename__ = "analyses"

    request_id = Column(String, primary_key=True, index=True)
    created_at = Column(DateTime, nullable=False)
    patient_id = Column(String, nullable=False, index=True)
    visit_label = Column(String, nullable=True)
    auscultation_site = Column(String, nullable=False)
    summary = Column(Text, nullable=False)
    response_json = Column(JSON, nullable=False)
