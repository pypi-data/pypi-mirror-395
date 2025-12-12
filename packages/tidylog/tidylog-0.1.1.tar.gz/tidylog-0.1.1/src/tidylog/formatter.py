"""Custom logging formatters for tidylog.

This module provides formatters for structured logging output:
- ColoredJsonFormatter: Console output with ANSI colors and JSON extra fields
- TextFormatter: Plain text output for file handlers with JSON extra fields
"""

from __future__ import annotations

import json
import logging
from typing import Any


class ColoredJsonFormatter(logging.Formatter):
    """Formatter with colored log levels and dimmed JSON extra fields.

    This formatter enhances standard log output by:
    - Applying ANSI colors to log level names based on severity
    - Appending extra fields as dimmed JSON at the end of each message

    Args:
        fmt: Log message format string. Defaults to timestamp format.
        datefmt: Date format string. Defaults to None (ISO format).
        style: Format style ('%', '{', or '$'). Defaults to '%'.
        use_colors: Whether to apply ANSI colors. Defaults to True.
            Set to False for non-TTY output or file handlers.

    Example:
        >>> import logging
        >>> from tidylog import ColoredJsonFormatter
        >>> handler = logging.StreamHandler()
        >>> formatter = ColoredJsonFormatter()
        >>> handler.setFormatter(formatter)
        >>> logger = logging.getLogger("myapp")
        >>> logger.addHandler(handler)
        >>> logger.info("User logged in", extra={"user_id": 123})
        2024-01-15 10:30:00 - myapp - INFO - User logged in - {"user_id": 123}
    """

    # ANSI escape codes
    RESET: str = "\033[0m"
    DIM: str = "\033[2m"
    BOLD: str = "\033[1m"

    # Level-specific colors
    # fmt: off
    LEVEL_COLORS: dict[str, str] = {
        "DEBUG": "\033[36m",     # Cyan
        "INFO": "\033[32m",      # Green
        "WARNING": "\033[33m",   # Yellow
        "ERROR": "\033[31m",     # Red
        "CRITICAL": "\033[35m",  # Magenta
    }
    # fmt: on

    # Standard LogRecord attributes to exclude from extra fields
    # fmt: off
    _STANDARD_ATTRS: frozenset[str] = frozenset({
        "name", "msg", "args", "created", "filename", "funcName", "levelname",
        "levelno", "lineno", "module", "msecs", "message", "pathname", "process",
        "processName", "relativeCreated", "thread", "threadName", "exc_info",
        "exc_text", "stack_info", "taskName",
    })
    # fmt: on

    def __init__(
        self,
        fmt: str | None = None,
        datefmt: str | None = None,
        style: str = "%",
        use_colors: bool = True,
    ) -> None:
        """Initialize the formatter with optional color support.

        Args:
            fmt: Log message format string. Defaults to standard format.
            datefmt: Date format string. Defaults to None.
            style: Format style character. Defaults to '%'.
            use_colors: Whether to use ANSI colors. Defaults to True.
        """
        if fmt is None:
            fmt = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        super().__init__(fmt=fmt, datefmt=datefmt, style=style)
        self._use_colors = use_colors

    def format(self, record: logging.LogRecord) -> str:
        """Format a log record with colors and JSON extra fields.

        Args:
            record: The log record to format.

        Returns:
            Formatted log message string with optional colors and JSON extras.
        """
        # Make a copy to avoid mutating the original record
        record = logging.makeLogRecord(record.__dict__)

        # Apply color to log level if enabled
        levelname = record.levelname
        if self._use_colors and levelname in self.LEVEL_COLORS:
            record.levelname = (
                f"{self.LEVEL_COLORS[levelname]}{levelname}{self.RESET}"
            )

        # Get base formatted message
        base_message = super().format(record)

        # Extract and format extra fields
        extra_data = self._extract_extra(record)
        extra_str = self._format_extra(extra_data)

        return f"{base_message} - {extra_str}"

    def _extract_extra(self, record: logging.LogRecord) -> dict[str, Any]:
        """Extract non-standard attributes from a log record.

        Args:
            record: The log record to extract extras from.

        Returns:
            Dictionary of extra fields that were passed to the logger.
        """
        return {
            key: value
            for key, value in record.__dict__.items()
            if key not in self._STANDARD_ATTRS and not key.startswith("_")
        }

    def _format_extra(self, extra: dict[str, Any]) -> str:
        """Format extra data as a JSON string.

        Args:
            extra: Dictionary of extra fields to format.

        Returns:
            JSON string, optionally with dim ANSI formatting.
        """
        if extra:
            json_str = json.dumps(extra, default=str)
            if self._use_colors:
                return f"{self.DIM}{json_str}{self.RESET}"
            return json_str
        return "{}"


class TextFormatter(logging.Formatter):
    """Plain text formatter with JSON extra fields for file output.

    This formatter is designed for file handlers where ANSI colors are not
    needed. It appends extra fields as JSON only when present, resulting
    in cleaner log files.

    Args:
        fmt: Log message format string. Defaults to timestamp format.
        datefmt: Date format string. Defaults to None (ISO format).
        style: Format style ('%', '{', or '$'). Defaults to '%'.

    Example:
        >>> import logging
        >>> from tidylog import TextFormatter
        >>> handler = logging.FileHandler("app.log")
        >>> formatter = TextFormatter()
        >>> handler.setFormatter(formatter)
        >>> logger = logging.getLogger("myapp")
        >>> logger.addHandler(handler)
        >>> logger.info("User logged in", extra={"user_id": 123})
        # Output: 2024-01-15 10:30:00 - myapp - INFO - User logged in {"user_id": 123}
        >>> logger.info("Simple message")
        # Output: 2024-01-15 10:30:00 - myapp - INFO - Simple message
    """

    # Standard LogRecord attributes to exclude from extra fields
    # fmt: off
    _STANDARD_ATTRS: frozenset[str] = frozenset({
        "name", "msg", "args", "created", "filename", "funcName", "levelname",
        "levelno", "lineno", "module", "msecs", "message", "pathname", "process",
        "processName", "relativeCreated", "thread", "threadName", "exc_info",
        "exc_text", "stack_info", "taskName",
    })
    # fmt: on

    def __init__(
        self,
        fmt: str | None = None,
        datefmt: str | None = None,
        style: str = "%",
    ) -> None:
        """Initialize the text formatter.

        Args:
            fmt: Log message format string. Defaults to standard format.
            datefmt: Date format string. Defaults to None.
            style: Format style character. Defaults to '%'.
        """
        if fmt is None:
            fmt = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        super().__init__(fmt=fmt, datefmt=datefmt, style=style)

    def format(self, record: logging.LogRecord) -> str:
        """Format a log record with optional JSON extra fields.

        Args:
            record: The log record to format.

        Returns:
            Formatted log message string with JSON extras appended if present.
        """
        # Get base formatted message
        base_message = super().format(record)

        # Extract extra fields
        extra_data = self._extract_extra(record)

        # Only append JSON if there are extra fields
        if extra_data:
            json_str = json.dumps(extra_data, default=str)
            return f"{base_message} {json_str}"

        return base_message

    def _extract_extra(self, record: logging.LogRecord) -> dict[str, Any]:
        """Extract non-standard attributes from a log record.

        Args:
            record: The log record to extract extras from.

        Returns:
            Dictionary of extra fields that were passed to the logger.
        """
        return {
            key: value
            for key, value in record.__dict__.items()
            if key not in self._STANDARD_ATTRS and not key.startswith("_")
        }
