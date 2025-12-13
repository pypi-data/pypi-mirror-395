# src/jules_cli/commands/hooks.py

import os
import sys
from ..utils.logging import logger
import typer

def install_hooks():
    """
    Installs Jules CLI hooks into .pre-commit-config.yaml
    """
    config_file = ".pre-commit-config.yaml"

    hook_config = """
  - repo: local
    hooks:
      - id: jules-suggest
        name: Jules Suggest
        entry: jules suggest --check
        language: system
        pass_filenames: false
"""

    if os.path.exists(config_file):
        with open(config_file, "r") as f:
            content = f.read()
            if "jules-suggest" in content:
                logger.info("Jules hooks already present in .pre-commit-config.yaml")
                return

    # Check if we are creating new or appending
    mode = "a" if os.path.exists(config_file) else "w"

    with open(config_file, mode) as f:
        if mode == "w":
            f.write("repos:\n")
        f.write(hook_config)

    logger.info(f"Added Jules hooks to {config_file}")
    logger.info("Run `pre-commit install` to activate.")
