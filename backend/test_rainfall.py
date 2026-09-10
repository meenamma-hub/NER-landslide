from src.predict_risk import predict_risk


rainfall_values = [
    0,
    25,
    50,
    75,
    100,
    125,
    150,
    175,
    200,
    225,
    250,
    275,
    300,
]


rainfall_7d = 250
elevation = 1000
slope = 35
historical = 10


print("\n=== RAINFALL SENSITIVITY TEST ===\n")


for rainfall in rainfall_values:

    result = predict_risk(
        rainfall,
        rainfall_7d,
        elevation,
        slope,
        historical,
    )

    print(
        f"{rainfall:>3} mm"
        f"  →  "
        f"{result['risk_percentage']:>6}%"
        f"  →  "
        f"{result['risk_level']}"
    )