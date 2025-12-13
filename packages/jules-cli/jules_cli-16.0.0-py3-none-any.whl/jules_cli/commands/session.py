# src/jules_cli/commands/session.py

import json
from ..core.api import list_sessions, get_session
from ..utils.logging import logger
from ..cache import load_from_cache, save_to_cache

def cmd_session_list():
    cache_key = "session_list"
    cached_data = load_from_cache(cache_key)

    if cached_data:
        logger.info("Loaded session list from cache.")
        logger.info(json.dumps(cached_data, indent=2))
        return cached_data

    j = list_sessions()
    save_to_cache(cache_key, j)
    logger.info(json.dumps(j, indent=2))
    return j

def cmd_session_show(session_id: str):
    cache_key = f"session_{session_id}"
    cached_data = load_from_cache(cache_key)

    if cached_data:
        logger.info(f"Loaded session {session_id} from cache.")
        logger.info(json.dumps(cached_data, indent=2))
        return cached_data

    s = get_session(session_id)
    save_to_cache(cache_key, s)
    logger.info(json.dumps(s, indent=2))
    return s
