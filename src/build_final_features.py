from pathlib import Path
import pandas as pd


# ============================================================
# PROJECT PATH
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / "data"
PROCESSED_DIR = DATA_DIR / "processed"

BASE_FILE = (
    PROCESSED_DIR
    / "landslide_training_base.csv"
)

RAINFALL_FILE = (
    PROCESSED_DIR
    / "imerg"
    / "aizawl_daily_rainfall.csv"
)

TERRAIN_FILE = (
    PROCESSED_DIR
    / "terrain_features.csv"
)

OUTPUT_FILE = (
    PROCESSED_DIR
    / "landslide_training_features.csv"
)


# ============================================================
# FIND INVENTORY AUTOMATICALLY
# ============================================================

inventory_candidates = list(
    BASE_DIR.rglob("Aizawl_Landslide_Inventory_2015_2025.xlsx")
)

if len(inventory_candidates) == 0:
    raise FileNotFoundError(
        "\nCould not find:\n"
        "Aizawl_Landslide_Inventory_2015_2025.xlsx\n\n"
        "Put the Excel inventory somewhere inside the project folder:\n"
        f"{BASE_DIR}\n"
    )

if len(inventory_candidates) > 1:
    print("\nMultiple inventory files found:")
    for file in inventory_candidates:
        print(f"  {file}")

    raise ValueError(
        "\nMore than one inventory file was found. "
        "Keep only the correct one."
    )

INVENTORY_FILE = inventory_candidates[0]


# ============================================================
# REQUIRED COLUMNS
# ============================================================

BASE_COLUMNS = [
    "observation_date_ist",
    "cell_id",
    "cell_latitude_center",
    "cell_longitude_center",
    "landslide_occurred_next_7d",
]

RAIN_COLUMNS = [
    "date",
    "cell_id",
    "rainfall_24h_mm",
]

TERRAIN_COLUMNS = [
    "cell_id",
    "elevation_m",
    "slope_degrees",
]


def check_columns(df, required, name):

    missing = [
        column
        for column in required
        if column not in df.columns
    ]

    if missing:
        raise ValueError(
            f"\n{name} is missing columns:\n"
            + "\n".join(f"  - {c}" for c in missing)
        )


# ============================================================
# START
# ============================================================

print("=" * 70)
print("BUILDING FINAL LANDSLIDE ML FEATURE TABLE")
print("=" * 70)


# ============================================================
# 1. CHECK FILES
# ============================================================

print("\n[1/8] Checking input files...")

files_to_check = [
    BASE_FILE,
    RAINFALL_FILE,
    TERRAIN_FILE,
    INVENTORY_FILE,
]

for file in files_to_check:

    if not file.exists():

        raise FileNotFoundError(
            f"\nMissing file:\n{file}"
        )

    print(f"  ✓ {file.name}")

print("\n  All required files found.")


# ============================================================
# 2. LOAD TRAINING BASE
# ============================================================

print("\n[2/8] Loading training base...")

base = pd.read_csv(BASE_FILE)

check_columns(
    base,
    BASE_COLUMNS,
    "Training base"
)

base["observation_date_ist"] = pd.to_datetime(
    base["observation_date_ist"]
)

print(f"  Rows: {len(base):,}")
print(f"  Cells: {base['cell_id'].nunique()}")

print(
    f"  Observation dates: "
    f"{base['observation_date_ist'].min().date()} "
    f"→ "
    f"{base['observation_date_ist'].max().date()}"
)


# ============================================================
# 3. LOAD RAINFALL
# ============================================================

print("\n[3/8] Loading NASA rainfall data...")

rain = pd.read_csv(RAINFALL_FILE)

check_columns(
    rain,
    RAIN_COLUMNS,
    "Rainfall data"
)

rain["date"] = pd.to_datetime(
    rain["date"]
)

rain_duplicates = rain.duplicated(
    subset=["date", "cell_id"]
).sum()

if rain_duplicates > 0:

    raise ValueError(
        f"Rainfall data contains "
        f"{rain_duplicates} duplicate date/cell rows."
    )

print(f"  Rows: {len(rain):,}")
print(f"  Dates: {rain['date'].nunique()}")
print(f"  Cells: {rain['cell_id'].nunique()}")

print(
    f"  Valid rainfall values: "
    f"{rain['rainfall_24h_mm'].notna().sum()}/"
    f"{len(rain)}"
)


# ============================================================
# 4. CALCULATE 7-DAY RAINFALL
# ============================================================

print("\n[4/8] Calculating rainfall_7d_mm...")

rain = rain.sort_values(
    ["cell_id", "date"]
).copy()

processed_groups = []

for cell_id, group in rain.groupby("cell_id"):

    group = group.sort_values(
        "date"
    ).copy()

    group = group.set_index("date")

    # Require seven consecutive daily rainfall observations.
    group["rainfall_7d_mm"] = (
        group["rainfall_24h_mm"]
        .rolling(
            window="7D",
            min_periods=7
        )
        .sum()
    )

    group = group.reset_index()

    processed_groups.append(group)


rain = pd.concat(
    processed_groups,
    ignore_index=True
)

print(
    f"  Valid 7-day rainfall values: "
    f"{rain['rainfall_7d_mm'].notna().sum()}/"
    f"{len(rain)}"
)


# ============================================================
# 5. LOAD TERRAIN
# ============================================================

print("\n[5/8] Loading terrain features...")

terrain = pd.read_csv(
    TERRAIN_FILE
)

check_columns(
    terrain,
    TERRAIN_COLUMNS,
    "Terrain data"
)

terrain_duplicates = terrain.duplicated(
    subset=["cell_id"]
).sum()

if terrain_duplicates > 0:

    raise ValueError(
        f"Terrain data contains "
        f"{terrain_duplicates} duplicate cell IDs."
    )

print(
    f"  Terrain rows: {len(terrain)}"
)

print(
    f"  Terrain cells: "
    f"{terrain['cell_id'].nunique()}"
)

print(
    f"  Elevation range: "
    f"{terrain['elevation_m'].min():.1f} → "
    f"{terrain['elevation_m'].max():.1f} m"
)

print(
    f"  Slope range: "
    f"{terrain['slope_degrees'].min():.2f} → "
    f"{terrain['slope_degrees'].max():.2f}°"
)


# ============================================================
# 6. HISTORICAL LANDSLIDE COUNT
# ============================================================

print(
    "\n[6/8] Calculating "
    "historical_landslide_count_5y..."
)

inventory = pd.read_excel(
    INVENTORY_FILE,
    sheet_name="Aizawl Landslide Inventory"
)

# Keep only actual records.
inventory = inventory[
    inventory["Date"].notna()
    &
    inventory["Latitude (°N)"].notna()
    &
    inventory["Longitude (°E)"].notna()
].copy()

inventory["Date"] = pd.to_datetime(
    inventory["Date"]
)

inventory["Latitude (°N)"] = pd.to_numeric(
    inventory["Latitude (°N)"],
    errors="coerce"
)

inventory["Longitude (°E)"] = pd.to_numeric(
    inventory["Longitude (°E)"],
    errors="coerce"
)

inventory = inventory.dropna(
    subset=[
        "Date",
        "Latitude (°N)",
        "Longitude (°E)"
    ]
)

print(
    f"  Valid inventory records retained: "
    f"{len(inventory)}"
)


# ============================================================
# MAP INVENTORY TO IMERG CELLS
# ============================================================

def get_cell_id(latitude, longitude):

    row = int(
        (latitude + 90.0) // 0.1
    )

    column = int(
        (longitude + 180.0) // 0.1
    )

    return (
        f"IMERG_r{row}_c{column}"
    )


inventory["cell_id"] = inventory.apply(
    lambda row: get_cell_id(
        row["Latitude (°N)"],
        row["Longitude (°E)"]
    ),
    axis=1
)


# One occurrence per cell/date.
inventory_events = (
    inventory[
        ["Date", "cell_id"]
    ]
    .drop_duplicates()
    .rename(
        columns={
            "Date": "event_date"
        }
    )
)

print(
    f"  Unique cell-date occurrences: "
    f"{len(inventory_events)}"
)

print(
    f"  Occupied cells: "
    f"{inventory_events['cell_id'].nunique()}"
)


# ============================================================
# HISTORICAL COUNT FUNCTION
# ============================================================

def calculate_historical_count(row):

    observation_date = (
        row["observation_date_ist"]
    )

    cell_id = row["cell_id"]

    start_date = (
        observation_date
        - pd.Timedelta(days=5 * 365)
    )

    mask = (
        (inventory_events["cell_id"] == cell_id)
        &
        (inventory_events["event_date"] >= start_date)
        &
        (inventory_events["event_date"] < observation_date)
    )

    return int(mask.sum())


base[
    "historical_landslide_count_5y"
] = base.apply(
    calculate_historical_count,
    axis=1
)

print(
    "  Historical count calculated."
)

print(
    f"  Count range: "
    f"{base['historical_landslide_count_5y'].min()} "
    f"→ "
    f"{base['historical_landslide_count_5y'].max()}"
)


# ============================================================
# JOIN RAINFALL
# ============================================================

print(
    "\n[7/8] Joining rainfall + terrain..."
)

rain_features = rain.rename(
    columns={
        "date": "observation_date_ist"
    }
)

rain_features = rain_features[
    [
        "observation_date_ist",
        "cell_id",
        "rainfall_24h_mm",
        "rainfall_7d_mm",
    ]
]

final = base.merge(
    rain_features,
    on=[
        "observation_date_ist",
        "cell_id"
    ],
    how="left",
    validate="one_to_one"
)


# ============================================================
# JOIN TERRAIN
# ============================================================

final = final.merge(
    terrain[
        [
            "cell_id",
            "elevation_m",
            "slope_degrees"
        ]
    ],
    on="cell_id",
    how="left",
    validate="many_to_one"
)


# ============================================================
# VALIDATION
# ============================================================

print("\n" + "=" * 70)
print("VALIDATING FINAL FEATURE TABLE")
print("=" * 70)


# Row count
print(
    f"\nRows: {len(final):,}"
)

print(
    f"Cells: {final['cell_id'].nunique()}"
)

if len(final) != len(base):

    raise ValueError(
        "ROW COUNT CHANGED AFTER JOIN!\n"
        f"Expected: {len(base):,}\n"
        f"Got: {len(final):,}"
    )


# ============================================================
# FINAL FEATURES
# ============================================================

FEATURE_COLUMNS = [
    "rainfall_24h_mm",
    "rainfall_7d_mm",
    "elevation_m",
    "slope_degrees",
    "historical_landslide_count_5y",
]

TARGET_COLUMN = (
    "landslide_occurred_next_7d"
)


print("\nFinal ML features:")

for feature in FEATURE_COLUMNS:

    missing = final[feature].isna().sum()

    print(
        f"  {feature:<35} "
        f"missing: {missing:,}"
    )


# ============================================================
# TARGET DISTRIBUTION
# ============================================================

print("\nTarget distribution:")

print(
    final[TARGET_COLUMN]
    .value_counts()
    .sort_index()
)


# ============================================================
# POSITIVE SAMPLE CHECK
# ============================================================

positive = final[
    final[TARGET_COLUMN] == 1
]

complete_positive = positive[
    positive[FEATURE_COLUMNS]
    .notna()
    .all(axis=1)
]

print(
    f"\nPositive rows: "
    f"{len(positive)}"
)

print(
    f"Positive rows with ALL features: "
    f"{len(complete_positive)}"
)

print(
    f"Positive rows missing features: "
    f"{len(positive) - len(complete_positive)}"
)


# ============================================================
# SAMPLE
# ============================================================

print(
    "\nSample of final features:"
)

print(
    final[
        [
            "observation_date_ist",
            "cell_id",
            "rainfall_24h_mm",
            "rainfall_7d_mm",
            "elevation_m",
            "slope_degrees",
            "historical_landslide_count_5y",
            TARGET_COLUMN,
        ]
    ]
    .head(15)
    .to_string(index=False)
)


# ============================================================
# SAVE
# ============================================================

final.to_csv(
    OUTPUT_FILE,
    index=False
)


# ============================================================
# SUCCESS
# ============================================================

print("\n" + "=" * 70)
print("SUCCESS")
print("=" * 70)

print(
    f"\nSaved final feature table to:\n"
    f"{OUTPUT_FILE}"
)

print("\nFeatures included:")

for feature in FEATURE_COLUMNS:
    print(f"  ✓ {feature}")

print(
    f"  ✓ {TARGET_COLUMN}"
)

print(
    "\nNo machine-learning model was trained."
)