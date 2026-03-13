# database/decision_repo.py
from datetime import datetime
from database.db import get_connection


def log_decision(decision: dict) -> None:
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            """
            INSERT INTO decisions (
                content_id,
                decision,
                score,
                reason,
                stage,
                decided_at
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                decision["content_id"],
                decision["decision"],
                decision.get("score"),
                decision.get("reason"),
                decision.get("stage"),
                datetime.utcnow().isoformat(),
            )
        )
        conn.commit()
    except Exception as e:
        raise
    finally:
        conn.close()
