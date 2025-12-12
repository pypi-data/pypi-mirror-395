# src/jules_cli/patch/resolver.py
import os
import anthropic
from ..utils.logging import logger

def resolve_conflict_with_ai(rejected_patch: str):
    """
    Sends the rejected patch to an AI service to generate a conflict-free patch.
    """
    logger.info("Attempting to resolve conflict with AI...")

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        logger.error("ANTHROPIC_API_KEY not set.")
        return None

    client = anthropic.Anthropic(api_key=api_key)

    try:
        message = client.messages.create(
            model="claude-2.1",
            max_tokens=4096,
            messages=[
                {
                    "role": "user",
                    "content": f"The following patch failed to apply. Please resolve the conflicts and return a conflict-free patch.\n\n{rejected_patch}",
                }
            ],
        )
        resolved_patch = message.content[0].text
        logger.info("AI resolution successful.")
        return resolved_patch
    except Exception as e:
        logger.error(f"AI resolution failed: {e}")
        return None
