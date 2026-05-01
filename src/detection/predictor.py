import numpy as np
import pandas as pd
from src.detection.loader import load_all_sets
from src.detection.config import FEATURE_COLUMNS

models = None

def get_models():
    global models
    if models is None:
        models = load_all_sets()
    return models

def validate_sample(sample):
    if len(sample) != len(FEATURE_COLUMNS):
        raise ValueError(f"Expected {len(FEATURE_COLUMNS)} features, got {len(sample)}")

def predict(sample, model_key):
    validate_sample(sample)

    models = get_models()

    if model_key not in models:
        available = ", ".join(sorted(models.keys())) or "none"
        raise ValueError(f"Model '{model_key}' not found. Available models: {available}")

    bundle = models[model_key]

    scaler = bundle["scaler"]
    rf_model = bundle["rf_model"]
    unsup_model = bundle["unsupervised"]

    sample_frame = pd.DataFrame([sample], columns=FEATURE_COLUMNS)
    sample_scaled = scaler.transform(sample_frame)

    rf_pred = rf_model.predict(sample_scaled)[0]
    rf_prob = rf_model.predict_proba(sample_scaled)[0]

    unsup_pred = unsup_model.predict(sample_scaled)[0]

    return {
        "rf_prediction": int(rf_pred),
        "rf_confidence": float(max(rf_prob)),
        "unsupervised_prediction": int(unsup_pred)
    }

def decision_from_output(result):
    if result["rf_prediction"] == 1 or result["unsupervised_prediction"] == -1:
        return "ATTACK"
    return "NORMAL"

def final_decision(sample, model_key):
    result = predict(sample, model_key)
    return decision_from_output(result)
