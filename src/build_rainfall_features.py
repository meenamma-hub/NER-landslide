import pandas as pd
from pathlib import Path


# --------------------------------------------------
# Paths
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parents[1]

RAIN_DIR = BASE_DIR / "data" / "processed" / "imerg"

MAIN_RAINFALL = RAIN_DIR / "aizawl_daily_rainfall.csv"
TEST_RAINFALL = RAIN_DIR / "imerg_test_3days_aizawl.csv"

TRAINING_BASE = (
    BASE_DIR
    / "data"
    / "processed"
    / "landslide_training_base.csv"
)

OUTPUT = (
    BASE_DIR
    / "data"
    / "processed"
    / "landslide_training_rainfall.csv"
)


# --------------------------------------------------
# 1. Load rainfall files
# --------------------------------------------------

print("Loading rainfall data...")

main = pd.read_csv(MAIN_RAINFALL)
test = pd.read_csv(TEST_RAINFALL)

columns = [
    "date",
    "cell_id",
    "cell_latitude_center",
    "cell_longitude_center",
    "rainfall_24h_mm",
]

main = main[columns]
test = test[columns]

rainfall = pd.concat([main, test], ignore_index=True)

rainfall["date"] = pd.to_datetime(rainfall["date"])

rainfall = (
    rainfall
    .drop_duplicates(
        subset=["date", "cell_id"],
        keep="last"
    )
    .sort_values(["cell_id", "date"])
    .reset_index(drop=True)
)

print(f"Rainfall rows: {len(rainfall)}")
print(
    f"Dates: {rainfall['date'].min().date()} "
    f"to {rainfall['date'].max().date()}"
)
print(f"Unique dates: {rainfall['date'].nunique()}")
print(f"Cells: {rainfall['cell_id'].nunique()}")


# --------------------------------------------------
# 2. Calculate 7-day rainfall
# --------------------------------------------------

print("\nCalculating rainfall_7d_mm...")

rainfall["rainfall_7d_mm"] = (
    rainfall
    .groupby("cell_id")["rainfall_24h_mm"]
    .transform(
        lambda x: x.rolling(
            window=7,
            min_periods=7
        ).sum()
    )
)


# --------------------------------------------------
# 3. Load landslide training table
# --------------------------------------------------

print("\nLoading landslide training table...")

training = pd.read_csv(TRAINING_BASE)

training["observation_date_ist"] = pd.to_datetime(
    training["observation_date_ist"]
)


# --------------------------------------------------
# 4. Prepare rainfall date for joining
# --------------------------------------------------

rainfall = rainfall.rename(
    columns={"date": "observation_date_ist"}
)


rainfall_features = rainfall[
    [
        "observation_date_ist",
        "cell_id",
        "rainfall_24h_mm",
        "rainfall_7d_mm",
    ]
]


# --------------------------------------------------
# 5. Join rainfall features
# --------------------------------------------------

print("Joining rainfall features...")

training = training.merge(
    rainfall_features,
    on=[
        "observation_date_ist",
        "cell_id"
    ],
    how="left",
)


# --------------------------------------------------
# 6. Save
# --------------------------------------------------

training.to_csv(OUTPUT, index=False)

print("\nDone!")
print(f"Saved to: {OUTPUT}")

print("\nFinal shape:")
print(training.shape)

print("\nRainfall feature availability:")

print(
    training[
        [
            "rainfall_24h_mm",
            "rainfall_7d_mm"
        ]
    ].notna().sum()
)

print("\nRows with both rainfall features:")
print(
    training[
        [
            "rainfall_24h_mm",
            "rainfall_7d_mm"
        ]
    ]
    .notna()
    .all(axis=1)
    .sum()
)