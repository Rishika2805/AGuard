from database.db import get_connection

def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    # Enable FK support in SQLite
    cursor.execute("PRAGMA foreign_keys = ON")

    # Table - 1 -> Content Memory Table (Root Table)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS content_items (
            id TEXT PRIMARY KEY,
            source TEXT NOT NULL,
            sender TEXT,
            title TEXT,
            content TEXT,
            timestamp TEXT,
            url TEXT,
            tags TEXT,
            content_hash TEXT UNIQUE,
            processed_at TEXT
        )
    """)

    # Table - 2 -> Decision Log( FK -> content_items)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS decisions (
            decision_id INTEGER PRIMARY KEY AUTOINCREMENT,
            content_id TEXT NOT NULL,
            decision TEXT,
            score TEXT,
            reason TEXT,
            stage TEXT,
            decision_at TEXT,
            FOREIGN KEY (decision_id) 
                REFERENCES decisions (decision_id)
                ON DELETE CASCADE
        )           
        """
    )

    # Table - 3 -> Derived Patterns (no FK)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS patterns (
            pattern_key TEXT PRIMARY KEY,
            metric TEXT,
            value REAL,
            updated_at TEXT
    )
    """
    )

    # Table - 4 -> User Interaction ( FK -> content_items)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS interactions (
            interection_id INTEGER PRIMARY KEY AUTOINCREMENT,
            content_id TEXT NOT NULL,
            action TEXT,
            timestamp TEXT,
            FOREIGN KEY (content_id) 
                REFERENCES content_items (content_id)
                ON DELETE CASCADE
        )
    """
    )
    conn.commit()
    conn.close()