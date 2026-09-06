from database import SessionLocal
from models import Location, RiskData

db = SessionLocal()

# Clear existing data so we can safely re-seed
db.query(RiskData).delete()
db.query(Location).delete()

# Create locations
locations = [
    Location(
        name="Cherrapunji",
        district="East Khasi Hills",
        state="Meghalaya",
        latitude=25.264,
        longitude=91.732,
        population=15000
    ),
    Location(
        name="Mawsynram",
        district="East Khasi Hills",
        state="Meghalaya",
        latitude=25.298,
        longitude=91.582,
        population=12000
    ),
    Location(
        name="Shillong",
        district="East Khasi Hills",
        state="Meghalaya",
        latitude=25.5788,
        longitude=91.8933,
        population=143000
    ),
    Location(
        name="Aizawl",
        district="Aizawl",
        state="Mizoram",
        latitude=23.7271,
        longitude=92.7176,
        population=293000
    ),
    Location(
        name="Gangtok",
        district="East Sikkim",
        state="Sikkim",
        latitude=27.3389,
        longitude=88.6065,
        population=100000
    )
]

db.add_all(locations)
db.commit()

# Refresh IDs
for location in locations:
    db.refresh(location)

# Add risk data
risk_data = [
    RiskData(
        location_id=locations[0].id,
        rainfall=180,
        soil_moisture=72,
        slope=35,
        elevation=1500,
        risk_score=82,
        risk_level="HIGH"
    ),
    RiskData(
        location_id=locations[1].id,
        rainfall=220,
        soil_moisture=80,
        slope=40,
        elevation=1400,
        risk_score=91,
        risk_level="VERY HIGH"
    ),
    RiskData(
        location_id=locations[2].id,
        rainfall=120,
        soil_moisture=55,
        slope=25,
        elevation=1500,
        risk_score=58,
        risk_level="MODERATE"
    ),
    RiskData(
        location_id=locations[3].id,
        rainfall=160,
        soil_moisture=68,
        slope=32,
        elevation=1100,
        risk_score=76,
        risk_level="HIGH"
    ),
    RiskData(
        location_id=locations[4].id,
        rainfall=100,
        soil_moisture=45,
        slope=22,
        elevation=1650,
        risk_score=42,
        risk_level="MODERATE"
    )
]

db.add_all(risk_data)
db.commit()

print("Locations and risk data added successfully!")

db.close()