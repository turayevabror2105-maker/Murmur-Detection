from sqlalchemy.orm import Session

from app.db.models import Analysis


def create_analysis(db: Session, analysis: Analysis) -> Analysis:
    db.add(analysis)
    db.commit()
    db.refresh(analysis)
    return analysis


def list_history(db: Session, patient_id: str | None, limit: int = 50) -> list[Analysis]:
    query = db.query(Analysis)
    if patient_id:
        query = query.filter(Analysis.patient_id == patient_id)
    return query.order_by(Analysis.created_at.desc()).limit(limit).all()


def get_analysis(db: Session, request_id: str) -> Analysis | None:
    return db.query(Analysis).filter(Analysis.request_id == request_id).first()


def delete_analysis(db: Session, request_id: str) -> bool:
    analysis = get_analysis(db, request_id)
    if not analysis:
        return False
    db.delete(analysis)
    db.commit()
    return True
