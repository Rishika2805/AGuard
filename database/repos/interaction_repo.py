import sqlite3
from datetime import datetime
from database.db import get_connection


def log_interaction(content_id: str, action: str):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO interactions (content_id, action, timestamp)
        VALUES (?, ?, ?)
        """,
        (
            content_id,
            action,
            datetime.utcnow().isoformat()
        )
    )

    conn.commit()
    conn.close()
