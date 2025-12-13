"""
Custom exceptions for the dask_resilience package.
"""

try:
    # distributed >=2024 uses this location
    from distributed.comm.core import CommClosedError  # type: ignore
except ImportError:  # pragma: no cover
    class CommClosedError(Exception):
        """Fallback CommClosedError for older distributed versions."""
        pass

try:
    from tornado.iostream import StreamClosedError  # type: ignore
except ImportError:  # pragma: no cover
    class StreamClosedError(Exception):
        """Fallback StreamClosedError for missing tornado."""
        pass


# Common exception set considered recoverable by rebind-and-retry
RECOVERABLE_COMMS = (
    CommClosedError,
    StreamClosedError,
    TimeoutError,
    ConnectionError,
    OSError,
    RuntimeError,
)