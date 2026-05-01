from fastapi import APIRouter
from src.Database.db import get_connection

router = APIRouter()

@router.get("/logs")
def fetch_logs(page: int = 1, limit: int = 20):
    conn = get_connection()
    cursor = conn.cursor()
    offset = (page - 1) * limit
    cursor.execute("SELECT * FROM events ORDER BY timestamp DESC LIMIT ? OFFSET ?", (limit, offset))
    rows = cursor.fetchall()
    cursor.execute("SELECT COUNT(*) as total FROM events")
    total = cursor.fetchone()["total"]

    logs = [dict(r) for r in rows]
    total_pages = max(1, (total + limit - 1) // limit)

    conn.close()
    return {"logs": logs, "page": page, "total_pages": total_pages, "total": total}
