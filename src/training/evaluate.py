import pandas as pd
import joblib
from sklearn.metrics import classification_report, confusion_matrix
from training.preprocess import preprocess_data
from training.config import MODEL_PATH, DATASET_PATH


def load_model():
    return joblib.load(MODEL_PATH)


def load_data():
    df = pd.read_csv(DATASET_PATH)
    return df


def evaluate():
    print("[INFO] Loading model...")
    model = load_model()

    print("[INFO] Loading dataset...")
    df = load_data()

    print("[INFO] Preprocessing data...")
    X, y = preprocess_data(df, training=False)

    print("[INFO] Making predictions...")
    y_pred = model.predict(X)

    print("\n Confusion Matrix:")
    print(confusion_matrix(y, y_pred))

    print("\n Classification Report:")
    print(classification_report(y, y_pred))


if __name__ == "__main__":
    evaluate()