import os
import joblib

BASE_PATH = os.environ.get("MODELS_DIR", os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'Models'))

def load_all_sets():
    data = {}

    scaler_path = os.path.join(BASE_PATH, 'Scaler')
    rf_path = os.path.join(BASE_PATH, 'Supervisedrf')
    unsup_path = os.path.join(BASE_PATH, 'Unsupervised')

    for file in os.listdir(rf_path):
        if file.endswith('-supervised_rf.joblib'):
            key = file.replace('-supervised_rf.joblib', '')
            scaler_file = f"{key}-scaler.joblib"
            unsup_file = f"{key}-unsupervised_iso.joblib"

            scaler_file_path = os.path.join(scaler_path, scaler_file)
            rf_file_path = os.path.join(rf_path, file)
            unsup_file_path = os.path.join(unsup_path, unsup_file)

            missing = [
                path for path in (scaler_file_path, rf_file_path, unsup_file_path)
                if not os.path.exists(path)
            ]
            if missing:
                raise FileNotFoundError(f"Missing model assets for {key}: {missing}")

            data[key] = {
                "rf_model": joblib.load(rf_file_path),
                "scaler": joblib.load(scaler_file_path),
                "unsupervised": joblib.load(unsup_file_path)
            }

    return data
