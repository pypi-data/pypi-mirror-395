"""Utility helpers for the backend service."""

from __future__ import annotations

import logging
from typing import Optional

from rich.console import Console
from rich.logging import RichHandler


def get_logger(name: Optional[str] = None) -> logging.Logger:
    """Return a configured logger with Rich formatting.

    Args:
        name: Optional logger name; defaults to the module name.

    Returns:
        Configured logging.Logger instance.
    """

    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = RichHandler(
            rich_tracebacks=True,
            markup=True,
            console=Console(),
        )
        handler.setLevel(logging.INFO)
        logger.setLevel(logging.INFO)
        logger.addHandler(handler)
        logger.propagate = False
    return logger
