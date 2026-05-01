import sqlite3
import os

DEFAULT_DB_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "database")
DB_PATH = os.environ.get("IDS_DB_PATH", os.path.join(DEFAULT_DB_DIR, "ids.db"))
DB_DIR = os.path.dirname(DB_PATH)

def get_connection():
    os.makedirs(DB_DIR, exist_ok=True)
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn
