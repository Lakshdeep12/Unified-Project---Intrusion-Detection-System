import os

BASE_PATH = os.environ.get(
    "MODELS_DIR",
    os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "Models")
)

PATHS = {
    "scaler": os.path.join(BASE_PATH, "Scaler"),
    "supervised": os.path.join(BASE_PATH, "Supervisedrf"),
    "unsupervised": os.path.join(BASE_PATH, "Unsupervised")
}

# Optional: define expected features (important for IDS)
FEATURE_COLUMNS = [
    "Protocol",
    "Fwd IAT Total",
    "Flow IAT Mean",
    "Flow IAT Max",
    "Flow IAT Min",
    "PSH Flag Count",
    "FIN Flag Count",
    "ACK Flag Count",
    "SYN Flag Count",
    "Average Packet Size",
    "Flow Duration",
    "Total Fwd Packets",
    "Total Backward Packets",
    "Flow Bytes/s",
    "Flow Packets/s",
]

# Optional: threshold for anomaly detection
ANOMALY_THRESHOLD = 0.5
