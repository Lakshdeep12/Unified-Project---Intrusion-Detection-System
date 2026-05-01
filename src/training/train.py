import pandas as pd
import os
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import IsolationForest, GradientBoostingClassifier, RandomForestClassifier

from training.preprocess import preprocess_data
from training.evaluate import evaluate_model
from training.config import DATASET_PATH

# =========================
# CONFIG
# =========================
MODEL_DIR = "models"


# =========================
# LOAD DATA
# =========================
def load_data():
    if not os.path.exists(DATASET_PATH):
        raise FileNotFoundError(f"Dataset not found at: {DATASET_PATH}")
    
    print(f"[INFO] Loading dataset from {DATASET_PATH}")
    df = pd.read_csv(DATASET_PATH)
    print(f"[INFO] Dataset shape: {df.shape}")
    
    return df


# =========================
# TRAIN MODELS
# =========================
def train_models(X_train, y_train):
    print("[INFO] Training models...")

    # -------------------------
    # Random Forest
    # -------------------------
    rf = RandomForestClassifier(
        n_estimators=100,
        random_state=42,
        n_jobs=-1
    )
    rf.fit(X_train, y_train)
    print("[INFO] RandomForest trained")

    # -------------------------
    # Gradient Boosting
    # -------------------------
    gb = GradientBoostingClassifier(
        n_estimators=100,
        random_state=42
    )
    gb.fit(X_train, y_train)
    print("[INFO] GradientBoosting trained")

    # -------------------------
    # Isolation Forest
    # -------------------------
    ifc = IsolationForest(
        n_estimators=100,
        random_state=42,
        contamination=0.1
    )
    ifc.fit(X_train)
    print("[INFO] IsolationForest trained")

    return rf, gb, ifc


# =========================
# SAVE MODELS
# =========================
def save_models(rf, gb, ifc):
    os.makedirs(MODEL_DIR, exist_ok=True)

    joblib.dump(rf, os.path.join(MODEL_DIR, "rf_model.pkl"))
    joblib.dump(gb, os.path.join(MODEL_DIR, "gb_model.pkl"))
    joblib.dump(ifc, os.path.join(MODEL_DIR, "iso_model.pkl"))

    print(f"[INFO] Models saved in '{MODEL_DIR}/'")


# =========================
# MAIN PIPELINE
# =========================
def main():
    # Load data
    df = load_data()

    # Preprocess (already includes scaling)
    X, y = preprocess_data(df, training=True)

    # Split
    print("[INFO] Splitting dataset...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=0.2,
        stratify=y,
        random_state=42
    )

    # Train
    rf, gb, ifc = train_models(X_train, y_train)

    # Save
    save_models(rf, gb, ifc)

    # =========================
    # EVALUATION
    # =========================
    print("\n Evaluating RandomForest...")
    evaluate_model(rf, X_test, y_test)

    print("\n Evaluating GradientBoosting...")
    evaluate_model(gb, X_test, y_test)

    # Isolation Forest evaluation fix
    print("\n Evaluating IsolationForest...")
    iso_preds = ifc.predict(X_test)

    # Convert (-1, 1) → (1 = attack, 0 = normal)
    iso_preds = [1 if p == -1 else 0 for p in iso_preds]

    from sklearn.metrics import classification_report
    print(classification_report(y_test, iso_preds))


# =========================
# ENTRY POINT
# =========================
if __name__ == "__main__":
    main()