from fastapi import APIRouter, Depends, Form, UploadFile, File
from sqlalchemy.orm import Session
from pathlib import Path
import shutil
import uuid

from database import get_db
from models import Report
from schemas import ReportResponse


router = APIRouter(
    prefix="/reports",
    tags=["Reports"]
)


# Folder where uploaded images will be stored
UPLOAD_DIR = Path("uploads/reports")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


@router.post("/", response_model=ReportResponse)
def create_report(
    location: str = Form(...),
    description: str = Form(...),
    latitude: float | None = Form(None),
    longitude: float | None = Form(None),
    report_type: str = Form("LANDSLIDE"),
    image: UploadFile | None = File(None),
    db: Session = Depends(get_db)
):

    image_path = None

    # Save image if provided
    if image:
        file_extension = Path(image.filename).suffix.lower()

        # Generate unique filename
        filename = f"report_{uuid.uuid4().hex}{file_extension}"

        file_path = UPLOAD_DIR / filename

        with file_path.open("wb") as buffer:
            shutil.copyfileobj(image.file, buffer)

        # Browser-friendly path
        image_path = f"/uploads/reports/{filename}"

    # Create database record
    new_report = Report(
        location=location,
        description=description,
        latitude=latitude,
        longitude=longitude,
        report_type=report_type,
        image_path=image_path
    )

    db.add(new_report)
    db.commit()
    db.refresh(new_report)

    return new_report


@router.get("/", response_model=list[ReportResponse])
def get_reports(db: Session = Depends(get_db)):
    return db.query(Report).order_by(
        Report.created_at.desc()
    ).all()