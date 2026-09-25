import sqlite3
from datetime import datetime

MEMORY_DB = "memory.db"


def init_memory_db():
    conn = sqlite3.connect(MEMORY_DB)
    conn.execute("""CREATE TABLE IF NOT EXISTS memory (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        session_id TEXT,
        fact_text TEXT,
        created_at TEXT
    )""")
    conn.commit()
    conn.close()


def store_fact(session_id, fact_text):
    init_memory_db()
    conn = sqlite3.connect(MEMORY_DB)
    conn.execute(
        "INSERT INTO memory (session_id, fact_text, created_at) VALUES (?, ?, ?)",
        (session_id, fact_text, datetime.now().isoformat())
    )
    conn.commit()
    conn.close()


def get_all_facts():
    conn = sqlite3.connect(MEMORY_DB)
    rows = conn.execute("SELECT session_id, fact_text, created_at FROM memory").fetchall()
    conn.close()
    return rows