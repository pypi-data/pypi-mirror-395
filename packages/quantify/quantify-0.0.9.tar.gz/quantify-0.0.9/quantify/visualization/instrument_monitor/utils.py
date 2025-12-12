# Repository: https://gitlab.com/quantify-os/quantify
# Licensed according to the LICENSE file on the main branch
"""Utility functions for the instrument monitor."""

import contextlib
from typing import Any

import numpy as np

from quantify.visualization.instrument_monitor.logging_setup import get_logger

logger = get_logger(__name__)


def safe_value_format(value: object) -> str:
    """Value formatting with paths for common types.

    - None -> ""
    - Scalar types -> str
    - Numpy arrays -> scalar if size 1 else array<shape>
    - Sequences (non-strings) -> show "[N items]" if long
    """
    if value is None:
        return ""

    if isinstance(value, (str, int, float, bool)):
        return str(value)

    try:
        if hasattr(value, "__array__"):
            arr = np.asarray(value)
            return str(arr.item()) if arr.size == 1 else f"array{arr.shape}"

        if hasattr(value, "__len__") and not isinstance(value, (str, bytes)):
            size = len(value)  # type: ignore[arg-type]
            return str(value) if size <= 5 else f"[{size} items]"

        return str(value)
    except Exception:
        return f"<{type(value).__name__}>"


def values_equal(val1: Any, val2: Any) -> bool:
    """Compare two values for equality."""
    result = False

    if val1 is val2:
        result = True
    elif val1 is None or val2 is None:
        result = val1 is val2
    elif type(val1) is type(val2) and isinstance(val1, (int, float, str, bool)):
        result = val1 == val2

    # Handle numpy arrays
    try:
        if hasattr(val1, "shape") and hasattr(val2, "shape"):
            result = bool(np.array_equal(val1, val2, equal_nan=True))
    except Exception:
        logger.warning("Failed to compare numpy arrays", exc_info=True)

    with contextlib.suppress(Exception):
        result = bool(val1 == val2)

    return result
