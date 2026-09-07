from database import SessionLocal
from models import Location, RiskData

db = SessionLocal()

# Clear existing data so we can safely re-seed
db.query(RiskData).delete()
db.query(Location).delete()

# ---------------------------------------------------------
# 10 NER locations
# ---------------------------------------------------------

locations = [
    Location(
        name="Tawang",
        district="Tawang",
        state="Arunachal Pradesh",
        latitude=27.5861,
        longitude=91.8594,
        population=11000
    ),
    Location(
        name="Bomdila",
        district="West Kameng",
        state="Arunachal Pradesh",
        latitude=27.2648,
        longitude=92.4247,
        population=7000
    ),
    Location(
        name="Itanagar",
        district="Papum Pare",
        state="Arunachal Pradesh",
        latitude=27.0844,
        longitude=93.6053,
        population=60000
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
        name="Churachandpur",
        district="Churachandpur",
        state="Manipur",
        latitude=24.3333,
        longitude=93.6833,
        population=32000
    ),
    Location(
        name="Kohima",
        district="Kohima",
        state="Nagaland",
        latitude=25.6751,
        longitude=94.1086,
        population=99000
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
        name="Gangtok",
        district="East Sikkim",
        state="Sikkim",
        latitude=27.3389,
        longitude=88.6065,
        population=100000
    ),
    Location(
        name="Haflong",
        district="Dima Hasao",
        state="Assam",
        latitude=25.1648,
        longitude=93.0176,
        population=43000
    ),
    Location(
        name="Agartala",
        district="West Tripura",
        state="Tripura",
        latitude=23.8315,
        longitude=91.2868,
        population=400000
    )
]

db.add_all(locations)
db.commit()

# Refresh IDs
for location in locations:
    db.refresh(location)

# ---------------------------------------------------------
# Risk + Impact sample data
#
# Aizawl's risk will later be replaced dynamically
# by Aditi's ML prediction.
# ---------------------------------------------------------

risk_data = [
    RiskData(
        location_id=locations[0].id,
        rainfall=180,
        rainfall_7d=450,
        soil_moisture=72,
        slope=35,
        elevation=3000,
        historical_landslide_count=4,
        risk_score=82,
        risk_level="CRITICAL",
        population_factor=80,
        infrastructure_factor=90,
        connectivity_factor=85
    ),

    RiskData(
        location_id=locations[1].id,
        rainfall=150,
        rainfall_7d=380,
        soil_moisture=68,
        slope=32,
        elevation=2200,
        historical_landslide_count=3,
        risk_score=74,
        risk_level="HIGH",
        population_factor=60,
        infrastructure_factor=75,
        connectivity_factor=80
    ),

    RiskData(
        location_id=locations[2].id,
        rainfall=120,
        rainfall_7d=300,
        soil_moisture=60,
        slope=28,
        elevation=400,
        historical_landslide_count=2,
        risk_score=68,
        risk_level="HIGH",
        population_factor=90,
        infrastructure_factor=85,
        connectivity_factor=70
    ),

    RiskData(
        location_id=locations[3].id,
        rainfall=160,
        rainfall_7d=400,
        soil_moisture=68,
        slope=32,
        elevation=1100,
        historical_landslide_count=3,
        risk_score=86,
        risk_level="CRITICAL",
        population_factor=85,
        infrastructure_factor=80,
        connectivity_factor=90
    ),

    RiskData(
        location_id=locations[4].id,
        rainfall=140,
        rainfall_7d=350,
        soil_moisture=65,
        slope=30,
        elevation=900,
        historical_landslide_count=3,
        risk_score=79,
        risk_level="HIGH",
        population_factor=70,
        infrastructure_factor=65,
        connectivity_factor=80
    ),

    RiskData(
        location_id=locations[5].id,
        rainfall=130,
        rainfall_7d=320,
        soil_moisture=62,
        slope=27,
        elevation=1450,
        historical_landslide_count=2,
        risk_score=72,
        risk_level="HIGH",
        population_factor=75,
        infrastructure_factor=80,
        connectivity_factor=75
    ),

    RiskData(
        location_id=locations[6].id,
        rainfall=110,
        rainfall_7d=280,
        soil_moisture=58,
        slope=25,
        elevation=1500,
        historical_landslide_count=2,
        risk_score=65,
        risk_level="HIGH",
        population_factor=85,
        infrastructure_factor=80,
        connectivity_factor=70
    ),

    RiskData(
        location_id=locations[7].id,
        rainfall=170,
        rainfall_7d=420,
        soil_moisture=70,
        slope=34,
        elevation=1650,
        historical_landslide_count=4,
        risk_score=88,
        risk_level="CRITICAL",
        population_factor=75,
        infrastructure_factor=90,
        connectivity_factor=85
    ),

    RiskData(
        location_id=locations[8].id,
        rainfall=145,
        rainfall_7d=360,
        soil_moisture=64,
        slope=29,
        elevation=700,
        historical_landslide_count=3,
        risk_score=76,
        risk_level="HIGH",
        population_factor=55,
        infrastructure_factor=65,
        connectivity_factor=80
    ),

    RiskData(
        location_id=locations[9].id,
        rainfall=70,
        rainfall_7d=180,
        soil_moisture=45,
        slope=15,
        elevation=20,
        historical_landslide_count=1,
        risk_score=45,
        risk_level="MODERATE",
        population_factor=80,
        infrastructure_factor=70,
        connectivity_factor=60
    )
]

# ---------------------------------------------------------
# Calculate impact + priority for every location
# ---------------------------------------------------------

for risk in risk_data:

    # Impact
    risk.population_affected = risk.population_factor * 10

    if risk.connectivity_factor >= 80:
        risk.connectivity_status = "High connectivity risk"

    elif risk.connectivity_factor >= 60:
        risk.connectivity_status = "Moderate connectivity risk"

    else:
        risk.connectivity_status = "Low connectivity risk"

    # Priority
    priority_score = (
        risk.risk_score * 0.4
        + risk.population_factor * 0.2
        + risk.infrastructure_factor * 0.2
        + risk.connectivity_factor * 0.2
    )

    risk.priority_score = round(priority_score)

    if risk.priority_score >= 80:
        risk.priority = "P1"
        risk.recommended_action = "Deploy response team immediately"

    elif risk.priority_score >= 60:
        risk.priority = "P2"
        risk.recommended_action = "Urgent field inspection required"

    else:
        risk.priority = "P3"
        risk.recommended_action = "Continuous monitoring"


db.add_all(risk_data)
db.commit()

print("10 NER locations, risk, impact and priority data added successfully!")

db.close()