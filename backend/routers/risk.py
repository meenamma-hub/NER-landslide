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
@router.post("/predict")
@router.post("/predict")
@router.post("/predict")
def predict_landslide_risk(
    data: RiskPredictionRequest,
    db: Session = Depends(get_db)
):
    try:
        # 1. Run Aditi's ML model
        result = predict_risk(
            data.rainfall_24h_mm,
            data.rainfall_7d_mm,
            data.elevation_m,
            data.slope_degrees,
            data.historical_landslide_count_5y
        )

        # ML score: 0–1
        # System score: 0–100
        risk_score_100 = result["risk_percentage"]

        # 2. Get Aizawl's existing risk record
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

        # 3. Get Aizawl impact factors
        population_factor = risk_data.population_factor
        infrastructure_factor = risk_data.infrastructure_factor
        connectivity_factor = risk_data.connectivity_factor

        # 4. Calculate impact
        from services.impact_service import calculate_impact

        impact = calculate_impact(
            population_factor,
            connectivity_factor
        )

        # 5. Calculate priority
        from services.priority_service import calculate_priority
        from services.priority_service import get_action

        priority_score, priority = calculate_priority(
            risk_score_100,
            population_factor,
            infrastructure_factor,
            connectivity_factor
        )

        recommended_action = get_action(priority)

        # 6. Update Aizawl's database record
        risk_data.rainfall = data.rainfall_24h_mm
        risk_data.rainfall_7d = data.rainfall_7d_mm
        risk_data.elevation = data.elevation_m
        risk_data.slope = data.slope_degrees
        risk_data.historical_landslide_count = (
            data.historical_landslide_count_5y
        )

        risk_data.risk_score = risk_score_100
        risk_data.risk_level = result["risk_level"]

        risk_data.population_affected = impact["population_affected"]
        risk_data.connectivity_status = impact["connectivity_status"]

        risk_data.priority_score = priority_score
        risk_data.priority = priority
        risk_data.recommended_action = recommended_action

        db.commit()
        db.refresh(risk_data)

        # 7. Return updated result
        return {
            "location": "Aizawl",

            "risk_score": risk_data.risk_score,
            "ml_risk_score": result["risk_score"],
            "risk_level": risk_data.risk_level,

            "population_factor": risk_data.population_factor,
            "infrastructure_factor": risk_data.infrastructure_factor,
            "connectivity_factor": risk_data.connectivity_factor,

            "population_affected": risk_data.population_affected,
            "connectivity_status": risk_data.connectivity_status,

            "priority_score": risk_data.priority_score,
            "priority": risk_data.priority,
            "recommended_action": risk_data.recommended_action
        }

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )