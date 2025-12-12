# src/jules_cli/patch/apply.py

import os
import re
from ..utils.commands import run_cmd
from ..utils.logging import logger
from ..utils.exceptions import PatchError
from .resolver import resolve_conflict_with_ai

def extract_rejected_hunks(patch_output: str) -> str:
    """
    Extracts the rejected hunks from the output of the patch command.
    """
    rejected_hunks_content = []
    # This regex looks for lines that represent removed or added lines in a diff,
    # often prefixed by a space in patch output.
    # It specifically targets lines starting with a space then '-' or '+'
    # followed by the actual content.
    diff_line_pattern = re.compile(r"^[ ]*([-+].*)$", re.MULTILINE)

    for match in diff_line_pattern.finditer(patch_output):
        rejected_hunks_content.append(match.group(1))

    return "\n".join(rejected_hunks_content)

def apply_patch_text(patch_text: str):
    tmp = "tmp_patch.diff"
    try:
        with open(tmp, "w", encoding="utf-8") as f:
            f.write(patch_text)

        logger.info("Applying patch via 'patch -p1 -i tmp_patch.diff' ...")
        code, out, err = run_cmd(["patch", "-p1", "-i", tmp])

        if code == 0:
            logger.info("Patch applied successfully.")
            return

        logger.error("Patch failed; stdout/stderr:")
        logger.error(out)
        logger.error(err)

        # Extract rejected hunks
        rejected_hunks = extract_rejected_hunks(err)

        # Attempt to resolve conflict with AI
        logger.info("Attempting AI conflict resolution...")
        resolved_patch = resolve_conflict_with_ai(rejected_hunks)

        if not resolved_patch:
            logger.warning("AI resolution failed. Please resolve conflicts manually.")
            logger.info("Fallback strategies:")
            logger.info("1. Manually resolve the conflicts in the rejected patch file.")
            logger.info("2. Apply the patch with a different tool, such as `git apply`.")
            logger.info("3. Discard the patch and start over.")
            raise PatchError("patch failed and AI could not resolve it")

        with open(tmp, "w", encoding="utf-8") as f:
            f.write(resolved_patch)

        logger.info("Re-applying patch after AI resolution...")
        code, out, err = run_cmd(["patch", "-p1", "-i", tmp])

        if code != 0:
            logger.error("Re-applying patch failed; stdout/stderr:")
            logger.error(out)
            logger.error(err)
            raise PatchError("patch failed after AI resolution")

        logger.info("Patch applied successfully after AI resolution.")
    finally:
        if os.path.exists(tmp):
            os.remove(tmp)
