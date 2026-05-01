import os
import tempfile
import uuid

os.environ["IDS_DB_PATH"] = os.path.join(tempfile.gettempdir(), "ids_test.db")

from fastapi.testclient import TestClient

from backend.main import app
from src.Database.db import get_connection
from src.Database.models import create_tables
from src.features.extractor import extract_features


SAMPLE_FEATURES = [
    6,
    0,
    0,
    0,
    0,
    0,
    0,
    1,
    0,
    64,
    1200,
    10,
    8,
    5000,
    15,
]


def setup_module():
    create_tables()


def test_health_endpoint():
    client = TestClient(app)
    response = client.get("/api/health")

    assert response.status_code == 200
    assert response.json()["status"] == "running"


def test_register_and_login_flow():
    client = TestClient(app)
    username = f"operator_{uuid.uuid4().hex[:8]}"
    password = "pass12345"

    register = client.post(
        "/api/auth/register",
        json={"username": username, "password": password},
    )
    assert register.status_code == 200

    login = client.post(
        "/api/auth/login",
        data={"username": username, "password": password},
    )
    assert login.status_code == 200
    body = login.json()
    assert body["token_type"] == "bearer"
    assert body["access_token"]


def test_database_tables_exist():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type = 'table'")
    tables = {row["name"] for row in cursor.fetchall()}
    conn.close()

    assert {"users", "events", "alerts", "system_config"}.issubset(tables)


def test_predict_endpoint_uses_real_model():
    client = TestClient(app)
    response = client.post(
        "/api/predict",
        json={"features": SAMPLE_FEATURES, "model_key": "Set-1"},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "success"
    assert body["model_key"] == "Set-1"
    assert body["prediction"] in {"NORMAL", "ATTACK"}
    assert "rf_confidence" in body["details"]


def test_predict_rejects_wrong_feature_count():
    client = TestClient(app)
    response = client.post(
        "/api/predict",
        json={"features": [1, 2, 3], "model_key": "Set-1"},
    )

    assert response.status_code == 422


def test_packet_extractor_matches_model_feature_count():
    from scapy.all import IP, TCP

    packet = IP(src="192.168.1.10", dst="10.0.0.5") / TCP(sport=12345, dport=80, flags="S")
    features = extract_features(packet)

    assert len(features) == 15
