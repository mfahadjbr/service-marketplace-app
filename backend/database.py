import sqlite3
import os
from dotenv import load_dotenv

load_dotenv()

DB_PATH = os.getenv("SQLITE_DB_PATH", "app.db")

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def execute_query(query, params=None):
    with get_db_connection() as conn:
        cur = conn.cursor()
        cur.execute(query, params or ())
        if query.strip().upper().startswith('SELECT'):
            return [dict(row) for row in cur.fetchall()]
        conn.commit()
        return None

def execute_query_one(query, params=None):
    with get_db_connection() as conn:
        cur = conn.cursor()
        cur.execute(query, params or ())
        # Fetch result before commit for SELECT, INSERT, UPDATE, and DELETE (with RETURNING)
        if (
            query.strip().upper().startswith('SELECT') or
            query.strip().upper().startswith('INSERT') or
            query.strip().upper().startswith('UPDATE') or
            query.strip().upper().startswith('DELETE')
        ):
            row = cur.fetchone()
            conn.commit()
            return dict(row) if row else None
        conn.commit()
        return None 