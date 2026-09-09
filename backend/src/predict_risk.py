from pathlib import Path

import joblib
import pandas as pd


# --------------------------------------------------
# Model configuration
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

MODEL_FILE = BASE_DIR / "models" / "landslide_rf.joblib"

FEATURE_COLUMNS = [
    "rainfall_24h_mm",
    "rainfall_7d_mm",
    "elevation_m",
    "slope_degrees",
    "historical_landslide_count_5y",
]


# Load trained model
model = joblib.load(MODEL_FILE)


# --------------------------------------------------
# Risk classification
# --------------------------------------------------

def classify_risk(score):
    """Convert model score into a prototype risk level."""

    if score < 0.25:
        return "LOW"
    elif score < 0.50:
        return "MODERATE"
    elif score < 0.75:
        return "HIGH"
    else:
        return "CRITICAL"


# --------------------------------------------------
# Input validation
# --------------------------------------------------

def validate_inputs(
    rainfall_24h_mm,
    rainfall_7d_mm,
    elevation_m,
    slope_degrees,
    historical_landslide_count_5y,
):
    """Validate input values before sending them to the model."""

    if rainfall_24h_mm < 0:
        raise ValueError("24-hour rainfall cannot be negative.")

    if rainfall_7d_mm < 0:
        raise ValueError("7-day rainfall cannot be negative.")

    if elevation_m < 0:
        raise ValueError("Elevation cannot be negative.")

    if not 0 <= slope_degrees <= 90:
        raise ValueError("Slope must be between 0 and 90 degrees.")

    if historical_landslide_count_5y < 0:
        raise ValueError(
            "Historical landslide count cannot be negative."
        )


# --------------------------------------------------
# Risk prediction
# --------------------------------------------------

def predict_risk(
    rainfall_24h_mm,
    rainfall_7d_mm,
    elevation_m,
    slope_degrees,
    historical_landslide_count_5y,
):
    """
    Predict landslide hazard risk for a location.

    Returns:
        dict containing:
        - risk_score
        - risk_percentage
        - risk_level
    """

    validate_inputs(
        rainfall_24h_mm,
        rainfall_7d_mm,
        elevation_m,
        slope_degrees,
        historical_landslide_count_5y,
    )

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

    # Positive-class model score.
    score = float(model.predict_proba(data)[0][1])

    return {
        "risk_score": round(score, 4),
        "risk_percentage": round(score * 100, 2),
        "risk_level": classify_risk(score),
    }


# --------------------------------------------------
# Local testing
# --------------------------------------------------

if __name__ == "__main__":

    print("\n=== Landslide Risk Predictor ===\n")

    try:
        rainfall_24h = float(
            input("24-hour rainfall (mm): ")
        )

        rainfall_7d = float(
            input("7-day rainfall (mm): ")
        )

        elevation = float(
            input("Elevation (m): ")
        )

        slope = float(
            input("Slope (degrees): ")
        )

        historical = int(
            input("Historical landslides (last 5 years): ")
        )

        result = predict_risk(
            rainfall_24h,
            rainfall_7d,
            elevation,
            slope,
            historical,
        )

        print("\nPrediction:")
        print(f"Risk Score:       {result['risk_score']}")
        print(f"Risk Percentage:  {result['risk_percentage']}%")
        print(f"Risk Level:       {result['risk_level']}")

    except ValueError as error:
        print(f"\nInput error: {error}")