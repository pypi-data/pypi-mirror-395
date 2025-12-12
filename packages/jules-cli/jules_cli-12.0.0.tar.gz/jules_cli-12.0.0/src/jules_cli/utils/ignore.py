import os
import fnmatch
from typing import List, Generator

DEFAULT_IGNORES = [
    ".git/",
    ".env",
    ".venv/",
    "node_modules/",
    "__pycache__/",
    "*.pyc",
    ".DS_Store",
    "package-lock.json",
    "yarn.lock",
    "poetry.lock"
]

class ContextFilter:
    def __init__(self, root_path: str = "."):
        self.root_path = os.path.abspath(root_path)
        self.ignore_patterns = self._load_ignore_patterns()

    def _load_ignore_patterns(self) -> List[str]:
        patterns = list(DEFAULT_IGNORES)
        ignore_file = os.path.join(self.root_path, ".julesignore")
        if os.path.exists(ignore_file):
            with open(ignore_file, "r") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#"):
                        patterns.append(line)
        return patterns

    def is_ignored(self, path: str) -> bool:
        """
        Check if a file path (absolute or relative to root) should be ignored.
        """
        if os.path.isabs(path):
            rel_path = os.path.relpath(path, self.root_path)
        else:
            rel_path = path

        # Normalize path separators
        rel_path = rel_path.replace(os.sep, "/")

        # Split path into parts to check directories
        parts = rel_path.split("/")

        for pattern in self.ignore_patterns:
            # Directory match (ends with /)
            if pattern.endswith("/"):
                dir_pattern = pattern.rstrip("/")

                # Check if the pattern matches any directory in the path
                # Case 1: Simple directory name "node_modules/"
                if "/" not in dir_pattern:
                    if dir_pattern in parts:
                        return True

                # Case 2: Nested directory pattern "foo/bar/"
                else:
                    if rel_path.startswith(dir_pattern + "/") or rel_path == dir_pattern:
                        return True

            else:
                # File match
                # If pattern contains /, match against full relative path
                if "/" in pattern:
                     if fnmatch.fnmatch(rel_path, pattern):
                         return True
                else:
                     # Match against filename only
                     if fnmatch.fnmatch(os.path.basename(rel_path), pattern):
                         return True
        return False

    def walk(self) -> Generator[str, None, None]:
        """
        Walks the directory and yields files that are not ignored.
        Yields absolute file paths.
        """
        for root, dirs, files in os.walk(self.root_path):
            # Filter directories in-place to avoid traversing ignored ones
            # We iterate backwards to allow safe removal
            for d in list(dirs):
                 full_path = os.path.join(root, d)
                 if self.is_ignored(full_path):
                     dirs.remove(d)

            for f in files:
                full_path = os.path.join(root, f)
                if not self.is_ignored(full_path):
                    yield full_path

def collect_context_files(root_path: str = ".") -> List[str]:
    """
    Collects all files in the given directory that are not ignored by .julesignore.
    Returns a list of relative file paths (relative to root_path).
    """
    ctx_filter = ContextFilter(root_path)
    files = []
    for f in ctx_filter.walk():
        # Convert to relative path
        files.append(os.path.relpath(f, ctx_filter.root_path))
    return files
