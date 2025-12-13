"""
Utility functions for the dask_resilience package.
"""

import numpy as np
import pandas as pd
from typing import Any


def _to_int_safe(x: Any, default: int = 0) -> int:
    """
    Safely convert a value to integer with fallback defaults.

    Args:
        x: Value to convert to integer
        default: Default value if conversion fails

    Returns:
        Integer value or default if conversion fails
    """
    if x is None:
        return default
    if isinstance(x, (int, np.integer)) and not isinstance(x, bool):
        return int(x)
    if isinstance(x, (float, np.floating)):
        try:
            return int(x)
        except Exception:
            return default
    if isinstance(x, np.generic):
        try:
            return int(x.item())
        except Exception:
            return default
    if isinstance(x, (pd.Series, pd.Index, list, tuple, np.ndarray)):
        try:
            arr = np.asarray(x)
            if arr.size == 0:
                return default
            return _to_int_safe(arr.ravel()[0], default=default)
        except Exception:
            return default
    if hasattr(x, "item"):
        try:
            return _to_int_safe(x.item(), default=default)
        except Exception:
            return default
    if hasattr(x, "iloc"):
        try:
            return _to_int_safe(x.iloc[0], default=default)
        except Exception:
            return default
    try:
        return int(x)
    except Exception:
        return default
