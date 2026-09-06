import pandas as pd

FILE = "data/processed/landslide_training_features.csv"

df = pd.read_csv(FILE)

features = [
    "rainfall_24h_mm",
    "rainfall_7d_mm",
    "elevation_m",
    "slope_degrees",
    "historical_landslide_count_5y"
]

target = "landslide_occurred_next_7d"

print("Total rows:", len(df))
print()

print("Target distribution:")
print(df[target].value_counts())
print()

print("Missing values:")
print(df[features].isna().sum())
print()

complete = df[features + [target]].dropna()

print("Complete rows:", len(complete))
print("Complete positives:", complete[target].sum())
print("Complete negatives:", (complete[target] == 0).sum())