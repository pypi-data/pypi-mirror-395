# src/jules_cli/db.py


import sqlite3
import os
from pathlib import Path
from .utils.logging import logger

def get_db_path() -> Path:
    """Get the path to the history database."""
    xdg_data_home = os.environ.get('XDG_DATA_HOME', os.path.expanduser('~/.local/share'))
    db_dir = Path(xdg_data_home) / 'jules'
    db_dir.mkdir(parents=True, exist_ok=True)
    return db_dir / 'history.db'

def init_db():
    """Initialize the database and create the history table if it doesn't exist."""
    db_path = get_db_path()
    logger.debug("Initializing database at %s", db_path)
    try:
        con = sqlite3.connect(db_path)
        cur = con.cursor()
        cur.execute('''
            CREATE TABLE IF NOT EXISTS history (
                session_id TEXT PRIMARY KEY,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                prompt TEXT,
                patch TEXT,
                pr_url TEXT,
                status TEXT
            )
        ''')
        con.commit()
        con.close()
        logger.debug("Database initialized successfully.")
    except sqlite3.Error as e:
        logger.error("Database error: %s", e)
        raise

def add_history_record(session_id, prompt=None, patch=None, pr_url=None, status=None):
    """Add or update a record in the history table."""
    db_path = get_db_path()
    try:
        con = sqlite3.connect(db_path)
        cur = con.cursor()

        # Check if the record already exists
        cur.execute("SELECT 1 FROM history WHERE session_id = ?", (session_id,))
        exists = cur.fetchone()

        if exists:
            # Update existing record
            updates = {}
            if prompt is not None:
                updates['prompt'] = prompt
            if patch is not None:
                updates['patch'] = patch
            if pr_url is not None:
                updates['pr_url'] = pr_url
            if status is not None:
                updates['status'] = status

            if updates:
                set_clause = ", ".join([f"{k} = ?" for k in updates.keys()])
                values = list(updates.values())
                values.append(session_id)
                query = f"UPDATE history SET {set_clause} WHERE session_id = ?"
                cur.execute(query, tuple(values))
                logger.debug("History record for session %s updated.", session_id)
        else:
            # Insert new record
            cur.execute(
                "INSERT INTO history (session_id, prompt, patch, pr_url, status) VALUES (?, ?, ?, ?, ?)",
                (session_id, prompt, patch, pr_url, status)
            )
            logger.debug("History record for session %s added.", session_id)

        con.commit()
        con.close()
    except sqlite3.Error as e:
        logger.error("Failed to add/update history record: %s", e)
        raise


def get_latest_session_id():
    """Get the most recent session ID from the history."""
    db_path = get_db_path()
    try:
        con = sqlite3.connect(db_path)
        cur = con.cursor()
        cur.execute("SELECT session_id FROM history ORDER BY timestamp DESC LIMIT 1")
        row = cur.fetchone()
        con.close()
        return row[0] if row else None
    except sqlite3.Error as e:
        logger.error(f"Failed to get latest session: {e}")
        return None