# src/jules_cli/commands/history.py


import sqlite3
from ..db import get_db_path
from ..utils.logging import logger

def cmd_history_list():
    """List all history records."""
    db_path = get_db_path()
    try:
        con = sqlite3.connect(db_path)
        cur = con.cursor()
        cur.execute("SELECT session_id, timestamp, prompt, status FROM history ORDER BY timestamp DESC")
        rows = cur.fetchall()
        con.close()
        if not rows:
            logger.info("No history found.")
            return []
        results = []
        for row in rows:
            logger.info("Session: %s, Time: %s, Prompt: %s, Status: %s", row[0], row[1], row[2], row[3])
            results.append({"session_id": row[0], "timestamp": row[1], "prompt": row[2], "status": row[3]})
        return results
    except sqlite3.Error as e:
        logger.error("Failed to list history: %s", e)
        return {"error": str(e)}

def cmd_history_view(session_id: str):
    """View a specific history record."""
    db_path = get_db_path()
    try:
        con = sqlite3.connect(db_path)
        cur = con.cursor()
        cur.execute("SELECT * FROM history WHERE session_id = ?", (session_id,))
        row = cur.fetchone()
        con.close()
        if not row:
            logger.warning("Session not found: %s", session_id)
            return {"error": "Session not found."}
        logger.info("Session ID: %s", row[0])
        logger.info("Timestamp: %s", row[1])
        logger.info("Prompt: %s", row[2])
        logger.info("Patch: %s", row[3])
        logger.info("PR URL: %s", row[4])
        logger.info("Status: %s", row[5])
        return {
            "session_id": row[0],
            "timestamp": row[1],
            "prompt": row[2],
            "patch": row[3],
            "pr_url": row[4],
            "status": row[5],
        }
    except sqlite3.Error as e:
        logger.error("Failed to view history for session %s: %s", session_id, e)
        return {"error": str(e)}
