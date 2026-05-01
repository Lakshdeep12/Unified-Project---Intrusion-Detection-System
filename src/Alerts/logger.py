import os
from datetime import datetime

LOG_DIR = "logs"
ALERT_LOG_FILE = os.path.join(LOG_DIR, "alerts.log")
EVENT_LOG_FILE = os.path.join(LOG_DIR, "events.log")


def _ensure_log_dir():
    os.makedirs(LOG_DIR, exist_ok=True)


def log_alert(message):
    _ensure_log_dir()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    log_msg = f"[ALERT] {timestamp} - {message}"

    print(log_msg)

    with open(ALERT_LOG_FILE, "a") as f:
        f.write(log_msg + "\n")


def log_event(message):
    _ensure_log_dir()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    log_msg = f"[EVENT] {timestamp} - {message}"

    with open(EVENT_LOG_FILE, "a") as f:
        f.write(log_msg + "\n")