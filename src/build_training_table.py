from pathlib import Path
import math
import pandas as pd


# ---------------------------------------------------------
# Paths
# ---------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[1]

INPUT_FILE = PROJECT_ROOT / "data" / "raw" / "Aizawl_Landslide_Inventory_2015_2025.xlsx"
OUTPUT_DIR = PROJECT_ROOT / "data" / "processed"
OUTPUT_FILE = OUTPUT_DIR / "landslide_training_base.csv"


# ---------------------------------------------------------
# IMERG grid helper
# ---------------------------------------------------------

def get_imerg_cell(latitude, longitude):
    """
    Assign a latitude/longitude to the native 0.1° IMERG grid.

    IMERG cell centers are offset by 0.05° from integer
    tenth-degree boundaries.
    """

    row = math.floor((latitude + 90.0) / 0.1)
    column = math.floor((longitude + 180.0) / 0.1)

    cell_south = -90.0 + row * 0.1
    cell_west = -180.0 + column * 0.1

    cell_center_lat = round(cell_south + 0.05, 5)
    cell_center_lon = round(cell_west + 0.05, 5)

    cell_id = f"IMERG_r{row}_c{column}"

    return cell_id, cell_center_lat, cell_center_lon


# ---------------------------------------------------------
# Load inventory
# ---------------------------------------------------------

print("Loading inventory...")

inventory = pd.read_excel(
    INPUT_FILE,
    sheet_name="Aizawl Landslide Inventory"
)

# Keep only actual inventory records.
# The workbook contains formula-only rows near the bottom.
inventory = inventory[inventory["S.No."].notna()].copy()

inventory["Date"] = pd.to_datetime(
    inventory["Date"],
    errors="coerce"
)

inventory["Latitude (°N)"] = pd.to_numeric(
    inventory["Latitude (°N)"],
    errors="coerce"
)

inventory["Longitude (°E)"] = pd.to_numeric(
    inventory["Longitude (°E)"],
    errors="coerce"
)

# Remove malformed records if any exist.
inventory = inventory.dropna(
    subset=["Date", "Latitude (°N)", "Longitude (°E)"]
).copy()

print(f"Inventory records: {len(inventory)}")


# ---------------------------------------------------------
# Assign IMERG cells
# ---------------------------------------------------------

cell_information = inventory.apply(
    lambda row: get_imerg_cell(
        row["Latitude (°N)"],
        row["Longitude (°E)"]
    ),
    axis=1
)

inventory["cell_id"] = cell_information.apply(lambda x: x[0])
inventory["cell_latitude_center"] = cell_information.apply(lambda x: x[1])
inventory["cell_longitude_center"] = cell_information.apply(lambda x: x[2])

inventory["event_date"] = inventory["Date"].dt.normalize()


# ---------------------------------------------------------
# Collapse multiple inventory records occurring in the
# same cell on the same date.
# ---------------------------------------------------------

event_groups = (
    inventory
    .groupby(
        [
            "cell_id",
            "cell_latitude_center",
            "cell_longitude_center",
            "event_date"
        ],
        as_index=False
    )
    .agg(
        inventory_event_count=("S.No.", "count"),
        inventory_event_ids=("S.No.", lambda x: ",".join(
            str(int(v)) for v in x
        ))
    )
)

print(f"Unique cell-date event groups: {len(event_groups)}")


# ---------------------------------------------------------
# Build the study-area cells
#
# These are the 15 cells identified during our previous
# study-area inspection.
# ---------------------------------------------------------

study_cells = []

for row in range(1136, 1141):
    for column in range(2725, 2728):

        cell_south = -90.0 + row * 0.1
        cell_west = -180.0 + column * 0.1

        cell_center_lat = round(cell_south + 0.05, 5)
        cell_center_lon = round(cell_west + 0.05, 5)

        cell_id = f"IMERG_r{row}_c{column}"

        study_cells.append(
            {
                "cell_id": cell_id,
                "cell_latitude_center": cell_center_lat,
                "cell_longitude_center": cell_center_lon
            }
        )

study_cells = pd.DataFrame(study_cells)

occupied_cells = set(event_groups["cell_id"])

study_cells["cell_type"] = study_cells["cell_id"].apply(
    lambda x: "occupied" if x in occupied_cells else "background"
)

print(f"Study-area cells: {len(study_cells)}")
print(f"Occupied cells: {sum(study_cells['cell_type'] == 'occupied')}")
print(f"Background cells: {sum(study_cells['cell_type'] == 'background')}")


# ---------------------------------------------------------
# Observation date range
#
# We need enough history for the 5-year historical count.
# Therefore observations begin 5 years after the earliest
# inventory date.
# ---------------------------------------------------------

earliest_event_date = event_groups["event_date"].min()
latest_event_date = event_groups["event_date"].max()

observation_start = earliest_event_date + pd.DateOffset(years=5)

# We need the target window to remain inside the inventory
# period, so the final observation date is 7 days before
# the final event date.
observation_end = latest_event_date - pd.Timedelta(days=7)

print()
print(f"Earliest inventory event: {earliest_event_date.date()}")
print(f"Latest inventory event:   {latest_event_date.date()}")
print(f"Observation start:         {observation_start.date()}")
print(f"Observation end:           {observation_end.date()}")


# ---------------------------------------------------------
# Create complete cell × observation-date panel
# ---------------------------------------------------------

observation_dates = pd.date_range(
    start=observation_start,
    end=observation_end,
    freq="D"
)

print(f"Observation dates: {len(observation_dates)}")

study_cells["_key"] = 1

date_table = pd.DataFrame(
    {
        "observation_date_ist": observation_dates,
        "_key": 1
    }
)

training_base = study_cells.merge(
    date_table,
    on="_key"
).drop(columns="_key")


# ---------------------------------------------------------
# Create future 7-day target window
# ---------------------------------------------------------

training_base["target_window_start"] = (
    training_base["observation_date_ist"]
    + pd.Timedelta(days=1)
)

training_base["target_window_end"] = (
    training_base["observation_date_ist"]
    + pd.Timedelta(days=7)
)


# ---------------------------------------------------------
# Create event lookup
# ---------------------------------------------------------

event_lookup = event_groups[
    [
        "cell_id",
        "event_date",
        "inventory_event_count",
        "inventory_event_ids"
    ]
].copy()


# ---------------------------------------------------------
# Label each observation date
#
# Positive if at least one inventory event exists in:
#
# observation_date + 1 day
# through
# observation_date + 7 days
#
# Event on observation date itself does NOT count.
# ---------------------------------------------------------

training_base["landslide_occurred_next_7d"] = 0
training_base["inventory_event_count_in_window"] = 0
training_base["inventory_event_ids_in_window"] = ""


for idx, row in training_base.iterrows():

    matching_events = event_lookup[
        (event_lookup["cell_id"] == row["cell_id"])
        &
        (
            event_lookup["event_date"]
            >= row["target_window_start"]
        )
        &
        (
            event_lookup["event_date"]
            <= row["target_window_end"]
        )
    ]

    if not matching_events.empty:

        training_base.at[
            idx,
            "landslide_occurred_next_7d"
        ] = 1

        training_base.at[
            idx,
            "inventory_event_count_in_window"
        ] = int(
            matching_events["inventory_event_count"].sum()
        )

        training_base.at[
            idx,
            "inventory_event_ids_in_window"
        ] = ",".join(
            matching_events["inventory_event_ids"].tolist()
        )


# ---------------------------------------------------------
# Label basis
# ---------------------------------------------------------

training_base["label_basis"] = training_base[
    "landslide_occurred_next_7d"
].apply(
    lambda x:
        "inventory_positive"
        if x == 1
        else "inventory_negative_control"
)


# ---------------------------------------------------------
# Storm cluster metadata
#
# Remal is explicitly grouped because the eight records
# on 2024-05-28 belong to the same event.
# ---------------------------------------------------------

training_base["storm_cluster_id"] = ""

remal_start = pd.Timestamp("2024-05-28")
remal_end = pd.Timestamp("2024-05-28")

remal_mask = (
    (training_base["target_window_start"] <= remal_end)
    &
    (training_base["target_window_end"] >= remal_start)
)

training_base.loc[
    remal_mask,
    "storm_cluster_id"
] = "cyclone_remal_2024_05_28"


# ---------------------------------------------------------
# Cell / storm split metadata
# ---------------------------------------------------------

training_base["split_group_cell"] = training_base["cell_id"]

training_base["split_group_storm"] = (
    training_base["storm_cluster_id"]
    .replace("", pd.NA)
)


# ---------------------------------------------------------
# Source / feature metadata
#
# Environmental features will be added later.
# ---------------------------------------------------------

training_base["feature_available_through"] = (
    training_base["observation_date_ist"]
)


# ---------------------------------------------------------
# Select final columns
# ---------------------------------------------------------

training_base = training_base[
    [
        "observation_date_ist",
        "cell_id",
        "cell_latitude_center",
        "cell_longitude_center",
        "cell_type",

        "target_window_start",
        "target_window_end",

        "landslide_occurred_next_7d",

        "label_basis",
        "inventory_event_ids_in_window",
        "inventory_event_count_in_window",

        "storm_cluster_id",

        "split_group_cell",
        "split_group_storm",

        "feature_available_through"
    ]
].copy()


# ---------------------------------------------------------
# Sort
# ---------------------------------------------------------

training_base = training_base.sort_values(
    [
        "observation_date_ist",
        "cell_id"
    ]
).reset_index(drop=True)


# ---------------------------------------------------------
# Save
# ---------------------------------------------------------

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)

training_base.to_csv(
    OUTPUT_FILE,
    index=False
)


# ---------------------------------------------------------
# Summary
# ---------------------------------------------------------

positive_count = int(
    training_base["landslide_occurred_next_7d"].sum()
)

negative_count = len(training_base) - positive_count

print()
print("=" * 60)
print("TRAINING BASE TABLE CREATED")
print("=" * 60)

print(f"Rows:             {len(training_base)}")
print(f"Positive rows:    {positive_count}")
print(f"Negative rows:    {negative_count}")

print()
print("Rows by cell:")
print(
    training_base.groupby(
        ["cell_id", "cell_type"]
    ).size()
)

print()
print("Positive rows by cell:")
print(
    training_base[
        training_base["landslide_occurred_next_7d"] == 1
    ]
    .groupby("cell_id")
    .size()
)

print()
print(f"Saved to:")
print(OUTPUT_FILE)