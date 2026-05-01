import os

def create_files():
    base_dir = r"d:\Unfied Project-1"
    
    # Update DB Schema
    models_path = os.path.join(base_dir, "src", "Database", "models.py")
    with open(models_path, "w") as f:
        f.write("""from src.Database.db import get_connection

def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password_hash TEXT
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS events (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        source_ip TEXT,
        dest_ip TEXT,
        prediction TEXT,
        confidence REAL,
        is_attack INTEGER,
        data TEXT
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS alerts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        message TEXT,
        source_ip TEXT,
        attack_type TEXT,
        is_read INTEGER DEFAULT 0
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS system_config (
        id INTEGER PRIMARY KEY,
        attack_threshold REAL,
        mode TEXT,
        replay_speed INTEGER
    )
    ''')
    
    cursor.execute("SELECT COUNT(*) as count FROM system_config")
    if cursor.fetchone()["count"] == 0:
        cursor.execute("INSERT INTO system_config (id, attack_threshold, mode, replay_speed) VALUES (1, 0.8, 'Hybrid', 1)")

    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_tables()
""")

    # Update backend main.py
    main_path = os.path.join(base_dir, "backend", "main.py")
    with open(main_path, "w") as f:
        f.write("""import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.Routes import auth, logs, stats, alerts, metrics, config

app = FastAPI(title="Advanced IDS API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, tags=["Authentication"])
app.include_router(logs.router, prefix="/api", tags=["Logs"])
app.include_router(stats.router, prefix="/api", tags=["Stats"])
app.include_router(alerts.router, prefix="/api", tags=["Alerts"])
app.include_router(metrics.router, prefix="/api", tags=["Metrics"])
app.include_router(config.router, prefix="/api", tags=["Config"])

if __name__ == "__main__":
    import uvicorn
    from src.Database.models import create_tables
    create_tables()
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
""")

    # Create config route
    os.makedirs(os.path.join(base_dir, "backend", "Routes"), exist_ok=True)
    config_path = os.path.join(base_dir, "backend", "Routes", "config.py")
    with open(config_path, "w") as f:
        f.write("""from fastapi import APIRouter
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
""")

    # Create metrics route
    metrics_path = os.path.join(base_dir, "backend", "Routes", "metrics.py")
    with open(metrics_path, "w") as f:
        f.write("""from fastapi import APIRouter
import random

router = APIRouter()

@router.get("/metrics/confusion-matrix")
def get_confusion_matrix():
    # Dummy data for UI
    return {
        "matrix": [
            [random.randint(900, 1000), random.randint(10, 50)],
            [random.randint(5, 30), random.randint(800, 950)]
        ],
        "labels": ["Normal", "Attack"]
    }

@router.get("/metrics/roc")
def get_roc():
    return {
        "fpr": [0.0, 0.1, 0.2, 0.5, 1.0],
        "tpr": [0.0, 0.8, 0.9, 0.95, 1.0]
    }

@router.get("/metrics/precision-recall")
def get_pr_curve():
    return {
        "recall": [0.0, 0.2, 0.5, 0.8, 1.0],
        "precision": [1.0, 0.95, 0.9, 0.85, 0.6]
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
""")

    # Update stats route
    stats_path = os.path.join(base_dir, "backend", "Routes", "stats.py")
    with open(stats_path, "w") as f:
        f.write("""from fastapi import APIRouter
from src.Database.db import get_connection
import time
import random

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
    
    # Simulate dynamic growth if DB is empty
    if total_events == 0:
        total_events = random.randint(10000, 15000)
        total_attacks = random.randint(500, 1000)
        
    normal = total_events - total_attacks
    return {
        "total_packets": total_events,
        "attacks_detected": total_attacks,
        "normal_traffic": normal,
        "status": "Running"
    }

@router.get("/attack-rate")
def get_attack_rate():
    # Return mock data for the last 60 seconds
    now = int(time.time())
    data = []
    for i in range(60):
        data.append({
            "time": now - (60 - i),
            "attacks": random.randint(0, 50)
        })
    return {"history": data}
""")

    # Update logs route
    logs_path = os.path.join(base_dir, "backend", "Routes", "logs.py")
    with open(logs_path, "w") as f:
        f.write("""from fastapi import APIRouter
from src.Database.db import get_connection
import random
import time

router = APIRouter()

@router.get("/logs")
def fetch_logs(page: int = 1, limit: int = 20):
    conn = get_connection()
    cursor = conn.cursor()
    offset = (page - 1) * limit
    cursor.execute("SELECT * FROM events ORDER BY timestamp DESC LIMIT ? OFFSET ?", (limit, offset))
    rows = cursor.fetchall()
    
    # If DB empty, generate mock logs for UI demonstration
    if not rows:
        logs = []
        for i in range(limit):
            is_attack = random.choice([0, 1])
            logs.append({
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time() - i*10)),
                "source_ip": f"192.168.1.{random.randint(2, 200)}",
                "dest_ip": f"10.0.0.{random.randint(2, 200)}",
                "prediction": "Attack" if is_attack else "Normal",
                "is_attack": is_attack
            })
    else:
        logs = [dict(r) for r in rows]
        
    conn.close()
    return {"logs": logs, "page": page, "total_pages": 10}
""")

    # Update alerts route
    alerts_path = os.path.join(base_dir, "backend", "Routes", "alerts.py")
    with open(alerts_path, "w") as f:
        f.write("""from fastapi import APIRouter
from src.Database.db import get_connection
import random
import time

router = APIRouter()

@router.get("/alerts/recent")
def get_alerts(limit: int = 10):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM alerts ORDER BY timestamp DESC LIMIT ?", (limit,))
    rows = cursor.fetchall()
    
    if not rows:
        alerts = []
        types = ["DDoS", "SQL Injection", "Port Scan", "Brute Force"]
        for i in range(limit):
            alerts.append({
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time() - random.randint(10, 1000))),
                "source_ip": f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}",
                "attack_type": random.choice(types),
                "message": "Intrusion attempt detected"
            })
    else:
        alerts = [dict(r) for r in rows]
    conn.close()
    return {"alerts": alerts}
""")

if __name__ == "__main__":
    create_files()
    print("Advanced backend generated.")
