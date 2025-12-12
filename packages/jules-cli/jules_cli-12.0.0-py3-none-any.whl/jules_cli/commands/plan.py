# src/jules_cli/commands/plan.py

from typing import Optional
from ..core.api import approve_plan, send_message, poll_for_result, get_session
from ..db import get_latest_session_id
from ..utils.logging import logger
from ..state import _state
import json

def _get_session_id(session_id: Optional[str]) -> Optional[str]:
    if session_id:
        return session_id
    
    # Try to get from current state (if in REPL)
    if _state.get("current_session"):
        return _state["current_session"].get("id")
        
    # Try to get from DB
    latest = get_latest_session_id()
    if latest:
        return latest
        
    return None

def cmd_approve(session_id: Optional[str] = None):
    """
    Approve the plan for a session.
    """
    sid = _get_session_id(session_id)
    if not sid:
        logger.error("No session ID provided and no recent session found.")
        return {"status": "error", "message": "No session found."}

    try:
        approve_plan(sid)
        logger.info(f"Plan for session {sid} approved.")
        
        # Poll for the next result (execution)
        logger.info("Polling for execution results...")
        result = poll_for_result(sid)
        
        # Store result in state for 'apply' command
        _state["last_result"] = result
        
        if result["type"] == "patch":
            logger.info("Patch available in last_result['patch']. Use `apply` to apply locally.")
        elif result["type"] == "pr":
            pr = result.get("pr")
            logger.info("PR artifact: %s", json.dumps(pr, indent=2))
        elif result["type"] == "message":
            logger.info(f"Jules: {result.get('message')}")
            
        return {"status": "success", "result": result}
    except Exception as e:
        logger.error(f"Failed to approve plan: {e}")
        return {"status": "error", "message": str(e)}

def cmd_reject(session_id: Optional[str] = None):
    """
    Reject the plan for a session.
    """
    sid = _get_session_id(session_id)
    if not sid:
        logger.error("No session ID provided and no recent session found.")
        return {"status": "error", "message": "No session found."}

    try:
        logger.info(f"Rejecting plan for session {sid}...")
        send_message(sid, "I reject this plan. Please stop or propose a different approach.")
        return {"status": "success", "message": "Rejection sent."}
    except Exception as e:
        logger.error(f"Failed to reject plan: {e}")
        return {"status": "error", "message": str(e)}