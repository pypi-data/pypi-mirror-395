# src/jules_cli/utils/environment.py

import os
from .exceptions import JulesError

def check_env():
    JULES_KEY = os.environ.get("JULES_API_KEY")
    if not JULES_KEY:
        raise JulesError("JULES_API_KEY not set in environment. Set it before running.")
    # check if git is in path
    if os.system("git --version > /dev/null 2>&1") != 0:
        raise JulesError("git command not found. Make sure git is installed and in your PATH.")
