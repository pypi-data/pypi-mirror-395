"""LiveKit integration for tidylog.

This module provides logging utilities specifically designed for LiveKit
agent applications. It enables per-job log files for easy debugging and
audit trails of interview sessions.

Note:
    This module requires the `livekit-agents` package. Install with:
    pip install tidylog[livekit]
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from tidylog.logger import setup_file_logging

if TYPE_CHECKING:
    try:
        from livekit.agents import JobContext
    except ModuleNotFoundError:

        class JobContext: ...


# Default LiveKit plugin loggers to capture
DEFAULT_LIVEKIT_LOGGERS: list[str] = [
    "livekit",
    "livekit.agents",
    "livekit.plugins.cartesia",
    "livekit.plugins.deepgram",
    "livekit.plugins.openai",
    "livekit.plugins.google",
    "livekit.plugins.silero",
    "livekit.plugins.turn_detector",
]


def setup_job_logging(
    ctx: JobContext,
    log_dir: str = "logs",
    level: int | str = logging.DEBUG,
    fmt: str | None = None,
    logger_names: list[str] | None = None,
    include_livekit_loggers: bool = True,
) -> logging.FileHandler:
    """Configure per-job logging for LiveKit agents.

    Creates a dedicated log file for each LiveKit job/room, making it easy
    to debug and audit individual sessions.

    Args:
        ctx: The LiveKit JobContext containing room information.
        log_dir: Directory for log files. Defaults to "logs".
        level: Log level as int (e.g., logging.DEBUG) or string ("DEBUG").
            Defaults to logging.DEBUG.
        fmt: Custom format string. Defaults to standard timestamp format.
        logger_names: Additional logger names to capture. These are added
            to the default LiveKit loggers if include_livekit_loggers is True.
        include_livekit_loggers: Whether to include default LiveKit plugin
            loggers. Defaults to True.

    Returns:
        The FileHandler instance (useful for cleanup when job ends).

    Example:
        >>> from livekit.agents import JobContext
        >>> from tidylog.livekit import setup_job_logging
        >>>
        >>> async def entrypoint(ctx: JobContext):
        ...     file_handler = setup_job_logging(ctx)
        ...     # Logs are now written to logs/{room_name}.log
        ...     # ... your agent code ...
        ...     # Optionally cleanup when done:
        ...     # logging.getLogger().removeHandler(file_handler)

    Example with custom loggers:
        >>> file_handler = setup_job_logging(
        ...     ctx,
        ...     logger_names=["myapp", "myapp.agents"],
        ...     include_livekit_loggers=True,
        ... )
    """
    log_file = f"{log_dir}/{ctx.room.name}.log"

    # Build list of loggers to capture
    all_loggers: list[str] = []
    if include_livekit_loggers:
        all_loggers.extend(DEFAULT_LIVEKIT_LOGGERS)
    if logger_names:
        all_loggers.extend(logger_names)

    # Use the generic file logging setup
    return setup_file_logging(
        log_file=log_file,
        level=level,
        fmt=fmt,
        logger_names=all_loggers if all_loggers else None,
    )
