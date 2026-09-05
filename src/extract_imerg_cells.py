from pathlib import Path

import pandas as pd
import rasterio


# -----------------------------------
# 1. Project paths
# -----------------------------------

project_root = Path(__file__).resolve().parent.parent

tif_file = (
    project_root
    / "data"
    / "raw"
    / "imerg"
    / "20240528"
    / "3B-DAY-GIS.MS.MRG.3IMERG.20240528-S000000-E235959.4440.V07B.total.accum.tif"
)


# -----------------------------------
# 2. Our 15 IMERG study-area cells
# -----------------------------------

cells = [
    ("IMERG_r1136_c2725", 23.65, 92.55),
    ("IMERG_r1136_c2726", 23.65, 92.65),
    ("IMERG_r1136_c2727", 23.65, 92.75),

    ("IMERG_r1137_c2725", 23.75, 92.55),
    ("IMERG_r1137_c2726", 23.75, 92.65),
    ("IMERG_r1137_c2727", 23.75, 92.75),

    ("IMERG_r1138_c2725", 23.85, 92.55),
    ("IMERG_r1138_c2726", 23.85, 92.65),
    ("IMERG_r1138_c2727", 23.85, 92.75),

    ("IMERG_r1139_c2725", 23.95, 92.55),
    ("IMERG_r1139_c2726", 23.95, 92.65),
    ("IMERG_r1139_c2727", 23.95, 92.75),

    ("IMERG_r1140_c2725", 24.05, 92.55),
    ("IMERG_r1140_c2726", 24.05, 92.65),
    ("IMERG_r1140_c2727", 24.05, 92.75),
]


# -----------------------------------
# 3. Extract raster values
# -----------------------------------

rows = []

with rasterio.open(tif_file) as src:

    for cell_id, lat, lon in cells:

        # Convert geographic coordinate
        # to raster row/column.
        row, col = src.index(lon, lat)

        raw_value = src.read(
            1,
            window=((row, row + 1), (col, col + 1))
        )[0, 0]

        # IMERG GIS precipitation scaling:
        # stored value / 10 = mm
        rainfall_mm = float(raw_value) / 10.0

        rows.append({
            "date": "2024-05-28",
            "cell_id": cell_id,
            "cell_latitude_center": lat,
            "cell_longitude_center": lon,
            "raster_row": row,
            "raster_column": col,
            "raw_value": int(raw_value),
            "rainfall_mm": rainfall_mm,
        })


# -----------------------------------
# 4. Create DataFrame
# -----------------------------------

df = pd.DataFrame(rows)


# -----------------------------------
# 5. Print results
# -----------------------------------

print()
print("IMERG rainfall extraction")
print("=========================")
print()

print(df.to_string(index=False))

print()
print("Rainfall statistics:")
print(df["rainfall_mm"].describe())


# -----------------------------------
# 6. Save
# -----------------------------------

output_dir = project_root / "data" / "processed"
output_dir.mkdir(parents=True, exist_ok=True)

output_file = output_dir / "imerg_20240528_aizawl_cells.csv"

df.to_csv(output_file, index=False)

print()
print("Saved to:")
print(output_file)