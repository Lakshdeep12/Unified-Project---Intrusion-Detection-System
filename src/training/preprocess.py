import pandas as pd
import numpy as np
import joblib
import os

from sklearn.preprocessing import StandardScaler, LabelEncoder

# =========================
# CONFIG
# =========================
MODEL_DIR = "models"

FEATURES_KEY = [
    'Protocol',
    'Fwd IAT Total',
    'Flow IAT Mean',
    'Flow IAT Max',
    'Flow IAT Min',
    'PSH Flag Count',
    'FIN Flag Count',
    'ACK Flag Count',
    'SYN Flag Count',
    'Average Packet Size',
    'Flow Duration',
    'Total Fwd Packets',
    'Total Backward Packets',
    'Flow Bytes/s',
    'Flow Packets/s'
]

LABEL_COL = 'Label'

PROTO_MAP = {
    6: 0,    # TCP
    17: 1    # UDP
}


# =========================
# HELPERS
# =========================
def encode_protocol(value):
    if pd.isna(value):
        return 2
    return PROTO_MAP.get(value, 2)


# =========================
# MAIN PREPROCESS FUNCTION
# =========================
def preprocess_data(df, training=True):
    """
    Input: Raw dataframe
    Output: X_scaled, y
    """

    df = df.copy()

    # Clean column names
    df.columns = df.columns.str.strip()

    # Replace inf with NaN
    df.replace([np.inf, -np.inf], np.nan, inplace=True)

    # =========================
    # CHECK LABEL
    # =========================
    if LABEL_COL not in df.columns:
        raise ValueError(f"Missing label column: {LABEL_COL}")

    # =========================
    # LABEL ENCODING
    # =========================
    if training:
        le = LabelEncoder()
        y = le.fit_transform(df[LABEL_COL])
        joblib.dump(le, os.path.join(MODEL_DIR, "label_encoder.pkl"))
    else:
        le = joblib.load(os.path.join(MODEL_DIR, "label_encoder.pkl"))
        y = le.transform(df[LABEL_COL])

    # =========================
    # FEATURE SELECTION
    # =========================
    missing_cols = [col for col in FEATURES_KEY if col not in df.columns]
    if missing_cols:
        raise ValueError(f"Missing required features: {missing_cols}")

    X = df[FEATURES_KEY].copy()

    # =========================
    # HANDLE NaN
    # =========================
    X.fillna(0.0, inplace=True)

    # =========================
    # ENCODE PROTOCOL
    # =========================
    X['Protocol'] = X['Protocol'].apply(encode_protocol)

    # =========================
    # SCALING
    # =========================
    if training:
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        joblib.dump(scaler, os.path.join(MODEL_DIR, "scaler.pkl"))
    else:
        scaler = joblib.load(os.path.join(MODEL_DIR, "scaler.pkl"))
        X_scaled = scaler.transform(X)

    return X_scaled, y