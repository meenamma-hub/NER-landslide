from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models import Hospital
from schemas import HospitalCreate, HospitalResponse


router = APIRouter(
    prefix="/hospitals",
    tags=["Hospitals"]
)


@router.get("/", response_model=list[HospitalResponse])
def get_hospitals(db: Session = Depends(get_db)):
    return db.query(Hospital).all()


@router.get("/{hospital_id}", response_model=HospitalResponse)
def get_hospital(
    hospital_id: int,
    db: Session = Depends(get_db)
):
    hospital = (
        db.query(Hospital)
        .filter(Hospital.id == hospital_id)
        .first()
    )

    if not hospital:
        raise HTTPException(
            status_code=404,
            detail="Hospital not found"
        )

    return hospital


@router.post("/", response_model=HospitalResponse)
def create_hospital(
    hospital_data: HospitalCreate,
    db: Session = Depends(get_db)
):
    hospital = Hospital(
        name=hospital_data.name,
        location=hospital_data.location,
        latitude=hospital_data.latitude,
        longitude=hospital_data.longitude,
        distance=hospital_data.distance,
        emergency_beds=hospital_data.emergency_beds,
        status=hospital_data.status,
    )

    db.add(hospital)
    db.commit()
    db.refresh(hospital)

    return hospital
