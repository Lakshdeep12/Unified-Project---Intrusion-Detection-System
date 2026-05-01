from src.Database.db import get_connection

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

    # Optimize database queries with indexes
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_events_timestamp ON events(timestamp)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_events_is_attack ON events(is_attack)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_alerts_timestamp ON alerts(timestamp)")

    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_tables()
