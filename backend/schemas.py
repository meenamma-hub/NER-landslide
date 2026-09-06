from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class LocationCreate(BaseModel):
    name: str
    district: str
    state: str
    latitude: float
    longitude: float
    population: int = 0


class LocationResponse(LocationCreate):
    id: int

    class Config:
        from_attributes = True


class RiskResponse(BaseModel):
    id: int
    location_id: int

    rainfall: float
    soil_moisture: float
    slope: float
    elevation: float

    risk_score: float
    risk_level: str

    class Config:
        from_attributes = True


class ReportCreate(BaseModel):
    location: str
    description: str

    latitude: Optional[float] = None
    longitude: Optional[float] = None

    report_type: str = "LANDSLIDE"


class ReportResponse(ReportCreate):
    id: int
    image_path: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


class AlertCreate(BaseModel):
    location_id: int
    title: str
    message: str
    risk_level: str = "LOW"
    priority: str = "P3"
    status: str = "ACTIVE"


class AlertResponse(AlertCreate):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True