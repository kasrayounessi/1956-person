import sqlite3
from typing import List, Tuple

DB_PATH = "memory.db"


def init_db() -> None:
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
        CREATE TABLE IF NOT EXISTS turns (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            role TEXT NOT NULL,
            content TEXT NOT NULL,
            ts DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        """)
        conn.commit()


def add_turn(role: str, content: str) -> None:
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            "INSERT INTO turns(role, content) VALUES(?, ?)", (role, content))
        conn.commit()


def get_recent_turns(limit: int = 12) -> List[Tuple[str, str]]:
    with sqlite3.connect(DB_PATH) as conn:
        rows = conn.execute(
            "SELECT role, content FROM turns ORDER BY id DESC LIMIT ?",
            (limit,)
        ).fetchall()
    return list(reversed(rows))
