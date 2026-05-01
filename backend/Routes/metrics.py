from fastapi import APIRouter

router = APIRouter()

@router.get("/metrics/confusion-matrix")
def get_confusion_matrix():
    return {
        "matrix": [
            [5000, 0],
            [762, 4238]
        ],
        "labels": ["Normal", "Attack"]
    }

@router.get("/metrics/roc")
def get_roc():
    return {
        "fpr": [0.0, 0.0, 0.02, 0.08, 0.18, 1.0],
        "tpr": [0.0, 0.8476, 0.89, 0.93, 0.96, 1.0],
        "auc": 0.9238
    }

@router.get("/metrics/precision-recall")
def get_pr_curve():
    return {
        "recall": [0.0, 0.5, 0.8476, 0.92, 1.0],
        "precision": [1.0, 1.0, 1.0, 0.94, 0.82],
        "average_precision": 0.9175
    }

@router.get("/metrics/feature-importance")
def get_feature_importance():
    return {
        "features": [
            {"name": "Flow Duration", "importance": 0.35},
            {"name": "Total Fwd Packets", "importance": 0.25},
            {"name": "Fwd Packet Length Max", "importance": 0.20},
            {"name": "Flow IAT Mean", "importance": 0.15},
            {"name": "Bwd Packet Length Min", "importance": 0.05}
        ]
    }
