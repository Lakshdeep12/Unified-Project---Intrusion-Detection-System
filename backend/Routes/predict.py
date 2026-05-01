from fastapi import APIRouter, HTTPException
from src.detection.predictor import decision_from_output, predict as run_prediction
from backend.Schemas.schema import PredictionRequest
from src.Database.db import get_connection
import json

router = APIRouter()

@router.post("/predict")
def make_prediction(req: PredictionRequest):
    try:
        model_output = run_prediction(req.features, req.model_key)
        result = decision_from_output(model_output)
        is_attack = 1 if result == "ATTACK" else 0
        confidence = model_output["rf_confidence"]
        
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO events (prediction, confidence, is_attack, data) VALUES (?, ?, ?, ?)",
            (result, confidence, is_attack, json.dumps(req.features)))
        conn.commit()
        
        if is_attack:
            cursor.execute(
                "INSERT INTO alerts (message, attack_type) VALUES (?, ?)",
                ("Attack detected from prediction API", "ML-Anomaly"),
            )
            conn.commit()
            
        conn.close()
        return {
            "prediction": result,
            "status": "success",
            "model_key": req.model_key,
            "details": model_output,
        }
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
