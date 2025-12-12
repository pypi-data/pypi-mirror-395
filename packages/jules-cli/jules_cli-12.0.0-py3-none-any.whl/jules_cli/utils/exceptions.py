# src/jules_cli/utils/exceptions.py

class JulesError(Exception):
    """Base class for all Jules CLI errors."""
    pass

class JulesAPIError(JulesError):
    """Raised when there's an error with the Jules API."""
    pass

class GitError(JulesError):
    """Raised when there's an error with a Git command."""
    pass

class PatchError(JulesError):
    """Raised when a patch fails to apply."""
    pass

class TestRunnerError(JulesError):
    """Raised when the test runner fails."""
    __test__ = False
    pass

class ConfigError(JulesError):
    """Raised when there's an error with the configuration."""
    pass
