import boto3
from botocore import UNSIGNED
from botocore.config import Config

BUCKET = "copernicus-dem-90m"

s3 = boto3.client(
    "s3",
    config=Config(signature_version=UNSIGNED),
    region_name="eu-central-1"
)

prefixes = [
    "Copernicus_DSM_COG_30_N23_00_E092_00_DEM/",
    "Copernicus_DSM_COG_30_N24_00_E092_00_DEM/",
]

for prefix in prefixes:
    print("=" * 70)
    print(f"Searching: {prefix}")
    print("=" * 70)

    response = s3.list_objects_v2(
        Bucket=BUCKET,
        Prefix=prefix,
        MaxKeys=20
    )

    if "Contents" not in response:
        print("NO FILES FOUND")
    else:
        for item in response["Contents"]:
            if item["Key"].endswith("_DEM.tif"):
                print("\nDEM FILE FOUND:")
                print(item["Key"])