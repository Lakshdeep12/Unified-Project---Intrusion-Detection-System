from fastapi import APIRouter
from src.Database.db import get_connection
from pydantic import BaseModel

router = APIRouter()

class ConfigUpdate(BaseModel):
    attack_threshold: float
    mode: str
    replay_speed: int

@router.get("/config")
def get_config():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT attack_threshold, mode, replay_speed FROM system_config WHERE id = 1")
    row = cursor.fetchone()
    conn.close()
    return dict(row)

@router.post("/config/update")
def update_config(conf: ConfigUpdate):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE system_config SET attack_threshold=?, mode=?, replay_speed=? WHERE id=1",
                   (conf.attack_threshold, conf.mode, conf.replay_speed))
    conn.commit()
    conn.close()
    return {"status": "success"}
