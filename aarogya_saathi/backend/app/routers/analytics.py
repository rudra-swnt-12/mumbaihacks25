from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db, Patient, Consultation

router = APIRouter(prefix="/analytics", tags=["Analytics"])


@router.get("/dashboard-stats")
async def get_dashboard_stats(db: Session = Depends(get_db)):
    """
    Returns high-level stats for the Doctor's God Mode Dashboard.
    """
    total_patients = db.query(Patient).count()
    critical_count = db.query(Patient).filter(Patient.medication_adherence < 50).count()
    recent_calls = (
        db.query(Consultation).order_by(Consultation.id.desc()).limit(5).all()
    )

    return {
        "total_patients": total_patients,
        "active_monitoring": total_patients,
        "critical_alerts": critical_count,
        "recent_activity": [
            {"time": log.timestamp, "summary": log.summary, "risk": log.risk_score}
            for log in recent_calls
        ],
    }
