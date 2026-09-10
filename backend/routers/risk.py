from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models import Location, RiskData

from schemas import RiskResponse, RiskPredictionRequest
from src.predict_risk import predict_risk


router = APIRouter(
    prefix="/risk",
    tags=["Risk"]
)
@router.get("/overview")
def get_risk_overview(db: Session = Depends(get_db)):
    results = (
        db.query(Location, RiskData)
        .join(
            RiskData,
            Location.id == RiskData.location_id
        )
        .all()
    )

    return [
        {
            "location_id": location.id,
            "location": location.name,
            "district": location.district,
            "state": location.state,
            "latitude": location.latitude,
            "longitude": location.longitude,

            "risk_score": risk.risk_score,
"risk_level": risk.risk_level,
"rainfall": risk.rainfall,

"population_factor": risk.population_factor,
            "infrastructure_factor": risk.infrastructure_factor,
            "connectivity_factor": risk.connectivity_factor,

            "population_affected": risk.population_affected,

            "priority_score": risk.priority_score,
            "priority": risk.priority,
            "recommended_action": risk.recommended_action
        }
        for location, risk in results
    ]

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


@router.post("/predict")
def predict_landslide_risk(
    data: RiskPredictionRequest,
    db: Session = Depends(get_db)
):
    try:
        # 1. Run ML prediction
        result = predict_risk(
            data.rainfall_24h_mm,
            data.rainfall_7d_mm,
            data.elevation_m,
            data.slope_degrees,
            data.historical_landslide_count_5y
        )

        # ML score converted from 0–1 to 0–100
        risk_score_100 = result["risk_percentage"]

        # 2. Get Aizawl's existing impact factors
        risk_data = (
            db.query(RiskData)
            .filter(RiskData.location_id == 4)
            .first()
        )

        if not risk_data:
            raise HTTPException(
                status_code=404,
                detail="Aizawl risk data not found"
            )

        population_factor = risk_data.population_factor
        infrastructure_factor = risk_data.infrastructure_factor
        connectivity_factor = risk_data.connectivity_factor

        # 3. Calculate impact
        from services.impact_service import calculate_impact

        impact = calculate_impact(
            population_factor,
            connectivity_factor
        )

        # 4. Calculate priority
        from services.priority_service import (
            calculate_priority,
            get_action
        )

        priority_score, priority = calculate_priority(
            risk_score_100,
            population_factor,
            infrastructure_factor,
            connectivity_factor
        )

        recommended_action = get_action(priority)

        # 5. Return prediction ONLY
        # IMPORTANT:
        # We do NOT update or commit the database here.
        return {
            "location": "Aizawl",

            "risk_score": risk_score_100,
            "ml_risk_score": result["risk_score"],
            "risk_level": result["risk_level"],

            "population_factor": population_factor,
            "infrastructure_factor": infrastructure_factor,
            "connectivity_factor": connectivity_factor,

            "population_affected": impact["population_affected"],
            "connectivity_status": impact["connectivity_status"],

            "priority_score": priority_score,
            "priority": priority,
            "recommended_action": recommended_action
        }

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )