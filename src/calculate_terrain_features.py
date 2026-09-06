from pathlib import Path
import math

import numpy as np
import pandas as pd
import rasterio
from rasterio.merge import merge
from rasterio.warp import (
    calculate_default_transform,
    reproject,
    Resampling,
)
from rasterio.windows import from_bounds


# ============================================================
# PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]

DEM_DIR = PROJECT_ROOT / "data" / "raw" / "dem"
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"

DEM_FILES = [
    DEM_DIR / "N23_E092.tif",
    DEM_DIR / "N24_E092.tif",
]

TRAINING_FILE = PROCESSED_DIR / "landslide_training_features.csv"

TERRAIN_OUTPUT = PROCESSED_DIR / "terrain_features.csv"
FINAL_OUTPUT = PROCESSED_DIR / "landslide_training_features.csv"


# ============================================================
# IMERG CELL HELPERS
# ============================================================

def cell_bounds(cell_id):
    """
    Convert IMERG cell ID into geographic bounds.

    Example:
        IMERG_r1137_c2727

    Returns:
        west, south, east, north
    """

    parts = cell_id.split("_")

    row = int(parts[1][1:])
    col = int(parts[2][1:])

    south = -90.0 + row * 0.1
    west = -180.0 + col * 0.1

    north = south + 0.1
    east = west + 0.1

    return west, south, east, north


# ============================================================
# LOAD + MOSAIC DEM
# ============================================================

print("=" * 70)
print("EXTRACTING ELEVATION + SLOPE FEATURES")
print("=" * 70)

print("\nChecking DEM files...")

for dem_file in DEM_FILES:
    if not dem_file.exists():
        raise FileNotFoundError(
            f"DEM file not found:\n{dem_file}"
        )

    print(f"✓ {dem_file.name}")


print("\nOpening DEM tiles...")

sources = []

for dem_file in DEM_FILES:
    src = rasterio.open(dem_file)
    sources.append(src)

    print(
        f"{dem_file.name}: "
        f"{src.width} x {src.height}, "
        f"CRS={src.crs}, "
        f"resolution={src.res}"
    )


print("\nMosaicking DEM tiles...")

mosaic, mosaic_transform = merge(sources)

source_crs = sources[0].crs
source_nodata = sources[0].nodata

for src in sources:
    src.close()

print(f"✓ Mosaic created")
print(f"  Shape: {mosaic.shape}")
print(f"  CRS:   {source_crs}")
print(f"  NoData: {source_nodata}")


# ============================================================
# PREPARE DEM
# ============================================================

dem = mosaic[0].astype(np.float32)

if source_nodata is not None:
    dem[dem == source_nodata] = np.nan

# Some DEM products use very large values for missing data.
dem[dem < -100] = np.nan
dem[dem > 10000] = np.nan

print("\nDEM statistics:")

valid_dem = dem[np.isfinite(dem)]

print(f"  Minimum elevation: {valid_dem.min():.2f} m")
print(f"  Maximum elevation: {valid_dem.max():.2f} m")
print(f"  Mean elevation:    {valid_dem.mean():.2f} m")


# ============================================================
# REPROJECT TO UTM 46N
# ============================================================

print("\nReprojecting DEM to UTM Zone 46N...")

TARGET_CRS = "EPSG:32646"

height, width = dem.shape

transform, new_width, new_height = calculate_default_transform(
    source_crs,
    TARGET_CRS,
    width,
    height,
    *rasterio.transform.array_bounds(
        height,
        width,
        mosaic_transform
    ),
    resolution=90
)

dem_utm = np.full(
    (new_height, new_width),
    np.nan,
    dtype=np.float32
)

reproject(
    source=dem,
    destination=dem_utm,
    src_transform=mosaic_transform,
    src_crs=source_crs,
    dst_transform=transform,
    dst_crs=TARGET_CRS,
    src_nodata=np.nan,
    dst_nodata=np.nan,
    resampling=Resampling.bilinear,
)

print("✓ Reprojection complete")
print(f"  CRS: {TARGET_CRS}")
print(f"  Shape: {dem_utm.shape}")
print(f"  Pixel size: {transform.a:.2f} m")


# ============================================================
# CALCULATE SLOPE
# ============================================================

print("\nCalculating terrain slope...")

pixel_size_x = abs(transform.a)
pixel_size_y = abs(transform.e)

# Gradient in metres/metre
gradient_y, gradient_x = np.gradient(
    dem_utm,
    pixel_size_y,
    pixel_size_x
)

# Slope angle:
#
# slope = arctan(sqrt(dx² + dy²))
#
slope_radians = np.arctan(
    np.sqrt(
        gradient_x ** 2 +
        gradient_y ** 2
    )
)

slope_degrees = np.degrees(slope_radians)

# Remove invalid slope values
slope_degrees[~np.isfinite(dem_utm)] = np.nan

valid_slope = slope_degrees[np.isfinite(slope_degrees)]

print("✓ Slope calculated")

print(f"  Minimum slope: {valid_slope.min():.2f}°")
print(f"  Maximum slope: {valid_slope.max():.2f}°")
print(f"  Mean slope:    {valid_slope.mean():.2f}°")


# ============================================================
# EXTRACT 15 IMERG CELLS
# ============================================================

print("\nLoading training grid...")

training = pd.read_csv(TRAINING_FILE)

required_columns = [
    "cell_id",
    "cell_latitude_center",
    "cell_longitude_center",
]

missing = [
    col for col in required_columns
    if col not in training.columns
]

if missing:
    raise ValueError(
        f"Training file is missing columns: {missing}"
    )

cells = (
    training[
        [
            "cell_id",
            "cell_latitude_center",
            "cell_longitude_center",
        ]
    ]
    .drop_duplicates()
    .sort_values("cell_id")
    .reset_index(drop=True)
)

print(f"✓ Found {len(cells)} unique IMERG cells")


# ============================================================
# CELL FEATURE EXTRACTION
# ============================================================

terrain_records = []

print("\nExtracting terrain features for each cell...")

for _, row in cells.iterrows():

    cell_id = row["cell_id"]

    west, south, east, north = cell_bounds(cell_id)

    # Convert geographic bounds to the DEM's projected CRS.
    from rasterio.warp import transform_bounds

    left, bottom, right, top = transform_bounds(
        "EPSG:4326",
        TARGET_CRS,
        west,
        south,
        east,
        north,
    )

    window = from_bounds(
        left,
        bottom,
        right,
        top,
        transform=transform,
    )

    # Convert floating window offsets to safe integer bounds.
    row_start = max(0, math.floor(window.row_off))
    row_stop = min(
        dem_utm.shape[0],
        math.ceil(window.row_off + window.height)
    )

    col_start = max(0, math.floor(window.col_off))
    col_stop = min(
        dem_utm.shape[1],
        math.ceil(window.col_off + window.width)
    )

    if row_start >= row_stop or col_start >= col_stop:
        print(f"WARNING: No DEM pixels found for {cell_id}")

        terrain_records.append({
            "cell_id": cell_id,
            "elevation_m": np.nan,
            "slope_degrees": np.nan,
        })

        continue

    elevation_subset = dem_utm[
        row_start:row_stop,
        col_start:col_stop
    ]

    slope_subset = slope_degrees[
        row_start:row_stop,
        col_start:col_stop
    ]

    valid_elevation = elevation_subset[
        np.isfinite(elevation_subset)
    ]

    valid_slope = slope_subset[
        np.isfinite(slope_subset)
    ]

    if len(valid_elevation) == 0:
        mean_elevation = np.nan
    else:
        mean_elevation = float(
            np.mean(valid_elevation)
        )

    if len(valid_slope) == 0:
        mean_slope = np.nan
    else:
        mean_slope = float(
            np.mean(valid_slope)
        )

    terrain_records.append({
        "cell_id": cell_id,
        "cell_latitude_center": row["cell_latitude_center"],
        "cell_longitude_center": row["cell_longitude_center"],
        "elevation_m": mean_elevation,
        "slope_degrees": mean_slope,
    })

    print(
        f"  {cell_id}: "
        f"elevation={mean_elevation:.1f} m, "
        f"slope={mean_slope:.2f}°"
    )


# ============================================================
# SAVE TERRAIN FEATURES
# ============================================================

terrain = pd.DataFrame(terrain_records)

terrain.to_csv(
    TERRAIN_OUTPUT,
    index=False
)

print("\n✓ Terrain features saved:")
print(f"  {TERRAIN_OUTPUT}")


# ============================================================
# MERGE INTO TRAINING TABLE
# ============================================================

print("\nAdding terrain features to training table...")

training = training.drop(
    columns=[
        "elevation_m",
        "slope_degrees",
    ],
    errors="ignore"
)

training = training.merge(
    terrain[
        [
            "cell_id",
            "elevation_m",
            "slope_degrees",
        ]
    ],
    on="cell_id",
    how="left",
    validate="many_to_one",
)


# ============================================================
# VALIDATION
# ============================================================

if len(training) != len(
    pd.read_csv(TRAINING_FILE)
):
    raise RuntimeError(
        "ERROR: Row count changed during terrain merge!"
    )

if training["elevation_m"].isna().any():
    print(
        "\nWARNING: Some rows have missing elevation."
    )

if training["slope_degrees"].isna().any():
    print(
        "WARNING: Some rows have missing slope."
    )

print("\nTerrain feature summary:")

print(
    training[
        [
            "elevation_m",
            "slope_degrees",
        ]
    ].describe()
)


# ============================================================
# SAVE FINAL TRAINING TABLE
# ============================================================

training.to_csv(
    FINAL_OUTPUT,
    index=False
)

print("\n" + "=" * 70)
print("TERRAIN EXTRACTION COMPLETE")
print("=" * 70)

print(f"\nFinal training table:")
print(f"  {FINAL_OUTPUT}")

print(f"\nRows: {len(training):,}")
print(f"Cells: {training['cell_id'].nunique()}")

print("\nNew ML features:")
print("  ✓ elevation_m")
print("  ✓ slope_degrees")

print("\nNext feature:")
print("  → soil_moisture_m3_m3")