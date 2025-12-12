# src/jules_cli/utils/commands.py

import subprocess
from typing import List
from .logging import logger

def run_cmd(cmd: List[str], capture: bool = True):
    logger.debug(f"Running command: {' '.join(cmd)}")
    result = subprocess.run(
        cmd,
        capture_output=capture,
        text=True,
    )
    if result.returncode != 0:
        logger.error(f"Command failed with code {result.returncode}: {result.stderr}")
    return result.returncode, result.stdout, result.stderr

def run_cmd_interactive(cmd: List[str]):
    logger.debug(f"Running interactive command: {' '.join(cmd)}")
    process = subprocess.Popen(
        cmd,
        stdin=subprocess.PIPE,
    )
    process.communicate()
    if process.returncode != 0:
        logger.error(f"Command failed with code {process.returncode}")
