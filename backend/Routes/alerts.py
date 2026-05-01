from fastapi import APIRouter
from src.Database.db import get_connection

router = APIRouter()

@router.get("/alerts/recent")
def get_alerts(limit: int = 10):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM alerts ORDER BY timestamp DESC LIMIT ?", (limit,))
    rows = cursor.fetchall()
    alerts = [dict(r) for r in rows]
    conn.close()
    return {"alerts": alerts}
