from ..utils.commands import run_cmd
from ..utils.logging import logger
import json
import tempfile
import os
from typing import Tuple

def run_tests(runner: str = "pytest", detect_flaky: bool = False) -> Tuple[int, str, str]:
    """
    Run tests using the specified runner.

    Args:
        runner: The test runner to use ('pytest', 'unittest', 'nose2').
        detect_flaky: Whether to try to detect flaky tests by re-running failures.

    Returns:
        tuple: (exit_code, stdout, stderr)
    """
    if runner == "pytest":
        return _run_pytest(detect_flaky=detect_flaky)
    elif runner == "unittest":
        return _run_unittest()
    elif runner == "nose2":
        return _run_nose2()
    else:
        raise ValueError(f"Unknown runner: {runner}")

def _run_pytest(detect_flaky: bool = False) -> Tuple[int, str, str]:
    logger.info("Running pytest...")

    with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as tmp:
        report_path = tmp.name

    try:
        cmd = ["pytest", "-q", "--json-report", f"--json-report-file={report_path}"]
        # If we are not detecting flaky tests, we can fail fast
        if not detect_flaky:
            cmd.append("--maxfail=1")

        code, out, err = run_cmd(cmd)

        try:
            with open(report_path) as f:
                report = json.load(f)

            summary = report.get("summary", {})
            failed_tests = []

            # Extract failed tests if any
            if summary.get("failed", 0) > 0:
                for test in report.get("tests", []):
                    if test.get("outcome") == "failed":
                        failed_tests.append(test.get("nodeid"))

            logger.info(
                f"Test run summary: "
                f"{summary.get('passed', 0)} passed, "
                f"{summary.get('failed', 0)} failed, "
                f"{summary.get('skipped', 0)} skipped."
            )

            # Flaky test detection
            if detect_flaky and failed_tests:
                logger.info(f"Attempting to detect flaky tests. Re-running {len(failed_tests)} failed tests...")

                # Re-run only the failed tests
                rerun_cmd = ["pytest", "-q", "--json-report", f"--json-report-file={report_path}"] + failed_tests
                rerun_code, rerun_out, rerun_err = run_cmd(rerun_cmd)

                # Check results of re-run
                with open(report_path) as f:
                    rerun_report = json.load(f)

                rerun_summary = rerun_report.get("summary", {})

                flaky_tests = []
                confirmed_failed = []

                for test in rerun_report.get("tests", []):
                    nodeid = test.get("nodeid")
                    if test.get("outcome") == "passed":
                        flaky_tests.append(nodeid)
                    elif test.get("outcome") == "failed":
                        confirmed_failed.append(nodeid)

                if flaky_tests:
                    logger.warning(f"⚠️  Flaky tests detected ({len(flaky_tests)}):")
                    for ft in flaky_tests:
                        logger.warning(f"  - {ft}")
                    out += f"\n\nFlaky tests detected ({len(flaky_tests)}):\n" + "\n".join(f"- {ft}" for ft in flaky_tests)

                    # If all failures were flaky, we consider the run effectively 'passed' (or at least not broken)
                    # But for now, let's keep the code as is, but maybe log it clearly.
                    # If we want to prevent auto-fix from kicking in for flaky tests, we might want to return code 0?
                    # But usually flaky tests are still a problem.

                    if not confirmed_failed:
                        logger.info("All failures were flaky.")
                        # Should we return 0?
                        # If detecting flaky, maybe we return 0 so 'jules auto' doesn't try to fix code that works sometimes.
                        code = 0

        except (FileNotFoundError, json.JSONDecodeError):
            logger.warning("Could not read pytest report.")
    finally:
        if os.path.exists(report_path):
            os.remove(report_path)

    return code, out, err

def _run_unittest() -> Tuple[int, str, str]:
    logger.info("Running unittest...")
    # unittest prints output to stderr by default
    return run_cmd(["python", "-m", "unittest"])

def _run_nose2() -> Tuple[int, str, str]:
    logger.info("Running nose2...")
    return run_cmd(["python", "-m", "nose2"])
