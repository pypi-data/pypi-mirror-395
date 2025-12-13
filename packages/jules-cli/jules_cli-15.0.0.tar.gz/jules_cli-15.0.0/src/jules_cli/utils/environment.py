# src/jules_cli/utils/environment.py

import os
from .exceptions import JulesError
from .config import config

def check_env():
    JULES_KEY = config.get_secret("JULES_API_KEY")
    if not JULES_KEY:
        raise JulesError("JULES_API_KEY not set in environment, keyring, or config. Set it via `jules auth login` or JULES_API_KEY env var.")
    # check if git is in path
    if os.system("git --version > /dev/null 2>&1") != 0:
        raise JulesError("git command not found. Make sure git is installed and in your PATH.")
