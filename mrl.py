import sqlite3
import json
from datetime import datetime
from sentence_transformers import SentenceTransformer
import numpy as np

MEMORY_DB = "memory.db"
_model = SentenceTransformer("all-MiniLM-L6-v2", device="cpu")


def init_memory_db():
    conn = sqlite3.connect(MEMORY_DB)
    conn.execute("""CREATE TABLE IF NOT EXISTS memory (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        session_id TEXT,
        fact_text TEXT,
        embedding TEXT,
        created_at TEXT
    )""")
    conn.commit()
    conn.close()


def embed_fact(fact_text):
    return _model.encode(fact_text).tolist()


def store_fact(session_id, fact_text):
    init_memory_db()
    embedding = embed_fact(fact_text)
    embedding_json = json.dumps(embedding)
    conn = sqlite3.connect(MEMORY_DB)
    conn.execute(
        "INSERT INTO memory (session_id, fact_text, embedding, created_at) VALUES (?, ?, ?, ?)",
        (session_id, fact_text, embedding_json, datetime.now().isoformat())
    )
    conn.commit()
    conn.close()


def get_all_facts_with_embeddings():
    conn = sqlite3.connect(MEMORY_DB)
    rows = conn.execute("SELECT session_id, fact_text, embedding, created_at FROM memory").fetchall()
    conn.close()
    return [(sid, text, json.loads(emb), created) for sid, text, emb, created in rows]


def search_facts(query_text, top_k=3):
    query_vector = embed_fact(query_text)
    all_facts = get_all_facts_with_embeddings()

    scored = []
    for session_id, fact_text, fact_vector, created_at in all_facts:
        similarity = np.dot(query_vector, fact_vector)
        scored.append((similarity, session_id, fact_text, created_at))

    scored.sort(reverse=True)
    return scored[:top_k]