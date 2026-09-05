from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from models import Report
from schemas import ReportCreate, ReportResponse

router = APIRouter(
    prefix="/reports",
    tags=["Reports"]
)


@router.post("/", response_model=ReportResponse)
def create_report(
    report: ReportCreate,
    db: Session = Depends(get_db)
):
    new_report = Report(**report.model_dump())

    db.add(new_report)
    db.commit()
    db.refresh(new_report)

    return new_report


@router.get("/", response_model=list[ReportResponse])
def get_reports(db: Session = Depends(get_db)):
    return db.query(Report).order_by(
        Report.created_at.desc()
    ).all()