from pathlib import Path
import zipfile


BASE_DIR = Path(__file__).resolve().parents[1]

RAW_DIR = BASE_DIR / "data" / "raw" / "imerg"
EXTRACT_DIR = RAW_DIR / "extracted"

EXTRACT_DIR.mkdir(parents=True, exist_ok=True)


zip_files = sorted(RAW_DIR.glob("*.zip"))

print(f"Found {len(zip_files)} ZIP files.\n")


for zip_path in zip_files:

    print(f"Processing: {zip_path.name}")

    with zipfile.ZipFile(zip_path, "r") as z:

        tif_files = [
            name
            for name in z.namelist()
            if name.lower().endswith(".total.accum.tif")
        ]

        if not tif_files:
            print("  No .total.accum.tif found")
            continue

        for tif_name in tif_files:

            output_path = EXTRACT_DIR / Path(tif_name).name

            if output_path.exists():
                print(f"  Already extracted: {output_path.name}")
                continue

            print(f"  Extracting: {Path(tif_name).name}")

            with z.open(tif_name) as source:
                with open(output_path, "wb") as target:
                    target.write(source.read())

            print(f"  Saved: {output_path}")


print("\nExtraction complete.")