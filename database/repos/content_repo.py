# database/repos/content_repo.py

import hashlib
import json
from datetime import datetime
from database.db import get_connection

def generate_content_hash(item : dict) -> dict:
    """
    Generates a stable hash from content-defining fields
    """

    base_text = f"{item.get('title','')}|{item.get('content','')}"
    return hashlib.sha256(base_text.encode('utf-8')).hexdigest()

def is_malformed(item  : dict) -> bool:
    """
    Basic sanity checks before DB insertion
    """

    if not item.get('id'):
        return True
    if not item.get('source'):
        return True
    if not item.get('content'):
        return True
    return False

def insert_content(item : dict) -> bool:
    """
    Inserts a content into DB.
    Returns True if insertion was successful, False otherwise
    """
    if is_malformed(item):
        print(f"[SKIPPED][MALFORMED]: {item.get('id')}]")
        return False

    content_hash = generate_content_hash(item)
    processed_at = datetime.utcnow().isoformat()

    conn = get_connection()
    cursor = conn.cursor()

    try :
        cursor.execute(
            """
            INSERT INTO content_items(
                id,
                source,
                sender,
                title,
                content,
                timestamp,
                url,
                tags,
                content_hash,
                processed_at
            )
                VALUES (?,?,?,?,?,?,?,?,?,?)
            """,
            (
                item['id'],
                item['source'],
                item.get('sender'),
                item.get('title'),
                item.get('content'),
                item.get('timestamp'),
                item.get('url'),
                json.dumps(item.get('tags',[])),
                content_hash,
                processed_at
            )
        )

        conn.commit()
        print(f"[INSERTED] {item['source']}::{item['id']}")
        return True

    except Exception as e:
        print(f"[SKIPPED][ERROR]: {e}")
        return False

    finally:
        cursor.close()
