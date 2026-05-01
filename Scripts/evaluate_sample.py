import argparse
import os
import sys
from glob import glob

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

import joblib
import pandas as pd
from sklearn.metrics import accuracy_score, confusion_matrix, precision_recall_fscore_support

from src.detection.config import FEATURE_COLUMNS


def evaluate_dataset(dataset_path, model_key, sample_size):
    try:
        df = pd.read_csv(dataset_path)
    except UnicodeDecodeError:
        df = pd.read_csv(dataset_path, encoding="latin1")
    df.columns = df.columns.str.strip()
    missing = [column for column in FEATURE_COLUMNS + ["Label"] if column not in df.columns]
    if missing:
        return {
            "dataset": dataset_path,
            "status": "skipped",
            "reason": f"Missing columns: {missing}",
        }

    df = df.replace([float("inf"), -float("inf")], 0).fillna(0)

    binary_label = (df["Label"].str.strip() != "BENIGN").astype(int)
    grouped = df.assign(_binary_label=binary_label).groupby("_binary_label", group_keys=False)
    class_counts = binary_label.value_counts()
    usable_size = min(sample_size, int(class_counts.min()))
    if usable_size < 1 or len(class_counts) < 2:
        return {
            "dataset": dataset_path,
            "status": "skipped",
            "reason": "Dataset sample does not contain at least two classes.",
        }

    sample = grouped.sample(n=usable_size, random_state=42)

    x = sample[FEATURE_COLUMNS]
    y = sample["_binary_label"].astype(int)

    scaler = joblib.load(f"Models/Scaler/{model_key}-scaler.joblib")
    model = joblib.load(f"Models/Supervisedrf/{model_key}-supervised_rf.joblib")
    predictions = model.predict(scaler.transform(x))

    precision, recall, f1, _ = precision_recall_fscore_support(
        y,
        predictions,
        average="binary",
        zero_division=0,
    )

    return {
        "dataset": dataset_path,
        "status": "ok",
        "rows": len(sample),
        "normal": int((1 - y).sum()),
        "attacks": int(y.sum()),
        "accuracy": accuracy_score(y, predictions),
        "precision": precision,
        "recall": recall,
        "f1": f1,
        "confusion_matrix": confusion_matrix(y, predictions).tolist(),
    }


def print_result(result):
    print(f"\nDataset: {result['dataset']}")
    if result["status"] != "ok":
        print(f"Status: skipped")
        print(f"Reason: {result['reason']}")
        return

    print(f"Rows: {result['rows']}")
    print(f"Normal rows: {result['normal']}")
    print(f"Attack rows: {result['attacks']}")
    print(f"Accuracy: {result['accuracy']:.4f}")
    print(f"Precision: {result['precision']:.4f}")
    print(f"Recall: {result['recall']:.4f}")
    print(f"F1-score: {result['f1']:.4f}")
    print(f"Confusion matrix: {result['confusion_matrix']}")


def main():
    parser = argparse.ArgumentParser(description="Evaluate saved IDS models on CICIDS2017 samples.")
    parser.add_argument(
        "--dataset",
        default="DataSet/Raw DataSet/CICD2017/Friday-WorkingHours-Afternoon-DDos.pcap_ISCX.csv",
        help="CSV dataset path.",
    )
    parser.add_argument("--all-cicids", action="store_true", help="Evaluate every CICIDS2017 CSV file.")
    parser.add_argument("--model-key", default="Set-1", help="Model set key, for example Set-1.")
    parser.add_argument("--sample-size", type=int, default=5000, help="Rows per class to sample.")
    args = parser.parse_args()

    if args.all_cicids:
        pattern = os.path.join(PROJECT_ROOT, "DataSet", "Raw DataSet", "CICD2017", "*.csv")
        dataset_paths = sorted(glob(pattern))
    else:
        dataset_paths = [args.dataset]

    results = [evaluate_dataset(path, args.model_key, args.sample_size) for path in dataset_paths]
    for result in results:
        print_result(result)

    ok_results = [result for result in results if result["status"] == "ok"]
    if len(ok_results) > 1:
        print("\nMacro average across evaluated files:")
        for metric in ["accuracy", "precision", "recall", "f1"]:
            value = sum(result[metric] for result in ok_results) / len(ok_results)
            print(f"{metric.title()}: {value:.4f}")


if __name__ == "__main__":
    main()
