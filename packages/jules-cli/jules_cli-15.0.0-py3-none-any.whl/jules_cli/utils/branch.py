# src/jules_cli/utils/branch.py

from .config import config
from slugify import slugify
import time

def generate_branch_name(description: str, branch_type: str = "feature") -> str:
    """
    Generates a branch name based on the description and type.

    Args:
        description: A description of the branch.
        branch_type: The type of the branch (e.g., feature, fix, refactor).

    Returns:
        The generated branch name.
    """
    pattern = config.get_nested("branch", "pattern", "{type}/{slug}/{timestamp}")

    slug = slugify(description)
    timestamp = str(int(time.time()))

    branch_name = pattern.format(type=branch_type, slug=slug, timestamp=timestamp, description=slug)

    return branch_name
