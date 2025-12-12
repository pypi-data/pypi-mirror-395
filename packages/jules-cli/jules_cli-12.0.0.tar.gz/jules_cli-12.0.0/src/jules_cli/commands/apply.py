# src/jules_cli/commands/apply.py

from ..state import _state
from ..patch.apply import apply_patch_text
from ..utils.logging import logger
from ..cache import save_to_cache
from ..db import get_latest_session_id
from ..core.api import poll_for_result

def cmd_apply():
    res = _state.get("last_result")
    
    # Fallback: If no result in memory, try to fetch from the last session in DB
    if not res:
        session_id = _state.get("session_id") or get_latest_session_id()
        if session_id:
            logger.info(f"No recent result in memory. Checking session {session_id}...")
            try:
                res = poll_for_result(session_id, timeout=5)
                _state["last_result"] = res
            except Exception:
                pass

    if not res:
        logger.warning("No last result to apply.")
        return {"status": "error", "message": "No last result to apply."}
        
    if res["type"] != "patch":
        logger.warning("Last result is not a patch. It may be a PR artifact.")
        return {"status": "error", "message": "Last result is not a patch."}
    
    patch = res["patch"]

    # Cache the patch
    cache_key = f"patch_{_state.get('session_id')}"
    save_to_cache(cache_key, {"patch": patch})

    apply_patch_text(patch)
    return {"status": "success", "message": "Patch applied."}