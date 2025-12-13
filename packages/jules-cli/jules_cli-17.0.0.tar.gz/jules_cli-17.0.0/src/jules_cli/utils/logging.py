# src/jules_cli/utils/logging.py

import logging

# -----------------
# Custom Log Levels
# -----------------
VERBOSE = 15
logging.addLevelName(VERBOSE, "VERBOSE")


# -----------------
# Setup initial logger
# -----------------
# This is a placeholder logger that can be used by any module.
# It will be configured by the CLI entrypoint.
logger = logging.getLogger("jules")


# -----------------
# Main setup function
# -----------------
def setup_logging(level="INFO", color=True):
    """
    Configure the root logger for the Jules CLI.
    This should be called once at the start of the application.
    """
    # Clear existing handlers to prevent duplicate output in tests
    # and ValueError: I/O operation on closed file.
    if logger.handlers:
        for handler in list(logger.handlers):
            logger.removeHandler(handler)
            # Only close FileHandlers, not StreamHandlers (which might wrap stdout/stderr)
            if isinstance(handler, logging.FileHandler):
                try:
                    handler.close()
                except Exception:
                    pass

    logger.setLevel(level)
    handler = logging.StreamHandler()
    formatter = ColorFormatter() if color else logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)


# -----------------
# Color Formatter for logging
# -----------------
# This formatter adds color to the log levels.
# It's a bit verbose, but it's a common pattern.
class ColorFormatter(logging.Formatter):
    """
    A logging formatter that adds color to the log levels.
    """

    GREY = "\x1b[38;20m"
    YELLOW = "\x1b[33;20m"
    RED = "\x1b[31;20m"
    BOLD_RED = "\x1b[31;1m"
    RESET = "\x1b[0m"
    GREEN = "\x1b[32m"
    BLUE = "\x1b[34m"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.FORMATS = {
            logging.DEBUG: self.GREY + "%(levelname)s" + self.RESET + ": %(message)s",
            VERBOSE: self.BLUE + "%(levelname)s" + self.RESET + ": %(message)s",
            logging.INFO: self.GREEN + "%(levelname)s" + self.RESET + ": %(message)s",
            logging.WARNING: self.YELLOW + "%(levelname)s" + self.RESET + ": %(message)s",
            logging.ERROR: self.RED + "%(levelname)s" + self.RESET + ": %(message)s",
            logging.CRITICAL: self.BOLD_RED + "%(levelname)s" + self.RESET + ": %(message)s",
        }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)
