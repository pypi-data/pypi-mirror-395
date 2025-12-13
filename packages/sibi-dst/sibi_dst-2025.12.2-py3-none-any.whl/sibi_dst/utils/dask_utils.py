
from __future__ import annotations

import asyncio
import json
import logging
import os
import tempfile
import time
from contextlib import asynccontextmanager, contextmanager, suppress
from typing import Any, Dict, List, Optional, Tuple

import dask
import dask.dataframe as dd
import numpy as np
import pandas as pd
from dask.distributed import Client, LocalCluster, Future, get_client

try:
    # distributed >=2024 uses this location
    from distributed.comm.core import CommClosedError  # type: ignore
except Exception:  # pragma: no cover
    class CommClosedError(Exception):
        ...

try:
    from tornado.iostream import StreamClosedError  # type: ignore
except Exception:  # pragma: no cover
    class StreamClosedError(Exception):
        ...

# If your project ships a logger helper, import it. Fallback to std logging.
try:
    from sibi_dst.utils import Logger  # type: ignore
    _default_logger = Logger.default_logger(logger_name=__name__)
except Exception:  # pragma: no cover
    _default_logger = logging.getLogger(__name__)
    if not _default_logger.handlers:
        _default_logger.addHandler(logging.StreamHandler())
    _default_logger.setLevel(logging.INFO)

LOG = _default_logger

# ---------------------------------------------------------------------------
# Global Dask comm timeouts. Conservative to avoid heartbeat failures.
# ---------------------------------------------------------------------------
dask.config.set({
    "distributed.comm.timeouts.connect": "20s",
    "distributed.comm.timeouts.tcp": "120s",
    "distributed.worker.memory.target": 0.6,
    "distributed.worker.memory.spill": 0.7,
    "distributed.worker.memory.pause": 0.8,
    "distributed.scheduler.allowed-failures": 3,
    "distributed.deploy.lost-worker-timeout": "60s",
})

# ---------------------------------------------------------------------------
# Common exception set considered recoverable by rebind-and-retry.
# ---------------------------------------------------------------------------
RECOVERABLE_COMMS = (
    CommClosedError,
    StreamClosedError,
    TimeoutError,
    ConnectionError,
    OSError,
    RuntimeError,
)

# ---------------------------------------------------------------------------
# Numeric coercion
# ---------------------------------------------------------------------------
def _to_int_safe(x: Any, default: int = 0) -> int:
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

# ---------------------------------------------------------------------------
# Safe compute / persist / gather with auto rebind and local fallback
# ---------------------------------------------------------------------------
def _rebind_client(logger=_default_logger) -> Optional[Client]:
    try:
        return get_persistent_client(logger=logger)
    except Exception:
        return None

def _retry_with_rebind(op, *args, dask_client: Optional[Client], logger=_default_logger, **kwargs):
    try:
        return op(*args, dask_client=dask_client, logger=logger, **kwargs)
    except RECOVERABLE_COMMS:
        logger.warning("Dask comm closed. Rebinding client and retrying once.")
        c2 = _rebind_client(logger)
        if c2:
            return op(*args, dask_client=c2, logger=logger, **kwargs)
        # Last resort: local compute path if applicable
        obj = args[0] if args else None
        if hasattr(obj, "compute"):
            return obj.compute(scheduler="threads")
        raise

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
        futs = [dask_client.compute(o) for o in objs]
        return dask_client.gather(futs)
    return list(dask.compute(*objs, scheduler="threads"))

def _safe_compute(obj: Any, dask_client: Optional[Client] = None) -> Any:
    return _retry_with_rebind(_compute_impl, obj, dask_client=dask_client)

def _safe_persist(obj: Any, dask_client: Optional[Client] = None) -> Any:
    return _retry_with_rebind(_persist_impl, obj, dask_client=dask_client)

def _safe_gather(objs: List[Any], dask_client: Optional[Client] = None) -> List[Any]:
    if not objs:
        return []
    try:
        return _gather_impl(objs, dask_client)
    except RECOVERABLE_COMMS:
        LOG.warning("Dask comm closed during gather. Rebinding.")
        c2 = _rebind_client(LOG)
        if c2:
            return _gather_impl(objs, c2)
        return list(dask.compute(*objs, scheduler="threads"))
    except ValueError as e:
        if "Missing dependency" in str(e):
            LOG.warning("Detected orphaned Dask graph. Recomputing locally.")
            try:
                return [o.compute(scheduler="threads") for o in objs]
            except Exception as inner:
                LOG.error(f"Local recompute failed: {inner}")
                raise
        raise

def _safe_wait(obj: Any, dask_client: Optional[Client] = None, timeout: Optional[float] = None) -> Any:
    if obj is None:
        return None
    try:
        if dask_client:
            with suppress(Exception):
                dask_client.wait_for_workers(1, timeout=10)
            dask_client.wait(obj, timeout=timeout)
            return obj
        try:
            c = get_client()
            c.wait(obj, timeout=timeout)
            return obj
        except ValueError:
            if hasattr(obj, "compute"):
                obj.compute(scheduler="threads")
            return obj
    except Exception as e:
        LOG.warning(f"_safe_wait: {type(e).__name__}: {e}")
        return obj

# ---------------------------------------------------------------------------
# Heuristic emptiness checks
# ---------------------------------------------------------------------------
def dask_is_probably_empty(ddf: dd.DataFrame) -> bool:
    return getattr(ddf, "npartitions", 0) == 0 or len(ddf._meta.columns) == 0

def dask_is_empty_truthful(ddf: dd.DataFrame, dask_client: Optional[Client] = None) -> bool:
    total = _safe_compute(ddf.map_partitions(len).sum(), dask_client)
    return int(_to_int_safe(total)) == 0

def dask_is_empty(ddf: dd.DataFrame, *, sample: int = 4, dask_client: Optional[Client] = None) -> bool:
    if dask_is_probably_empty(ddf):
        return True
    k = min(max(sample, 1), ddf.npartitions)
    probes = _safe_gather([ddf.get_partition(i).map_partitions(len) for i in range(k)], dask_client)
    if any(_to_int_safe(n) > 0 for n in probes):
        return False
    if k == ddf.npartitions and all(_to_int_safe(n) == 0 for n in probes):
        return True
    return dask_is_empty_truthful(ddf, dask_client=dask_client)

# ---------------------------------------------------------------------------
# Unique value extractor
# ---------------------------------------------------------------------------
class UniqueValuesExtractor:
    def __init__(self, dask_client: Optional[Client] = None):
        self.dask_client = dask_client

    def _compute_to_list_sync(self, series) -> List[Any]:
        if hasattr(series, "compute"):
            result = self.dask_client.compute(series).result() if self.dask_client else series.compute()
        else:
            result = series
        if isinstance(result, (np.ndarray, pd.Series, list)):
            return pd.Series(result).dropna().unique().tolist()
        return [result]

    async def compute_to_list(self, series) -> List[Any]:
        return await asyncio.to_thread(self._compute_to_list_sync, series)

    async def extract_unique_values(self, df, *columns: str) -> Dict[str, List[Any]]:
        async def one(col: str):
            ser = df[col].dropna().unique()
            return col, await self.compute_to_list(ser)
        kv = await asyncio.gather(*(one(c) for c in columns))
        return dict(kv)

# ---------------------------------------------------------------------------
# Dask client lifecycle with shared registry and watchdog
# ---------------------------------------------------------------------------
class DaskClientMixin:
    REGISTRY_PATH = os.path.join(tempfile.gettempdir(), "shared_dask_cluster.json")
    REGISTRY_LOCK_PATH = REGISTRY_PATH + ".lock"
    WATCHDOG_INTERVAL = 30  # seconds

    def __init__(self, **kwargs):
        self.dask_client: Optional[Client] = None
        self.own_dask_client = False
        self.logger = kwargs.get("logger", _default_logger)
        self._watchdog_task: Optional[asyncio.Task] = None
        self._watchdog_stop = asyncio.Event()

    # ---------- registry ----------
    @classmethod
    def _read_registry(cls) -> Optional[dict]:
        if not os.path.exists(cls.REGISTRY_PATH):
            return None
        try:
            with open(cls.REGISTRY_PATH, "r") as f:
                data = json.load(f)
            if not isinstance(data, dict) or "address" not in data:
                return None
            return data
        except (json.JSONDecodeError, OSError):
            return None

    @classmethod
    def _write_registry(cls, data: dict) -> None:
        tmp = cls.REGISTRY_PATH + ".tmp"
        with open(tmp, "w") as f:
            json.dump(data, f)
        os.replace(tmp, cls.REGISTRY_PATH)

    @classmethod
    def _remove_registry(cls) -> None:
        with suppress(FileNotFoundError):
            os.remove(cls.REGISTRY_PATH)

    @classmethod
    def _cleanup_stale_registry(cls, logger_obj=None) -> None:
        reg = cls._read_registry()
        if not reg:
            return
        try:
            c = Client(address=reg["address"], timeout=5)
            c.scheduler_info()
            c.close()
        except Exception:
            if logger_obj:
                logger_obj.warning(f"Stale Dask registry at {reg.get('address')}. Removing.")
            cls._remove_registry()

    # ---------- helpers ----------
    @staticmethod
    def _has_inflight(client: Client) -> bool:
        try:
            info = client.scheduler_info()
            processing = sum(len(v) for v in info.get("processing", {}).values())
            n_tasks = info.get("tasks", 0) or len(info.get("task_counts", {}))
            return bool(processing or n_tasks)
        except Exception:
            return False

    @staticmethod
    def _retire_all_workers(client: Client) -> None:
        with suppress(Exception):
            client.retire_workers(workers=None, close_workers=True, remove=True)

    # ---------- init ----------
    def _init_dask_client(
        self,
        dask_client: Optional[Client] = None,
        *,
        logger: Optional[logging.Logger] = None,
        scheduler_address: Optional[str] = None,
        use_remote_cluster: bool = False,
        n_workers: int = 4,
        threads_per_worker: int = 2,
        processes: bool = False,
        memory_limit: str = "auto",
        local_directory: Optional[str] = None,
        silence_logs: int = logging.WARNING,
        resources: Optional[dict] = None,
        timeout: int = 30,
        watchdog: bool = True,
    ) -> None:
        self.logger = logger or self.logger

        # Reduce noisy logs
        logging.getLogger("distributed.scheduler").setLevel(logging.WARNING)
        logging.getLogger("distributed.worker").setLevel(logging.WARNING)
        logging.getLogger("distributed.comm").setLevel(logging.ERROR)
        logging.getLogger("distributed.batched").setLevel(logging.ERROR)
        logging.getLogger("distributed.shuffle._scheduler_plugin").setLevel(logging.ERROR)

        self.dask_client = dask_client
        self.own_dask_client = False

        # 1) try in-context client
        if self.dask_client is None:
            with suppress(ValueError, RuntimeError):
                self.dask_client = get_client()

        # 2) remote scheduler
        if self.dask_client is None and use_remote_cluster and scheduler_address:
            try:
                self.dask_client = Client(address=scheduler_address, timeout=timeout)
                self.own_dask_client = True
                self.logger.info(f"Connected to external scheduler {scheduler_address}. Dashboard: {self.dask_client.dashboard_link}")
                if watchdog:
                    self._start_watchdog()
                return
            except Exception as e:
                self.logger.warning(f"Remote connect failed: {e}. Falling back to local.")

        # 3) shared local cluster via registry
        # Use a simple file lock implemented with portalocker-like fallback.
        # We avoid external deps by retrying write operations.
        for _ in range(20):
            try:
                # crude lock by creating a temp lock file exclusively
                fd = os.open(self.REGISTRY_LOCK_PATH, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
                os.close(fd)
                have_lock = True
            except FileExistsError:
                time.sleep(0.05)
                continue
            break
        else:
            have_lock = False

        try:
            self._cleanup_stale_registry(self.logger)
            reg = self._read_registry()
            if reg and not reg.get("closing"):
                try:
                    self.dask_client = Client(address=reg["address"], timeout=timeout)
                    reg["refcount"] = int(reg.get("refcount", 0)) + 1
                    self._write_registry(reg)
                    self.logger.info(f"Reusing LocalCluster at {reg['address']} (refcount={reg['refcount']}).")
                    if watchdog:
                        self._start_watchdog()
                    return
                except Exception:
                    self.logger.warning("Registry address unreachable. Recreating.")
                    self._remove_registry()

            cluster = LocalCluster(
                n_workers=n_workers,
                threads_per_worker=threads_per_worker,
                processes=processes,
                asynchronous=False,          # keep sync client to avoid loop crossings
                memory_limit=memory_limit,
                local_directory=local_directory,
                silence_logs=silence_logs,
                resources=resources,
                timeout=timeout,
            )
            self.dask_client = Client(cluster)
            self.own_dask_client = True

            reg = {"address": cluster.scheduler_address, "refcount": 1, "closing": False}
            self._write_registry(reg)
            self.logger.info(
                f"Started LocalCluster {reg['address']} ({n_workers} workers x {threads_per_worker} threads). "
                f"Dashboard: {self.dask_client.dashboard_link}"
            )
        finally:
            if have_lock:
                with suppress(Exception):
                    os.remove(self.REGISTRY_LOCK_PATH)

        if watchdog:
            self._start_watchdog()

    # ---------- watchdog ----------
    def _start_watchdog(self) -> None:
        async def watchdog_loop():
            while not self._watchdog_stop.is_set():
                await asyncio.sleep(self.WATCHDOG_INTERVAL)
                try:
                    c = self.dask_client
                    if not c:
                        raise RuntimeError("No client bound.")
                    # Exercise both scheduler RPC and worker comms
                    c.scheduler_info()
                    with suppress(Exception):
                        c.run(lambda: 1)
                    # Ask workers to GC to reduce unmanaged memory pressure
                    with suppress(Exception):
                        c.run(lambda: __import__("gc").collect())
                except Exception:
                    self.logger.warning("Watchdog: comm unhealthy. Reattaching.")
                    try:
                        self._reattach_or_recreate()
                    except Exception as e:
                        self.logger.error(f"Watchdog reattach failed: {e}")

        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                self._watchdog_task = loop.create_task(watchdog_loop())
                self.logger.debug("Started Dask watchdog.")
        except RuntimeError:
            self.logger.debug("Watchdog not started. No running loop.")

    def _reattach_or_recreate(self) -> None:
        # Small critical section to avoid concurrent recreations
        for _ in range(20):
            try:
                fd = os.open(self.REGISTRY_LOCK_PATH, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
                os.close(fd)
                have_lock = True
            except FileExistsError:
                time.sleep(0.05)
                continue
            break
        else:
            have_lock = False

        try:
            self._cleanup_stale_registry(self.logger)
            reg = self._read_registry()
            if reg and not reg.get("closing"):
                self.dask_client = Client(address=reg["address"], timeout=10)
                self.logger.info("Reattached to existing LocalCluster.")
                return

            cluster = LocalCluster(
                n_workers=2,
                threads_per_worker=1,
                processes=False,
                asynchronous=False,
                silence_logs=logging.WARNING,
            )
            self.dask_client = Client(cluster)
            self.own_dask_client = True
            self._write_registry({"address": cluster.scheduler_address, "refcount": 1, "closing": False})
            self.logger.info("Recreated LocalCluster.")
        finally:
            if have_lock:
                with suppress(Exception):
                    os.remove(self.REGISTRY_LOCK_PATH)

    async def _stop_watchdog(self) -> None:
        self._watchdog_stop.set()
        if self._watchdog_task:
            with suppress(Exception):
                await asyncio.wait([self._watchdog_task], timeout=5)
            self._watchdog_task = None

    # ---------- close ----------
    def _close_dask_client(self) -> None:
        if not self.dask_client:
            return

        # acquire simple file lock
        for _ in range(20):
            try:
                fd = os.open(self.REGISTRY_LOCK_PATH, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
                os.close(fd)
                have_lock = True
            except FileExistsError:
                time.sleep(0.05)
                continue
            break
        else:
            have_lock = False

        try:
            reg = self._read_registry()
            client = self.dask_client
            cluster = getattr(client, "cluster", None)

            # Do not close if tasks still inflight
            if self._has_inflight(client):
                self.logger.warning("Close requested with inflight tasks; skipping close.")
                return

            if reg and "refcount" in reg:
                reg["refcount"] = max(0, int(reg["refcount"]) - 1)
                if reg["refcount"] == 0:
                    self.logger.info("Refcount reached 0. Closing LocalCluster.")
                    reg["closing"] = True
                    self._write_registry(reg)

                    # Drain deterministically
                    deadline = time.time() + 20
                    try:
                        while self._has_inflight(client) and time.time() < deadline:
                            time.sleep(0.25)
                        self._retire_all_workers(client)
                        time.sleep(1.0)  # allow heartbeats to stop before scheduler closes
                    except Exception:
                        pass

                    with suppress(Exception):
                        client.close()
                    with suppress(Exception):
                        if cluster:
                            cluster.close()

                    self._remove_registry()
                else:
                    self._write_registry(reg)
                    self.logger.debug(f"Decremented refcount to {reg['refcount']}.")
            else:
                if self.own_dask_client:
                    with suppress(Exception):
                        self._retire_all_workers(client)
                    with suppress(Exception):
                        client.close()
                    with suppress(Exception):
                        if cluster:
                            cluster.close()
                self.logger.debug("Closed client without registry tracking.")
        finally:
            if have_lock:
                with suppress(Exception):
                    os.remove(self.REGISTRY_LOCK_PATH)

        # stop watchdog
        if self._watchdog_task:
            asyncio.create_task(self._stop_watchdog())

# ---------------------------------------------------------------------------
# Persistent singleton
# ---------------------------------------------------------------------------
_persistent_mixin: Optional[DaskClientMixin] = None

def get_persistent_client(
    *,
    logger: Optional[logging.Logger] = None,
    use_remote_cluster: bool = False,
    scheduler_address: Optional[str] = None,
) -> Client:
    global _persistent_mixin
    if _persistent_mixin is None or _persistent_mixin.dask_client is None:
        _persistent_mixin = DaskClientMixin(logger=logger or _default_logger)
        _persistent_mixin._init_dask_client(
            use_remote_cluster=use_remote_cluster,
            scheduler_address=scheduler_address,
            n_workers=4,
            threads_per_worker=2,
            processes=False,
            watchdog=True,
        )
    return _persistent_mixin.dask_client  # type: ignore[return-value]

# ---------------------------------------------------------------------------
# Shared session contexts
# ---------------------------------------------------------------------------
def shared_dask_session(*, async_mode: bool = True, **kwargs):
    """
    Context manager for shared Dask client with refcounted LocalCluster.
    """
    mixin = DaskClientMixin()
    mixin._init_dask_client(**kwargs)

    if async_mode:
        @asynccontextmanager
        async def _async_manager():
            try:
                yield mixin.dask_client
            finally:
                mixin._close_dask_client()
        return _async_manager()
    else:
        @contextmanager
        def _sync_manager():
            try:
                yield mixin.dask_client
            finally:
                mixin._close_dask_client()
        return _sync_manager()


