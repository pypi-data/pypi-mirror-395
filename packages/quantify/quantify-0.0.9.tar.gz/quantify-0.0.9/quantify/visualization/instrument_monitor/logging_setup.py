# Repository: https://gitlab.com/quantify-os/quantify
# Licensed according to the LICENSE file on the main branch
"""Logging setup with streamlined formatters."""

from __future__ import annotations

import logging
import sys


def setup_logging(level: str = "INFO") -> None:
    """Setup logging with optimized configuration."""
    logger = logging.getLogger("quantify.instrument_monitor")

    if logger.handlers:
        return
    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%H:%M:%S",
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(level)
    logger.propagate = False


def get_logger(name: str) -> logging.Logger:
    """Get a namespaced logger under 'quantify.instrument_monitor'.

    This ensures that module-level loggers inherit the handler configured by
    ``setup_logging`` which attaches to the ``quantify.instrument_monitor``
    logger. If ``name`` is already fully-qualified with this namespace, it is
    returned unchanged; otherwise it is appended as a child logger.
    """
    ns = "quantify.instrument_monitor"
    if name.startswith(ns):
        return logging.getLogger(name)
    return logging.getLogger(f"{ns}.{name}")
