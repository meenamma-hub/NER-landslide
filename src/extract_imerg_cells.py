from pathlib import Path
import zipfile
import re

import pandas as pd
import rasterio


# ============================================================
# 1. PROJECT PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

RAW_IMERG_DIR = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "imerg"
)

OUTPUT_DIR = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "imerg"
)

OUTPUT_FILE = (
    OUTPUT_DIR
    / "aizawl_daily_rainfall.csv"
)

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# ============================================================
# 2. OUR 15 IMERG STUDY-AREA CELLS
# ============================================================

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


# ============================================================
# 3. FIND IMERG ZIP FILES
# ============================================================

zip_files = sorted(
    RAW_IMERG_DIR.rglob(
        "3B-DAY-GIS.MS.MRG.3IMERG.*.V07B.zip"
    )
)

if not zip_files:
    print("ERROR: No IMERG ZIP files found.")
    print(f"Checked: {RAW_IMERG_DIR}")
    raise SystemExit(1)


print()
print("IMERG batch rainfall extraction")
print("================================")
print()
print(f"ZIP files found: {len(zip_files)}")
print()


# ============================================================
# 4. EXTRACT ONE ZIP + READ 15 CELLS
# ============================================================

all_rows = []

for zip_file in zip_files:

    # --------------------------------------------------------
    # Extract date from filename
    # --------------------------------------------------------

    match = re.search(
        r"3IMERG\.(\d{8})-",
        zip_file.name
    )

    if not match:
        print(f"Skipping unrecognized filename: {zip_file.name}")
        continue

    date_string = match.group(1)

    date_formatted = (
        f"{date_string[:4]}-"
        f"{date_string[4:6]}-"
        f"{date_string[6:8]}"
    )

    print(f"Processing {date_formatted}...")


    # --------------------------------------------------------
    # Temporary extraction directory
    # --------------------------------------------------------

    extract_dir = (
        zip_file.parent
        / f"extracted_{date_string}"
    )

    extract_dir.mkdir(
        parents=True,
        exist_ok=True
    )


    # --------------------------------------------------------
    # Extract ZIP
    # --------------------------------------------------------

    with zipfile.ZipFile(zip_file, "r") as z:
        z.extractall(extract_dir)


    # --------------------------------------------------------
    # Find precipitation GeoTIFF
    # --------------------------------------------------------

    tif_files = list(
        extract_dir.rglob(
            "*.total.accum.tif"
        )
    )

    if not tif_files:
        print(
            f"  ERROR: No .total.accum.tif found "
            f"inside {zip_file.name}"
        )
        continue

    tif_file = tif_files[0]


    # --------------------------------------------------------
    # Open raster
    # --------------------------------------------------------

    with rasterio.open(tif_file) as src:

        for cell_id, lat, lon in cells:

            # Convert geographic coordinate
            # to raster row/column.
            row, col = src.index(lon, lat)

            raw_value = src.read(
                1,
                window=((row, row + 1), (col, col + 1))
            )[0, 0]


            # ------------------------------------------------
            # IMERG GIS precipitation scaling
            # stored value / 10 = mm
            # ------------------------------------------------

            rainfall_mm = float(raw_value) / 10.0


            all_rows.append({
                "date": date_formatted,
                "cell_id": cell_id,
                "cell_latitude_center": lat,
                "cell_longitude_center": lon,
                "rainfall_24h_mm": rainfall_mm,
            })


    print(
        f"  Done: {len(cells)} cells"
    )


# ============================================================
# 5. CREATE DATAFRAME
# ============================================================

if not all_rows:
    print()
    print("ERROR: No rainfall data was extracted.")
    raise SystemExit(1)


df = pd.DataFrame(all_rows)


# ============================================================
# 6. CLEAN + VALIDATE
# ============================================================

df["date"] = pd.to_datetime(
    df["date"]
)

df = (
    df
    .drop_duplicates(
        subset=["date", "cell_id"],
        keep="last"
    )
    .sort_values(
        ["date", "cell_id"]
    )
    .reset_index(drop=True)
)


# ============================================================
# 7. VALIDATION
# ============================================================

expected_rows = (
    df["date"].nunique()
    * len(cells)
)

print()
print("Validation")
print("----------")
print(f"Dates extracted: {df['date'].nunique()}")
print(
    f"Date range: "
    f"{df['date'].min().date()} "
    f"to "
    f"{df['date'].max().date()}"
)
print(f"Cells: {df['cell_id'].nunique()}")
print(f"Rows: {len(df)}")
print(f"Expected rows: {expected_rows}")


if len(df) != expected_rows:
    print()
    print(
        "WARNING: Some date × cell combinations "
        "may be missing."
    )


# ============================================================
# 8. SAVE
# ============================================================

df.to_csv(
    OUTPUT_FILE,
    index=False
)

print()
print("Rainfall statistics")
print("-------------------")
print(df["rainfall_24h_mm"].describe())


print()
print("Saved to:")
print(OUTPUT_FILE)

print()
print("DONE.")