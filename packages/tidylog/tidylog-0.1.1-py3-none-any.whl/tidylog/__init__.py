"""TidyLog - Clean, colorized structured logging for Python.

TidyLog provides a simple API for structured logging with ANSI colors
and JSON extra fields. It uses only Python standard library modules.

Basic Usage:
    >>> from tidylog import get_logger
    >>> logger = get_logger(__name__)
    >>> logger.info("User action", extra={"user_id": 123, "action": "login"})

File Logging:
    >>> from tidylog import setup_file_logging
    >>> handler = setup_file_logging("logs/app.log", logger_names=["myapp"])

LiveKit Integration:
    >>> from tidylog.livekit import setup_job_logging
    >>> handler = setup_job_logging(ctx)  # Creates logs/{room_name}.log
"""

from tidylog._version import __version__
from tidylog.formatter import ColoredJsonFormatter, TextFormatter
from tidylog.logger import get_logger, setup_file_logging, setup_logging

__all__ = [
    "__version__",
    "ColoredJsonFormatter",
    "TextFormatter",
    "get_logger",
    "setup_file_logging",
    "setup_logging",
]
