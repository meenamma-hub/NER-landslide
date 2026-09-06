from pathlib import Path
import joblib
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_FILE = BASE_DIR / "models" / "landslide_rf.joblib"

model = joblib.load(MODEL_FILE)

FEATURE_COLUMNS = [
    "rainfall_24h_mm",
    "rainfall_7d_mm",
    "elevation_m",
    "slope_degrees",
    "historical_landslide_count_5y",
]


def classify_risk(score):
    if score < 0.25:
        return "LOW"
    elif score < 0.50:
        return "MODERATE"
    elif score < 0.75:
        return "HIGH"
    else:
        return "CRITICAL"


def predict_risk(
    rainfall_24h_mm,
    rainfall_7d_mm,
    elevation_m,
    slope_degrees,
    historical_landslide_count_5y,
):
    data = pd.DataFrame(
        [[
            rainfall_24h_mm,
            rainfall_7d_mm,
            elevation_m,
            slope_degrees,
            historical_landslide_count_5y,
        ]],
        columns=FEATURE_COLUMNS,
    )

    score = float(model.predict_proba(data)[0][1])

    return {
        "risk_score": round(score, 4),
        "risk_percentage": round(score * 100, 2),
        "risk_level": classify_risk(score),
    }