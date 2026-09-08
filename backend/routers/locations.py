from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from models import Location
from schemas import LocationCreate, LocationResponse

router = APIRouter(
    prefix="/locations",
    tags=["Locations"]
)


@router.get("/", response_model=list[LocationResponse])
def get_locations(db: Session = Depends(get_db)):
    return db.query(Location).all()


@router.get("/{location_id}", response_model=LocationResponse)
def get_location(location_id: int, db: Session = Depends(get_db)):
    return db.query(Location).filter(
        Location.id == location_id
    ).first()


@router.post("/", response_model=LocationResponse)
def create_location(
    location: LocationCreate,
    db: Session = Depends(get_db)
):
    new_location = Location(**location.model_dump())

    db.add(new_location)
    db.commit()
    db.refresh(new_location)

    return new_location