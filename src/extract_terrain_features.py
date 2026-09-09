from pathlib import Path

import numpy as np
import pandas as pd
import rasterio
from rasterio.windows import from_bounds


# ============================================================
# PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]

DEM_PATH = PROJECT_ROOT / "data" / "raw" / "dem" / "aizawl_dem.tif"

TRAINING_FEATURES_PATH = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "landslide_training_features.csv"
)

OUTPUT_TERRAIN_PATH = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "terrain_features.csv"
)

OUTPUT_FINAL_PATH = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "landslide_training_features.csv"
)


# ============================================================
# SETTINGS
# ============================================================

# Your IMERG cells are 0.1° × 0.1°
CELL_SIZE = 0.1

# The 15-cell study area:
LAT_MIN = 23.55
LAT_MAX = 24.15
LON_MIN = 92.50
LON_MAX = 92.85


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def calculate_slope_degrees(elevation, transform):
    """
    Calculate slope in degrees from a DEM.

    Uses the DEM's spatial resolution to estimate
    elevation gradients in the x and y directions.
    """

    # Pixel size in degrees
    pixel_width = abs(transform.a)
    pixel_height = abs(transform.e)

    # Approximate metres per degree around Aizawl
    mean_lat = 23.85

    meters_per_degree_lat = 111_320
    meters_per_degree_lon = (
        111_320 * np.cos(np.radians(mean_lat))
    )

    dx = pixel_width * meters_per_degree_lon
    dy = pixel_height * meters_per_degree_lat

    # Gradient of elevation
    dz_dy, dz_dx = np.gradient(
        elevation.astype(float),
        dy,
        dx
    )

    # Slope angle
    slope_radians = np.arctan(
        np.sqrt(dz_dx ** 2 + dz_dy ** 2)
    )

    slope_degrees = np.degrees(slope_radians)

    return slope_degrees


def get_cell_bounds(cell_id):
    """
    Convert an IMERG cell ID such as:

        IMERG_r1137_c2727

    into its 0.1° geographic bounds.
    """

    parts = cell_id.split("_")

    row = int(parts[1][1:])
    column = int(parts[2][1:])

    south = -90.0 + row * CELL_SIZE
    west = -180.0 + column * CELL_SIZE

    north = south + CELL_SIZE
    east = west + CELL_SIZE

    return south, west, north, east


# ============================================================
# MAIN
# ============================================================

print("=" * 70)
print("EXTRACTING ELEVATION + SLOPE FEATURES")
print("=" * 70)


# ------------------------------------------------------------
# 1. Check files
# ------------------------------------------------------------

print("\n[1/5] Checking input files...")

if not DEM_PATH.exists():
    raise FileNotFoundError(
        f"\nDEM not found:\n{DEM_PATH}\n\n"
        "Download your DEM GeoTIFF and save it with this filename:\n"
        "aizawl_dem.tif"
    )

if not TRAINING_FEATURES_PATH.exists():
    raise FileNotFoundError(
        f"Training feature table not found:\n"
        f"{TRAINING_FEATURES_PATH}"
    )

print("  DEM found.")
print("  Training feature table found.")


# ------------------------------------------------------------
# 2. Load training table
# ------------------------------------------------------------

print("\n[2/5] Loading training feature table...")

df = pd.read_csv(TRAINING_FEATURES_PATH)

required_columns = [
    "cell_id",
    "cell_latitude_center",
    "cell_longitude_center"
]

missing = [
    col for col in required_columns
    if col not in df.columns
]

if missing:
    raise ValueError(
        f"Missing required columns: {missing}"
    )

cells = (
    df[
        [
            "cell_id",
            "cell_latitude_center",
            "cell_longitude_center"
        ]
    ]
    .drop_duplicates()
    .sort_values("cell_id")
    .reset_index(drop=True)
)

print(f"  Training rows: {len(df):,}")
print(f"  Unique IMERG cells: {len(cells)}")


# ------------------------------------------------------------
# 3. Open DEM
# ------------------------------------------------------------

print("\n[3/5] Opening DEM...")

with rasterio.open(DEM_PATH) as src:

    print(f"  CRS: {src.crs}")
    print(f"  Resolution: {src.res}")
    print(f"  Size: {src.width} × {src.height}")
    print(f"  NoData: {src.nodata}")

    # Check coordinate system
    if src.crs is None:
        raise ValueError("DEM has no CRS information.")

    if src.crs.to_epsg() != 4326:
        print(
            "  DEM is not EPSG:4326. "
            "Rasterio will transform cell bounds."
        )

    results = []

    # --------------------------------------------------------
    # 4. Extract terrain features for every IMERG cell
    # --------------------------------------------------------

    print("\n[4/5] Calculating elevation + slope...")

    for _, cell in cells.iterrows():

        cell_id = cell["cell_id"]

        south, west, north, east = get_cell_bounds(cell_id)

        # Geographic bounds are WGS84
        left, bottom, right, top = (
            west,
            south,
            east,
            north
        )

        # If DEM is WGS84, directly create the window.
        if src.crs.to_epsg() == 4326:

            window = from_bounds(
                left,
                bottom,
                right,
                top,
                transform=src.transform
            )

        else:

            # Transform geographic bounds to DEM CRS
            from rasterio.warp import transform_bounds

            left, bottom, right, top = transform_bounds(
                "EPSG:4326",
                src.crs,
                left,
                bottom,
                right,
                top
            )

            window = from_bounds(
                left,
                bottom,
                right,
                top,
                transform=src.transform
            )

        # Read DEM pixels
        elevation = src.read(
            1,
            window=window,
            masked=True
        )

        # Need enough pixels for a meaningful slope calculation
        if elevation.size < 9:
            print(
                f"  WARNING: {cell_id} has too few DEM pixels."
            )

            results.append({
                "cell_id": cell_id,
                "elevation_m": np.nan,
                "slope_degrees": np.nan
            })

            continue

        # Convert masked array to NaN
        elevation_data = elevation.astype(float).filled(np.nan)

        # Mean elevation
        elevation_m = np.nanmean(elevation_data)

        # Slope
        slope = calculate_slope_degrees(
            elevation_data,
            src.window_transform(window)
        )

        slope_degrees = np.nanmean(slope)

        results.append({
            "cell_id": cell_id,
            "elevation_m": round(float(elevation_m), 2),
            "slope_degrees": round(float(slope_degrees), 2)
        })

        print(
            f"  {cell_id}: "
            f"elevation={elevation_m:.2f} m, "
            f"slope={slope_degrees:.2f}°"
        )


# ------------------------------------------------------------
# 5. Save + join
# ------------------------------------------------------------

terrain = pd.DataFrame(results)

print("\n[5/5] Validating terrain features...")

print(f"  Terrain rows: {len(terrain)}")
print(
    f"  Missing elevation: "
    f"{terrain['elevation_m'].isna().sum()}"
)
print(
    f"  Missing slope: "
    f"{terrain['slope_degrees'].isna().sum()}"
)

if len(terrain) != len(cells):
    raise ValueError(
        "Terrain table does not contain exactly one row per cell."
    )

if terrain["elevation_m"].isna().any():
    raise ValueError(
        "Some cells have missing elevation values."
    )

if terrain["slope_degrees"].isna().any():
    raise ValueError(
        "Some cells have missing slope values."
    )


# Save terrain-only table
terrain.to_csv(
    OUTPUT_TERRAIN_PATH,
    index=False
)

print(
    f"\n  Saved terrain table to:\n"
    f"  {OUTPUT_TERRAIN_PATH}"
)


# ------------------------------------------------------------
# Join to training table
# ------------------------------------------------------------

print("\nJoining terrain features to training table...")

original_rows = len(df)

df = df.drop(
    columns=["elevation_m", "slope_degrees"],
    errors="ignore"
)

df = df.merge(
    terrain,
    on="cell_id",
    how="left",
    validate="many_to_one"
)

if len(df) != original_rows:
    raise ValueError(
        "Row count changed after terrain join."
    )

if df["elevation_m"].isna().any():
    raise ValueError(
        "Missing elevation after join."
    )

if df["slope_degrees"].isna().any():
    raise ValueError(
        "Missing slope after join."
    )


df.to_csv(
    OUTPUT_FINAL_PATH,
    index=False
)


# ============================================================
# FINAL REPORT
# ============================================================

print("\n" + "=" * 70)
print("SUCCESS")
print("=" * 70)

print(f"\nTraining rows: {len(df):,}")
print(f"Cells: {df['cell_id'].nunique()}")

print("\nTerrain ranges:")

print(
    f"  Elevation: "
    f"{df['elevation_m'].min():.2f} → "
    f"{df['elevation_m'].max():.2f} m"
)

print(
    f"  Slope: "
    f"{df['slope_degrees'].min():.2f} → "
    f"{df['slope_degrees'].max():.2f}°"
)

print("\nFeatures now available:")

for column in [
    "rainfall_24h_mm",
    "rainfall_7d_mm",
    "historical_landslide_count_5y",
    "elevation_m",
    "slope_degrees"
]:
    print(f"  ✓ {column}")

print(
    f"\nUpdated training table:\n"
    f"{OUTPUT_FINAL_PATH}"
)