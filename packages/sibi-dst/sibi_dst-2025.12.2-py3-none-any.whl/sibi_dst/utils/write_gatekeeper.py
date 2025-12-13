# write_gatekeeper.py
from __future__ import annotations
import threading

_LOCK = threading.Lock()
_SEMS: dict[str, threading.Semaphore] = {}

def get_write_sem(key: str, max_concurrency: int) -> threading.Semaphore:
    """
    Acquires or creates a semaphore for a given key, ensuring thread-safe access
    and maximum concurrency.

    This function retrieves an existing semaphore associated with the provided
    key or creates a new one if it does not exist. The semaphore limits
    concurrent access based on the provided maximum concurrency value. This is
    used to manage thread-level synchronization for a specific resource or
    operation identified by the given key.

    :param key: The unique identifier for which the semaphore is associated.
    :param max_concurrency: The maximum number of concurrent access allowed. A
                            value less than 1 will default to a concurrency limit
                            of 1.
    :return: A `threading.Semaphore` object for the specified key, initialized
             with the maximum concurrency.
    :rtype: threading.Semaphore
    """
    with _LOCK:
        sem = _SEMS.get(key)
        if sem is None:
            sem = threading.Semaphore(max(1, int(max_concurrency)))
            _SEMS[key] = sem
        return sem