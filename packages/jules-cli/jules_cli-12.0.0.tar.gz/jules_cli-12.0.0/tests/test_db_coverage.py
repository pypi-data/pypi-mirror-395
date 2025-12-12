# tests/test_db_coverage.py

import pytest
from unittest.mock import patch, MagicMock
from jules_cli import db
import sqlite3

# src/jules_cli/db.py

def test_add_history_record_error():
    with patch("jules_cli.db.get_db_path") as mock_path:
        with patch("sqlite3.connect") as mock_conn:
            mock_conn.return_value.cursor.side_effect = sqlite3.Error("fail")
            with patch("jules_cli.db.logger") as mock_logger:
                with pytest.raises(sqlite3.Error):
                    db.add_history_record("sess1")
                mock_logger.error.assert_called()

def test_get_latest_session_id_error():
    with patch("jules_cli.db.get_db_path") as mock_path:
        with patch("sqlite3.connect", side_effect=sqlite3.Error("fail")):
            with patch("jules_cli.db.logger") as mock_logger:
                res = db.get_latest_session_id()
                assert res is None
                mock_logger.error.assert_called()

def test_init_db_error():
    with patch("jules_cli.db.get_db_path") as mock_path:
        with patch("sqlite3.connect", side_effect=sqlite3.Error("fail")):
             with pytest.raises(sqlite3.Error):
                 db.init_db()

def test_add_history_record_update_all_fields():
    with patch("jules_cli.db.get_db_path"):
        with patch("sqlite3.connect") as mock_conn:
            cur = mock_conn.return_value.cursor.return_value
            cur.fetchone.return_value = (1,)

            db.add_history_record("sess1", prompt="p", patch="diff", pr_url="url", status="done")

            # verify update query
            args, _ = cur.execute.call_args
            assert "UPDATE history SET" in args[0]
            assert "prompt = ?" in args[0]
            assert "patch = ?" in args[0]
            assert "pr_url = ?" in args[0]
            assert "status = ?" in args[0]

def test_add_history_record_update_no_fields():
    with patch("jules_cli.db.get_db_path"):
        with patch("sqlite3.connect") as mock_conn:
            cur = mock_conn.return_value.cursor.return_value
            cur.fetchone.return_value = (1,)

            db.add_history_record("sess1")
            # Should not execute update if no fields
            # Logic: if updates: ...
            # Check calls.
            # call 1: SELECT 1 ...
            # call 2?
            assert cur.execute.call_count == 1 # Only SELECT

def test_add_history_record_insert():
    with patch("jules_cli.db.get_db_path"):
        with patch("sqlite3.connect") as mock_conn:
            cur = mock_conn.return_value.cursor.return_value
            cur.fetchone.return_value = None

            db.add_history_record("sess1", prompt="hi")

            args, _ = cur.execute.call_args
            assert "INSERT INTO history" in args[0]
