"""Database helpers for opening SQLite connections and running SQL safely."""

import sqlite3
from flask import current_app

def get_db_connection():
    """Open a SQLite connection using the configured application database path."""
    db_path = current_app.config['DATABASE']
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

def execute_query(query: str, *args) -> list[dict] | None:
    """Execute parameterized SQL queries and return rows for SELECT statements."""
    with get_db_connection() as conn:
        conn.execute("PRAGMA foreign_keys = ON")
        cursor = conn.cursor()
        cursor.execute(query, args)
        conn.commit()
        
        if query.strip().upper().startswith("SELECT"):
            return [dict(row) for row in cursor.fetchall()]
        
        return None

def execute_script(script: str) -> None:
    """Execute a full SQL script, usually used for schema bootstrapping."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.executescript(script)
        conn.commit()
