from sqlalchemy import Column, Integer, String, Float, Text, DateTime
from datetime import datetime

from database import Base


class Location(Base):
    __tablename__ = "locations"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, nullable=False)
    district = Column(String, nullable=False)
    state = Column(String, nullable=False)

    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)

    population = Column(Integer, default=0)


class RiskData(Base):
    __tablename__ = "risk_data"

    id = Column(Integer, primary_key=True, index=True)

    location_id = Column(Integer, nullable=False)

    rainfall = Column(Float, default=0)
    soil_moisture = Column(Float, default=0)
    slope = Column(Float, default=0)
    elevation = Column(Float, default=0)

    risk_score = Column(Float, default=0)
    risk_level = Column(String, default="LOW")


class Report(Base):
    __tablename__ = "reports"

    id = Column(Integer, primary_key=True, index=True)

    location = Column(String, nullable=False)
    description = Column(Text, nullable=False)

    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)

    report_type = Column(String, default="LANDSLIDE")

    image_path = Column(String, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)


class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)

    location_id = Column(Integer, nullable=False)

    title = Column(String, nullable=False)
    message = Column(Text, nullable=False)

    risk_level = Column(String, default="LOW")
    priority = Column(String, default="P3")
    status = Column(String, default="ACTIVE")

    created_at = Column(DateTime, default=datetime.utcnow)