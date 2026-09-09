from pathlib import Path

import joblib
import pandas as pd

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    precision_score,
    recall_score,
    f1_score,
)
from sklearn.model_selection import GroupShuffleSplit


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_FILE = (
    BASE_DIR
    / "data"
    / "processed"
    / "landslide_training_features.csv"
)

MODEL_DIR = BASE_DIR / "models"

MODEL_FILE = MODEL_DIR / "landslide_rf.joblib"

FEATURE_FILE = MODEL_DIR / "landslide_rf_features.joblib"


# ============================================================
# ML FEATURES
# ============================================================

FEATURE_COLUMNS = [
    "rainfall_24h_mm",
    "rainfall_7d_mm",
    "elevation_m",
    "slope_degrees",
    "historical_landslide_count_5y",
]

TARGET_COLUMN = "landslide_occurred_next_7d"


# ============================================================
# START
# ============================================================

print("=" * 70)
print("RANDOM FOREST LANDSLIDE MODEL")
print("=" * 70)


# ============================================================
# 1. LOAD DATA
# ============================================================

print("\n[1/7] Loading training data...")

if not DATA_FILE.exists():
    raise FileNotFoundError(
        f"Training file not found:\n{DATA_FILE}"
    )

df = pd.read_csv(DATA_FILE)

df["observation_date_ist"] = pd.to_datetime(
    df["observation_date_ist"]
)

print(f"  Total rows loaded: {len(df):,}")


# ============================================================
# 2. CHECK COLUMNS
# ============================================================

print("\n[2/7] Checking required columns...")

required_columns = (
    FEATURE_COLUMNS
    + [
        TARGET_COLUMN,
        "cell_id",
        "observation_date_ist",
    ]
)

missing_columns = [
    column
    for column in required_columns
    if column not in df.columns
]

if missing_columns:
    raise ValueError(
        "Missing required columns:\n"
        + "\n".join(
            f"  - {column}"
            for column in missing_columns
        )
    )

print("  ✓ All required columns found.")


# ============================================================
# 3. KEEP COMPLETE ML SAMPLES
# ============================================================

print("\n[3/7] Selecting complete ML samples...")

before = len(df)

model_df = df.dropna(
    subset=FEATURE_COLUMNS + [TARGET_COLUMN]
).copy()

after = len(model_df)

print(
    f"  Rows before filtering: {before:,}"
)

print(
    f"  Rows with complete features: {after:,}"
)

print(
    f"  Rows removed: {before - after:,}"
)

positive_count = int(
    model_df[TARGET_COLUMN].sum()
)

negative_count = int(
    (model_df[TARGET_COLUMN] == 0).sum()
)

print(
    f"  Positive samples: {positive_count}"
)

print(
    f"  Negative samples: {negative_count}"
)

if positive_count < 2:
    raise ValueError(
        "Not enough positive samples to train the model."
    )


# ============================================================
# 4. CREATE EVENT-AWARE GROUPS
# ============================================================

print("\n[4/7] Creating leakage-aware groups...")

# For positive observations:
# group all observations belonging to the same target
# event date + cell together.
#
# For negative observations:
# group by cell + observation date.
#
# This prevents rows from the same event window from
# being randomly split between train and test.

model_df["split_group"] = (
    model_df["cell_id"].astype(str)
    + "_"
    + model_df[TARGET_COLUMN].astype(str)
    + "_"
    + model_df["observation_date_ist"]
        .dt.strftime("%Y-%m-%d")
)

print(
    f"  Unique groups: "
    f"{model_df['split_group'].nunique()}"
)


# ============================================================
# 5. TRAIN / TEST SPLIT
# ============================================================

print("\n[5/7] Creating train/test split...")

X = model_df[FEATURE_COLUMNS]

y = model_df[TARGET_COLUMN].astype(int)

groups = model_df["split_group"]

splitter = GroupShuffleSplit(
    n_splits=1,
    test_size=0.25,
    random_state=42,
)

train_indices, test_indices = next(
    splitter.split(
        X,
        y,
        groups=groups
    )
)

X_train = X.iloc[train_indices]
X_test = X.iloc[test_indices]

y_train = y.iloc[train_indices]
y_test = y.iloc[test_indices]


print(
    f"  Training rows: {len(X_train):,}"
)

print(
    f"  Testing rows:  {len(X_test):,}"
)

print(
    f"  Training positives: {int(y_train.sum())}"
)

print(
    f"  Testing positives:  {int(y_test.sum())}"
)

if y_train.sum() == 0:
    raise ValueError(
        "Training set contains no positive samples. "
        "Try another random_state."
    )

if y_test.sum() == 0:
    raise ValueError(
        "Test set contains no positive samples. "
        "Try another random_state."
    )


# ============================================================
# 6. TRAIN RANDOM FOREST
# ============================================================

print("\n[6/7] Training Random Forest...")

model = RandomForestClassifier(
    n_estimators=300,
    class_weight="balanced",
    random_state=42,
    n_jobs=-1,
    min_samples_leaf=2,
)

model.fit(
    X_train,
    y_train
)

print("  ✓ Model training completed.")


# ============================================================
# 7. EVALUATE
# ============================================================

print("\n[7/7] Evaluating model...")

y_pred = model.predict(X_test)

precision = precision_score(
    y_test,
    y_pred,
    zero_division=0
)

recall = recall_score(
    y_test,
    y_pred,
    zero_division=0
)

f1 = f1_score(
    y_test,
    y_pred,
    zero_division=0
)

print("\n" + "=" * 70)
print("MODEL PERFORMANCE")
print("=" * 70)

print(
    f"\nPrecision: {precision:.3f}"
)

print(
    f"Recall:    {recall:.3f}"
)

print(
    f"F1 Score:  {f1:.3f}"
)

print("\nClassification Report:")

print(
    classification_report(
        y_test,
        y_pred,
        zero_division=0
    )
)

print("Confusion Matrix:")

print(
    confusion_matrix(
        y_test,
        y_pred
    )
)


# ============================================================
# FEATURE IMPORTANCE
# ============================================================

print("\nFeature importance:")

importance = pd.Series(
    model.feature_importances_,
    index=FEATURE_COLUMNS
).sort_values(
    ascending=False
)

for feature, value in importance.items():

    print(
        f"  {feature:<35} "
        f"{value:.4f}"
    )


# ============================================================
# SAVE MODEL
# ============================================================

MODEL_DIR.mkdir(
    parents=True,
    exist_ok=True
)

joblib.dump(
    model,
    MODEL_FILE
)

joblib.dump(
    FEATURE_COLUMNS,
    FEATURE_FILE
)


# ============================================================
# FINAL
# ============================================================

print("\n" + "=" * 70)
print("MODEL SAVED SUCCESSFULLY")
print("=" * 70)

print(
    f"\nModel:\n{MODEL_FILE}"
)

print(
    f"\nFeature list:\n{FEATURE_FILE}"
)

print("\nFeatures used:")

for feature in FEATURE_COLUMNS:
    print(f"  ✓ {feature}")

print(
    "\nNext step: build predict_risk() for the API."
)