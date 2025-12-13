# src/jules_cli/cache.py
import os
import json
from pathlib import Path
from .utils.logging import logger

CACHE_DIR = Path("~/.cache/jules").expanduser()
CACHE_DIR.mkdir(parents=True, exist_ok=True)

def get_cache_file(cache_key: str) -> Path:
    return CACHE_DIR / f"{cache_key}.json"

def load_from_cache(cache_key: str):
    cache_file = get_cache_file(cache_key)
    if cache_file.exists():
        try:
            with open(cache_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            logger.warning(f"Failed to load from cache: {e}")
            return None
    return None

def save_to_cache(cache_key: str, data: dict):
    cache_file = get_cache_file(cache_key)
    try:
        with open(cache_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
    except IOError as e:
        logger.error(f"Failed to save to cache: {e}")

def clear_cache(cache_key: str):
    cache_file = get_cache_file(cache_key)
    if cache_file.exists():
        try:
            os.remove(cache_file)
        except OSError as e:
            logger.error(f"Failed to clear cache: {e}")
