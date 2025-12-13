"""
Dask Resilience - A module for robust Dask operations with automatic recovery.
"""

from .core import (
    _safe_compute,
    _safe_persist,
    _safe_gather,
    _safe_wait,
    dask_is_empty,
    dask_is_probably_empty,
    dask_is_empty_truthful,
    UniqueValuesExtractor,
)

from .client_manager import (
    DaskClientMixin,
    get_persistent_client,
    shared_dask_session,
)

# Define public API
__all__ = [
    # Core operations
    "_safe_compute",
    "_safe_persist",
    "_safe_gather",
    "_safe_wait",
    "dask_is_empty",
    "dask_is_probably_empty",
    "dask_is_empty_truthful",
    "UniqueValuesExtractor",
    # Client management
    "DaskClientMixin",
    "get_persistent_client",
    "shared_dask_session",
]
