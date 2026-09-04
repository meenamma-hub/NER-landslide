from database import SessionLocal
from models import RiskData

db = SessionLocal()

risk = RiskData(
    location_id=1,
    rainfall=180,
    soil_moisture=72,
    slope=35,
    elevation=1500,
    risk_score=82,
    risk_level="HIGH"
)

db.add(risk)
db.commit()

print("Risk data added successfully!")

db.close()