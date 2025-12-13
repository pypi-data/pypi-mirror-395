"""
Core functionality for resilient Dask operations.

Key invariants:
- If a Dask Distributed Client is available, compute/persist/gather MUST use it.
- Do NOT fall back to local threaded compute for Dask DataFrame/Series (dask-expr graphs),
  especially after comm failures or cluster recreation; rebuild the collection instead.
- Emptiness probes must be cheap, typed (meta), and non-fatal.
"""

from __future__ import annotations

import asyncio
from typing import Any, Dict, List, Optional

import dask
import dask.dataframe as dd
import numpy as np
import pandas as pd
from dask.distributed import Client, Future

from .utils import _to_int_safe


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def _has_compute(obj: Any) -> bool:
    return hasattr(obj, "compute")


def _is_dask_dataframe_like(obj: Any) -> bool:
    # Covers dd.DataFrame/dd.Series; and conservative check for expr collections
    # that still expose _meta (common in dask-expr).
    return isinstance(obj, (dd.DataFrame, dd.Series)) or hasattr(obj, "_meta")


def _rebind_client(logger=None) -> Optional[Client]:
    from .client_manager import get_persistent_client  # Avoid circular import

    try:
        return get_persistent_client(logger=logger)
    except Exception:
        return None


def _retry_with_rebind(op, *args, dask_client: Optional[Client], logger=None, **kwargs):
    """
    Retry once with a rebound client on recoverable comm failures.

    IMPORTANT:
    - Never attempt local threaded compute fallback for Dask DataFrame/Series graphs;
      those graphs may be orphaned after cluster/client recreation.
    """
    from .client_manager import RECOVERABLE_COMMS  # Avoid circular import

    try:
        return op(*args, dask_client=dask_client, logger=logger, **kwargs)
    except RECOVERABLE_COMMS as e:
        if logger:
            logger.warning("Dask comm closed. Rebinding client and retrying once.")
        c2 = _rebind_client(logger)
        if c2:
            return op(*args, dask_client=c2, logger=logger, **kwargs)

        # No client available: allow local fallback ONLY for non-dataframe objects
        obj = args[0] if args else None
        if obj is not None and _has_compute(obj) and not _is_dask_dataframe_like(obj):
            return obj.compute(scheduler="threads")

        raise RuntimeError(
            "Dask client unavailable after comm failure; cannot safely fallback locally "
            "for Dask DataFrame/expr graphs. Rebuild the collection after recreating the client."
        ) from e


# ---------------------------------------------------------------------------
# Safe compute / persist / gather with auto rebind and safe fallback rules
# ---------------------------------------------------------------------------
def _compute_impl(obj: Any, dask_client: Optional[Client], **_) -> Any:
    if dask_client:
        res = dask_client.compute(obj)
        return res.result() if isinstance(res, Future) else res
    return obj.compute()


def _persist_impl(obj: Any, dask_client: Optional[Client], **_) -> Any:
    if dask_client:
        res = dask_client.persist(obj)
        return res.result() if isinstance(res, Future) else res
    return obj.persist()


def _gather_impl(objs: List[Any], dask_client: Optional[Client], **_) -> List[Any]:
    if dask_client:
        # Compute all at once; avoids per-object scheduler confusion.
        futs = dask_client.compute(objs)
        return dask_client.gather(futs)
    return list(dask.compute(*objs, scheduler="threads"))


def _safe_compute(obj: Any, dask_client: Optional[Client] = None, logger=None) -> Any:
    return _retry_with_rebind(_compute_impl, obj, dask_client=dask_client, logger=logger)


def _safe_persist(obj: Any, dask_client: Optional[Client] = None, logger=None) -> Any:
    return _retry_with_rebind(_persist_impl, obj, dask_client=dask_client, logger=logger)


def _safe_gather(
    objs: List[Any], dask_client: Optional[Client] = None, logger=None
) -> List[Any]:
    """
    Gather results safely.

    IMPORTANT:
    - On comm failures, we rebind once and retry.
    - On Missing dependency (orphaned graph), we DO NOT attempt local recompute for
      dataframe/expr graphs; the caller must rebuild the collection.
    """
    if not objs:
        return []

    from .client_manager import RECOVERABLE_COMMS, _default_logger  # Avoid circular import

    LOG = logger or _default_logger

    try:
        return _gather_impl(objs, dask_client)
    except RECOVERABLE_COMMS as e:
        LOG.warning("Dask comm closed during gather. Rebinding.")
        c2 = _rebind_client(LOG)
        if c2:
            return _gather_impl(objs, c2)

        # No client available: allow local fallback ONLY for non-dataframe objects
        if all(_has_compute(o) and not _is_dask_dataframe_like(o) for o in objs):
            return [o.compute(scheduler="threads") for o in objs]

        raise RuntimeError(
            "Dask gather failed after comm failure and no client could be rebound. "
            "Local fallback is unsafe for Dask DataFrame/expr graphs; rebuild collections."
        ) from e
    except ValueError as e:
        if "Missing dependency" in str(e):
            LOG.error(
                "Detected orphaned Dask graph (Missing dependency). "
                "This typically occurs when a cluster/client is recreated while reusing old "
                "Dask DataFrame/expr objects. Rebuild the collection instead of recomputing."
            )
        raise


def _safe_wait(
    obj: Any,
    dask_client: Optional[Client] = None,
    timeout: Optional[float] = None,
    logger=None,
) -> Any:
    """
    Best-effort wait. Never forces unsafe local fallback for dataframe/expr graphs.
    """
    from .client_manager import _default_logger  # Avoid circular import

    LOG = logger or _default_logger

    if obj is None:
        return None

    try:
        if dask_client:
            from contextlib import suppress

            with suppress(Exception):
                dask_client.wait_for_workers(1, timeout=10)
            dask_client.wait(obj, timeout=timeout)
            return obj

        # No client provided; try to get active distributed client first
        try:
            from dask.distributed import get_client as get_dask_client

            c = get_dask_client()
            c.wait(obj, timeout=timeout)
            return obj
        except Exception:
            # If it is a non-dataframe computable object, allow local compute.
            if _has_compute(obj) and not _is_dask_dataframe_like(obj):
                obj.compute(scheduler="threads")
            return obj
    except Exception as e:
        LOG.warning(f"_safe_wait: {type(e).__name__}: {e}")
        return obj


# ---------------------------------------------------------------------------
# Heuristic emptiness checks
# ---------------------------------------------------------------------------
def dask_is_probably_empty(ddf: dd.DataFrame) -> bool:
    """Check if a Dask DataFrame is probably empty based on metadata."""
    return getattr(ddf, "npartitions", 0) == 0 or len(ddf._meta.columns) == 0


def dask_is_empty_truthful(
    ddf: dd.DataFrame, dask_client: Optional[Client] = None, logger=None
) -> bool:
    """Check if a Dask DataFrame is actually empty by computing the total length."""
    total = _safe_compute(ddf.map_partitions(len, meta=("n", "int64")).sum(), dask_client, logger=logger)
    return int(_to_int_safe(total)) == 0


def dask_is_empty(
    ddf: dd.DataFrame,
    *,
    sample: int = 4,
    dask_client: Optional[Client] = None,
    logger=None,
) -> bool:
    """
    Check if a Dask DataFrame is empty using sampling and fallback methods.

    Non-fatal by design: if probing fails due to comm/orphaned graph issues,
    assume NOT empty to avoid crashing upstream workflows. The caller should
    rebuild the collection if the graph is orphaned.
    """
    if dask_is_probably_empty(ddf):
        return True

    k = min(max(sample, 1), int(getattr(ddf, "npartitions", 0) or 0))
    if k <= 0:
        return True

    try:
        probes = _safe_gather(
            [ddf.get_partition(i).map_partitions(len, meta=("n", "int64")) for i in range(k)],
            dask_client,
            logger=logger,
        )
    except Exception as e:
        if logger:
            logger.warning("dask_is_empty probe failed; assuming not empty: %s", e)
        return False

    if any(_to_int_safe(n) > 0 for n in probes):
        return False
    if k == ddf.npartitions and all(_to_int_safe(n) == 0 for n in probes):
        return True

    try:
        return dask_is_empty_truthful(ddf, dask_client=dask_client, logger=logger)
    except Exception as e:
        if logger:
            logger.warning("dask_is_empty_truthful failed; assuming not empty: %s", e)
        return False


# ---------------------------------------------------------------------------
# Unique value extractor
# ---------------------------------------------------------------------------
class UniqueValuesExtractor:
    """Extract unique values from Dask DataFrame columns with resilience."""

    def __init__(self, dask_client: Optional[Client] = None, logger=None):
        self.dask_client = dask_client
        self.logger = logger

    def _compute_to_list_sync(self, series) -> List[Any]:
        if hasattr(series, "compute"):
            if self.dask_client:
                result = self.dask_client.compute(series).result()
            else:
                result = series.compute()
        else:
            result = series

        if isinstance(result, (np.ndarray, pd.Series, list)):
            return pd.Series(result).dropna().unique().tolist()
        return [result]

    async def compute_to_list(self, series) -> List[Any]:
        return await asyncio.to_thread(self._compute_to_list_sync, series)

    async def extract_unique_values(self, df, *columns: str) -> Dict[str, List[Any]]:
        """Extract unique values from specified columns."""

        async def one(col: str):
            ser = df[col].dropna().unique()
            return col, await self.compute_to_list(ser)

        kv = await asyncio.gather(*(one(c) for c in columns))
        return dict(kv)
