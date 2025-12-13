# src/jules_cli/commands/suggest.py

import typer
from typing import Optional
from ..commands.task import run_task
from ..utils.logging import logger
from ..utils.ignore import collect_context_files

MASTER_SUGGEST_PROMPT = """
You are a Senior Staff Engineer auditing this repository.
Your goal is to suggest high-impact improvements.

Please scan the codebase and identify:
1. Critical technical debt or anti-patterns.
2. Missing edge-case handling or error handling.
3. Areas with low test coverage or brittle tests.
4. Performance bottlenecks.
5. Opportunities to modernize the stack (e.g., new language features).

Output a detailed plan with specific, actionable steps to address the top 3 most important findings.
Do not execute code yet; wait for approval.
"""

SECURITY_PROMPT = """
You are a Security Engineer auditing this repository.
Your goal is to identify security vulnerabilities and enforce best practices.

Please scan the codebase for:
1. OWASP Top 10 vulnerabilities (e.g., injection, broken auth, sensitive data exposure).
2. Hardcoded secrets or credentials.
3. Insecure dependencies or configuration.
4. Improper error handling that leaks information.
5. Missing security headers or input validation.

Output a remediation plan for the most critical issues found.
"""

TESTS_PROMPT = """
You are a QA Automation Architect.
Your goal is to improve the test suite coverage and reliability.

Please scan the codebase to find:
1. Modules with low or missing test coverage.
2. Complex logic that lacks edge-case tests.
3. Brittle tests that might fail randomly.
4. Opportunities for integration or property-based testing.

Output a plan to generate the missing tests or refactor existing ones.
"""

CHORE_PROMPT = """
You are a Code Maintainability Expert.
Your goal is to clean up technical debt and improve project hygiene.

Please scan the repository for:
1. Outdated dependencies or unused packages.
2. Dead code, unused imports, or variables.
3. Inconsistent formatting or style violations (PEP 8, etc.).
4. Typos in documentation or code comments.
5. Opportunities to simplify complex functions or reduce cognitive load.

Output a plan to execute these maintenance chores.
"""

def cmd_suggest(
    focus: Optional[str] = None,
    security: bool = False,
    tests: bool = False,
    chore: bool = False,
):
    """
    Ask Jules to proactively scan the repo and suggest improvements.
    """
    # Determine the base prompt based on flags
    if security:
        prompt = SECURITY_PROMPT
        logger.info("🔒 Security mode enabled. Auditing for vulnerabilities...")
    elif tests:
        prompt = TESTS_PROMPT
        logger.info("🧪 Test generation mode enabled. Analyzing coverage...")
    elif chore:
        prompt = CHORE_PROMPT
        logger.info("🧹 Chore mode enabled. Looking for cleanup opportunities...")
    else:
        prompt = MASTER_SUGGEST_PROMPT
        logger.info("🧠 Starting general proactive code analysis...")

    # Append specific focus if provided
    if focus:
        prompt += f"\n\nAdditionally, please prioritize your analysis on: {focus.upper()}."

    # Collect local file context respecting .julesignore
    # Note: Currently run_task/create_session doesn't accept file_list,
    # so we append the file structure to the prompt to give context about what is being scanned.
    # In future, create_session should accept local_files explicitly.
    try:
        files = collect_context_files()
        file_list_str = "\n".join(files[:500]) # Limit to 500 files to avoid huge prompt
        if len(files) > 500:
            file_list_str += f"\n... and {len(files) - 500} more files."

        prompt += f"\n\nContext - Files in repository (filtered by .julesignore):\n{file_list_str}"
        logger.debug(f"Attached {len(files)} files to the prompt context.")
    except Exception as e:
        logger.warning(f"Failed to collect local context files: {e}")

    logger.info("This may take a moment as Jules reads the repository context...")
    
    # Reuse run_task for session management with extended timeout (10 minutes)
    return run_task(prompt, timeout=600)