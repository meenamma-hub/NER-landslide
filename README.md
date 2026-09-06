# NER-landslide

Creating MVP of our project: Predict, Prioritize, Prevent.

## ML Module

Machine learning module for landslide hazard risk prediction for the Aizawl prototype.

## ML Features

- rainfall_24h_mm
- rainfall_7d_mm
- elevation_m
- slope_degrees
- historical_landslide_count_5y

## Model

Random Forest Classifier using scikit-learn.

## Prediction

The `predict_risk()` function returns:

- risk_score
- risk_percentage
- risk_level

Risk levels:

- LOW
- MODERATE
- HIGH
- CRITICAL

## Current Prototype

The current trained model is an Aizawl-area prototype and should not be interpreted as a calibrated real-world probability model.