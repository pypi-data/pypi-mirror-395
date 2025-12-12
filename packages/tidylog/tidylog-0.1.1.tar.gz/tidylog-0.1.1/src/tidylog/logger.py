"""Logger configuration utilities for tidylog.

This module provides functions for setting up and retrieving
configured loggers with tidylog formatters.
"""

from __future__ import annotations

import logging
import os
import sys
from pathlib import Path
from typing import TextIO

from tidylog.formatter import ColoredJsonFormatter, TextFormatter


def _should_use_colors(stream: TextIO | None) -> bool:
    """Detect if ANSI colors should be used for a stream.

    Args:
        stream: The output stream to check. Defaults to stderr if None.

    Returns:
        True if colors should be used, False otherwise.
    """
    if stream is None:
        stream = sys.stderr

    # Check if stream is a TTY
    if not hasattr(stream, "isatty") or not stream.isatty():
        return False

    # Check for NO_COLOR environment variable (standard convention)
    if os.environ.get("NO_COLOR"):
        return False

    # Check TERM environment variable
    term = os.environ.get("TERM", "")
    if term == "dumb":
        return False

    return True


def setup_logging(
    level: int | str = logging.DEBUG,
    stream: TextIO | None = None,
    fmt: str | None = None,
    datefmt: str | None = None,
    use_colors: bool | None = None,
    logger_name: str | None = None,
) -> logging.Logger:
    """Configure structured logging with the ColoredJsonFormatter.

    Sets up a logger with a StreamHandler using the ColoredJsonFormatter
    for colorized, structured output.

    Args:
        level: Log level as int (e.g., logging.DEBUG) or string ("DEBUG").
            Defaults to logging.DEBUG.
        stream: Output stream for the handler. Defaults to sys.stderr.
        fmt: Custom format string. Defaults to standard timestamp format.
        datefmt: Custom date format string. Defaults to ISO format.
        use_colors: Enable/disable ANSI colors. Defaults to auto-detection
            based on whether stream is a TTY.
        logger_name: Name for the logger. Defaults to None (root logger).

    Returns:
        The configured logger instance.

    Example:
        >>> from tidylog import setup_logging
        >>> logger = setup_logging(level="INFO", logger_name="myapp")
        >>> logger.info("Application started")

    Note:
        Calling this function multiple times with the same logger_name
        will add additional handlers. Use get_logger() for repeat access.
    """
    if stream is None:
        stream = sys.stderr

    if use_colors is None:
        use_colors = _should_use_colors(stream)

    # Convert string level to int if needed
    if isinstance(level, str):
        level = logging._nameToLevel[level.upper()]

    # Create handler with formatter
    handler = logging.StreamHandler(stream)
    formatter = ColoredJsonFormatter(
        fmt=fmt,
        datefmt=datefmt,
        use_colors=use_colors,
    )
    handler.setFormatter(formatter)
    handler.setLevel(level)

    # Configure logger
    logger = logging.getLogger(logger_name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger


# Track which loggers have been configured to avoid duplicate handlers
_configured_loggers: set[str | None] = set()


def get_logger(
    name: str | None = None,
    level: int | str | None = None,
) -> logging.Logger:
    """Get or create a logger with tidylog formatting.

    This is the recommended way to obtain a logger in application code.
    On first call with a given name, configures the logger with
    ColoredJsonFormatter. Subsequent calls return the same logger.

    Args:
        name: Logger name. Typically pass __name__ for module-level logging.
            If None, returns the root logger.
        level: Optional log level to set. If None, defaults to DEBUG on first
            call, or inherits existing level on subsequent calls.

    Returns:
        A configured logging.Logger instance.

    Example:
        >>> from tidylog import get_logger
        >>> logger = get_logger(__name__)
        >>> logger.info("Processing request", extra={"request_id": "abc123"})
    """
    # Check if this logger was already configured by us
    if name not in _configured_loggers:
        effective_level = level if level is not None else logging.DEBUG
        setup_logging(level=effective_level, logger_name=name)
        _configured_loggers.add(name)
    else:
        # Logger already configured, just get it
        logger = logging.getLogger(name)
        # Update level if explicitly provided
        if level is not None:
            if isinstance(level, str):
                level = logging._nameToLevel[level.upper()]
            logger.setLevel(level)
        return logger

    return logging.getLogger(name)


def setup_file_logging(
    log_file: str | Path,
    level: int | str = logging.DEBUG,
    fmt: str | None = None,
    datefmt: str | None = None,
    logger_names: list[str] | None = None,
) -> logging.FileHandler:
    """Configure file-based logging with automatic directory creation.

    Creates a FileHandler with TextFormatter for structured logging to files.
    Automatically creates parent directories if they don't exist.

    Args:
        log_file: Path to the log file. Parent directories are created
            automatically if they don't exist.
        level: Log level as int (e.g., logging.DEBUG) or string ("DEBUG").
            Defaults to logging.DEBUG.
        fmt: Custom format string. Defaults to standard timestamp format.
        datefmt: Custom date format string. Defaults to ISO format.
        logger_names: List of logger names to attach the handler to.
            If None, attaches to root logger only.

    Returns:
        The FileHandler instance (useful for cleanup/removal later).

    Example:
        >>> from tidylog import setup_file_logging
        >>> handler = setup_file_logging("logs/app.log")
        >>> # Later, to remove the handler:
        >>> logging.getLogger().removeHandler(handler)

    Example with multiple loggers:
        >>> handler = setup_file_logging(
        ...     "logs/app.log",
        ...     level="DEBUG",
        ...     logger_names=["myapp", "livekit", "livekit.agents"],
        ... )
    """
    log_path = Path(log_file)
    log_path.parent.mkdir(parents=True, exist_ok=True)

    # Convert string level to int if needed
    if isinstance(level, str):
        level = logging._nameToLevel[level.upper()]

    # Create file handler with text formatter
    file_handler = logging.FileHandler(log_path)
    file_handler.setLevel(level)

    formatter = TextFormatter(fmt=fmt, datefmt=datefmt)
    file_handler.setFormatter(formatter)

    # Attach handler to specified loggers or root logger
    if logger_names:
        for logger_name in logger_names:
            logger = logging.getLogger(logger_name)
            logger.addHandler(file_handler)
            logger.setLevel(level)
    else:
        root_logger = logging.getLogger()
        root_logger.addHandler(file_handler)
        root_logger.setLevel(level)

    return file_handler
