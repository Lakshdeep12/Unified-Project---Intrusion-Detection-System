from fastapi import APIRouter
from src.Database.db import get_connection
import time

router = APIRouter()

@router.get("/live-stats")
def get_live_stats():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) as total FROM events")
    total_events = cursor.fetchone()["total"]
    cursor.execute("SELECT COUNT(*) as attacks FROM events WHERE is_attack = 1")
    total_attacks = cursor.fetchone()["attacks"]
    conn.close()
    
    normal = total_events - total_attacks
    return {
        "total_packets": total_events,
        "attacks_detected": total_attacks,
        "normal_traffic": normal,
        "latency": 0,
        "status": "Running"
    }

@router.get("/attack-rate")
def get_attack_rate():
    # Return real data grouped by time (mock fallback if DB empty)
    conn = get_connection()
    cursor = conn.cursor()
    # SQLite datetime('now', '-60 seconds') is useful here
    cursor.execute("""
        SELECT strftime('%s', timestamp) as ts, 
               SUM(CASE WHEN is_attack = 1 THEN 1 ELSE 0 END) as attacks,
               SUM(CASE WHEN is_attack = 0 THEN 1 ELSE 0 END) as normal
        FROM events 
        WHERE timestamp >= datetime('now', '-60 seconds')
        GROUP BY ts
        ORDER BY ts ASC
    """)
    rows = cursor.fetchall()
    conn.close()

    now = int(time.time())
    data = []
    
    ts_map = {int(r["ts"]): r for r in rows}
    for i in range(60):
        ts = now - (59 - i)
        if ts in ts_map:
            data.append({
                "time": ts,
                "attacks": ts_map[ts]["attacks"],
                "normal": ts_map[ts]["normal"]
            })
        else:
            data.append({
                "time": ts,
                "attacks": 0,
                "normal": 0
            })

    return {"history": data}
