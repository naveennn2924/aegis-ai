import sqlite3
from pathlib import Path

# Always resolve DB path relative to project root
BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "storage" / "aegisai_traces.db"


def get_connection():
    return sqlite3.connect(DB_PATH, check_same_thread=False)


def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS traces (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        trace_id TEXT,
        agent TEXT,
        event TEXT,
        latency REAL,
        payload TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS reviews (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        trace_id TEXT,
        decision TEXT,
        comment TEXT
    )
    """)

    conn.commit()
    conn.close()
