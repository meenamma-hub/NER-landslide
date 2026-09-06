import pandas as pd
from pathlib import Path


# ============================================================
# 1. PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[1]

RAIN_DIR = (
    BASE_DIR
    / "data"
    / "processed"
    / "imerg"
)

MAIN_RAINFALL = (
    RAIN_DIR
    / "aizawl_daily_rainfall.csv"
)

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


# ============================================================
# 2. LOAD RAINFALL DATA
# ============================================================

print("Loading rainfall data...")

rainfall = pd.read_csv(MAIN_RAINFALL)

required_columns = [
    "date",
    "cell_id",
    "cell_latitude_center",
    "cell_longitude_center",
    "rainfall_24h_mm",
]

missing_columns = [
    column
    for column in required_columns
    if column not in rainfall.columns
]

if missing_columns:
    raise ValueError(
        f"Rainfall file is missing columns: {missing_columns}"
    )

rainfall = rainfall[required_columns].copy()

rainfall["date"] = pd.to_datetime(
    rainfall["date"]
)

# Make sure rainfall values are numeric
rainfall["rainfall_24h_mm"] = pd.to_numeric(
    rainfall["rainfall_24h_mm"],
    errors="coerce"
)

# Remove duplicate date + cell combinations
rainfall = (
    rainfall
    .drop_duplicates(
        subset=["date", "cell_id"],
        keep="last"
    )
    .sort_values(
        ["cell_id", "date"]
    )
    .reset_index(drop=True)
)


print(f"Rainfall rows: {len(rainfall)}")
print(
    f"Dates: "
    f"{rainfall['date'].min().date()} "
    f"to "
    f"{rainfall['date'].max().date()}"
)
print(
    f"Unique dates: "
    f"{rainfall['date'].nunique()}"
)
print(
    f"Cells: "
    f"{rainfall['cell_id'].nunique()}"
)


# ============================================================
# 3. CALCULATE 7-DAY RAINFALL
# ============================================================

print()
print("Calculating rainfall_7d_mm...")


def calculate_7d_for_cell(group):

    # --------------------------------------------------------
    # Sort chronologically
    # --------------------------------------------------------

    group = group.sort_values(
        "date"
    ).copy()

    # --------------------------------------------------------
    # Keep cell_id as a normal column.
    #
    # We calculate the rolling value separately instead of
    # using groupby.apply(), avoiding pandas index issues.
    # --------------------------------------------------------

    group = group.set_index("date")

    # --------------------------------------------------------
    # IMPORTANT:
    #
    # A 7-day feature is valid only when all 7 calendar days
    # are present.
    #
    # Using a 7-day time window with min_periods=7 ensures
    # incomplete periods remain NaN.
    # --------------------------------------------------------

    group["rainfall_7d_mm"] = (
        group["rainfall_24h_mm"]
        .rolling(
            "7D",
            min_periods=7
        )
        .sum()
    )

    return group.reset_index()


# Process every cell independently
cell_results = []

for cell_id, group in rainfall.groupby(
    "cell_id",
    sort=False
):

    result = calculate_7d_for_cell(
        group
    )

    # Explicitly restore cell_id
    result["cell_id"] = cell_id

    cell_results.append(result)


rainfall = pd.concat(
    cell_results,
    ignore_index=True
)


# Final ordering
rainfall = (
    rainfall
    .sort_values(
        ["cell_id", "date"]
    )
    .reset_index(drop=True)
)


# ============================================================
# 4. VALIDATE RAINFALL TABLE
# ============================================================

print()
print("Rainfall feature table:")
print(
    rainfall[
        [
            "date",
            "cell_id",
            "rainfall_24h_mm",
            "rainfall_7d_mm",
        ]
    ].head(15)
)


# ============================================================
# 5. LOAD LANDSLIDE TRAINING BASE
# ============================================================

print()
print("Loading landslide training table...")

training = pd.read_csv(
    TRAINING_BASE
)

if "observation_date_ist" not in training.columns:
    raise ValueError(
        "Training table is missing "
        "'observation_date_ist'."
    )

if "cell_id" not in training.columns:
    raise ValueError(
        "Training table is missing 'cell_id'."
    )

training["observation_date_ist"] = pd.to_datetime(
    training["observation_date_ist"]
)


# ============================================================
# 6. PREPARE RAINFALL FOR JOIN
# ============================================================

rainfall_features = rainfall[
    [
        "date",
        "cell_id",
        "rainfall_24h_mm",
        "rainfall_7d_mm",
    ]
].copy()


rainfall_features = rainfall_features.rename(
    columns={
        "date": "observation_date_ist"
    }
)


# Validate uniqueness before merging
duplicate_keys = rainfall_features.duplicated(
    subset=[
        "observation_date_ist",
        "cell_id",
    ]
).sum()


if duplicate_keys > 0:
    raise ValueError(
        "Rainfall table contains duplicate "
        "date + cell_id combinations: "
        f"{duplicate_keys}"
    )


# ============================================================
# 7. JOIN RAINFALL FEATURES
# ============================================================

print()
print("Joining rainfall features...")

rows_before = len(training)

training = training.merge(
    rainfall_features,
    on=[
        "observation_date_ist",
        "cell_id",
    ],
    how="left",
)


rows_after = len(training)


# Make sure the merge did not duplicate training rows
if rows_after != rows_before:

    raise ValueError(
        "Training row count changed after rainfall merge!\n"
        f"Before: {rows_before}\n"
        f"After:  {rows_after}"
    )


# ============================================================
# 8. REPORT FEATURE AVAILABILITY
# ============================================================

print()
print("Rainfall feature availability")
print("-----------------------------")

print(
    f"rainfall_24h_mm available: "
    f"{training['rainfall_24h_mm'].notna().sum()}"
)

print(
    f"rainfall_7d_mm available: "
    f"{training['rainfall_7d_mm'].notna().sum()}"
)


complete_rainfall = (
    training[
        [
            "rainfall_24h_mm",
            "rainfall_7d_mm",
        ]
    ]
    .notna()
    .all(axis=1)
)


print()
print(
    "Rows with both rainfall features: "
    f"{complete_rainfall.sum()}"
)


# ============================================================
# 9. CHECK POSITIVE SAMPLES
# ============================================================

if "landslide_occurred_next_7d" in training.columns:

    positives = (
        training[
            "landslide_occurred_next_7d"
        ] == 1
    )

    print()
    print("Positive sample availability")
    print("----------------------------")

    print(
        f"Total positive rows: "
        f"{positives.sum()}"
    )

    print(
        f"Positive rows with complete rainfall: "
        f"{(positives & complete_rainfall).sum()}"
    )

    print(
        f"Positive rows missing rainfall: "
        f"{(positives & ~complete_rainfall).sum()}"
    )


# ============================================================
# 10. SAVE
# ============================================================

training.to_csv(
    OUTPUT,
    index=False
)


print()
print("Done!")
print()
print(f"Final rows: {len(training)}")
print(f"Final columns: {len(training.columns)}")
print()
print("Saved to:")
print(OUTPUT)