# src/jules_cli/pytest/runner.py

import json
from ..utils.commands import run_cmd
from ..utils.logging import logger
from ..utils.exceptions import TestRunnerError

def run_pytest() -> (int, str, str):
    logger.info("Running pytest...")
    code, out, err = run_cmd(["pytest", "-q", "--maxfail=1", "--json-report", "--json-report-file=report.json"])

    try:
        with open("report.json") as f:
            report = json.load(f)
        summary = report.get("summary", {})
        logger.info(
            f"Test run summary: "
            f"{summary.get('passed', 0)} passed, "
            f"{summary.get('failed', 0)} failed, "
            f"{summary.get('skipped', 0)} skipped."
        )
    except (FileNotFoundError, json.JSONDecodeError):
        logger.warning("Could not read pytest report.")

    return code, out, err
