from Database.db import get_connection
from datetime import datetime
import json


def insert_event(data, prediction):
    conn = get_connection()
    cursor = conn.cursor()

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    is_attack = 1 if prediction == 1 else 0

    cursor.execute("""
    INSERT INTO events (timestamp, prediction, is_attack, data)
    VALUES (?, ?, ?, ?)
    """, (timestamp, prediction, is_attack, json.dumps(data)))

    conn.commit()
    conn.close()