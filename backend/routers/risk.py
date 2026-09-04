from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models import RiskData
from schemas import RiskResponse

router = APIRouter(
    prefix="/risk",
    tags=["Risk"]
)


@router.get("/{location_id}", response_model=RiskResponse)
def get_risk(
    location_id: int,
    db: Session = Depends(get_db)
):
    risk = db.query(RiskData).filter(
        RiskData.location_id == location_id
    ).first()

    if not risk:
        raise HTTPException(
            status_code=404,
            detail="Risk data not found"
        )

    return risk