"""
Dask client lifecycle management with shared registry and watchdog.
"""

import asyncio
import json
import logging
import os
import tempfile
import time
from contextlib import asynccontextmanager, contextmanager, suppress
from typing import Optional, Dict, Any

from dask.distributed import Client, LocalCluster, get_client

from .exceptions import RECOVERABLE_COMMS
from .utils import _to_int_safe


# If your project ships a logger helper, import it. Fallback to std logging.
try:
    from sibi_dst.utils import Logger  # type: ignore

    _default_logger = Logger.default_logger(logger_name=__name__)
except ImportError:  # pragma: no cover
    _default_logger = logging.getLogger(__name__)
    if not _default_logger.handlers:
        _default_logger.addHandler(logging.StreamHandler())
    _default_logger.setLevel(logging.INFO)

LOG = _default_logger

# ---------------------------------------------------------------------------
# Global Dask comm timeouts. Conservative to avoid heartbeat failures.
# ---------------------------------------------------------------------------
import dask

dask.config.set(
    {
        "distributed.comm.timeouts.connect": "20s",
        "distributed.comm.timeouts.tcp": "120s",
        "distributed.worker.memory.target": 0.6,
        "distributed.worker.memory.spill": 0.7,
        "distributed.worker.memory.pause": 0.8,
        "distributed.scheduler.allowed-failures": 3,
        "distributed.deploy.lost-worker-timeout": "60s",
    }
)


class DaskClientMixin:
    """Mixin class for Dask client lifecycle management with shared registry and watchdog."""

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
    def _read_registry(cls) -> Optional[Dict[str, Any]]:
        """Read cluster registry from file."""
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
    def _write_registry(cls, data: Dict[str, Any]) -> None:
        """Write cluster registry to file."""
        tmp = cls.REGISTRY_PATH + ".tmp"
        with open(tmp, "w") as f:
            json.dump(data, f)
        os.replace(tmp, cls.REGISTRY_PATH)

    @classmethod
    def _remove_registry(cls) -> None:
        """Remove cluster registry file."""
        with suppress(FileNotFoundError):
            os.remove(cls.REGISTRY_PATH)

    @classmethod
    def _cleanup_stale_registry(cls, logger_obj=None) -> None:
        """Clean up stale registry entries."""
        reg = cls._read_registry()
        if not reg:
            return
        try:
            c = Client(address=reg["address"], timeout=5)
            c.scheduler_info()
            c.close()
        except Exception:
            if logger_obj:
                logger_obj.warning(
                    f"Stale Dask registry at {reg.get('address')}. Removing."
                )
            cls._remove_registry()

    # ---------- helpers ----------
    @staticmethod
    def _has_inflight(client: Client) -> bool:
        """Check if client has inflight tasks."""
        try:
            info = client.scheduler_info()
            processing = sum(len(v) for v in info.get("processing", {}).values())
            n_tasks = info.get("tasks", 0) or len(info.get("task_counts", {}))
            return bool(processing or n_tasks)
        except Exception:
            return False

    @staticmethod
    def _retire_all_workers(client: Client) -> None:
        """Retire all workers in the cluster."""
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
        resources: Optional[Dict[str, Any]] = None,
        timeout: int = 30,
        watchdog: bool = True,
        dashboard_address: str = ":0"
    ) -> None:
        """Initialize Dask client with resilience features."""
        self.logger = logger or self.logger

        # Reduce noisy logs
        logging.getLogger("distributed.scheduler").setLevel(logging.WARNING)
        logging.getLogger("distributed.worker").setLevel(logging.WARNING)
        logging.getLogger("distributed.comm").setLevel(logging.ERROR)
        logging.getLogger("distributed.batched").setLevel(logging.ERROR)
        logging.getLogger("distributed.shuffle._scheduler_plugin").setLevel(
            logging.ERROR
        )

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
                self.logger.info(
                    f"Connected to external scheduler {scheduler_address}. Dashboard: {self.dask_client.dashboard_link}"
                )
                if watchdog:
                    self._start_watchdog()
                return
            except Exception as e:
                self.logger.warning(
                    f"Remote connect failed: {e}. Falling back to local."
                )

        # 3) shared local cluster via registry
        # Use a simple file lock implemented with portalocker-like fallback.
        # We avoid external deps by retrying write operations.
        for _ in range(20):
            try:
                # crude lock by creating a temp lock file exclusively
                fd = os.open(
                    self.REGISTRY_LOCK_PATH, os.O_CREAT | os.O_EXCL | os.O_WRONLY
                )
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
                    self.logger.info(
                        f"Reusing LocalCluster at {reg['address']} (refcount={reg['refcount']})."
                    )
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
                asynchronous=False,  # keep sync client to avoid loop crossings
                memory_limit=memory_limit,
                local_directory=local_directory,
                silence_logs=silence_logs,
                resources=resources,
                timeout=timeout,
                dashboard_address=dashboard_address,
            )
            self.dask_client = Client(cluster)
            self.own_dask_client = True

            reg = {
                "address": cluster.scheduler_address,
                "refcount": 1,
                "closing": False,
            }
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
        """Start the watchdog task to monitor client health."""

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
        """Reattach to existing cluster or recreate if needed."""
        # Small critical section to avoid concurrent recreations
        for _ in range(20):
            try:
                fd = os.open(
                    self.REGISTRY_LOCK_PATH, os.O_CREAT | os.O_EXCL | os.O_WRONLY
                )
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
            self._write_registry(
                {"address": cluster.scheduler_address, "refcount": 1, "closing": False}
            )
            self.logger.info("Recreated LocalCluster.")
        finally:
            if have_lock:
                with suppress(Exception):
                    os.remove(self.REGISTRY_LOCK_PATH)

    def _force_close_persistent_cluster(self) -> None:
        """Force close the persistent cluster regardless of reference count."""
        if not self.dask_client:
            return

        # acquire simple file lock
        for _ in range(20):
            try:
                fd = os.open(
                    self.REGISTRY_LOCK_PATH, os.O_CREAT | os.O_EXCL | os.O_WRONLY
                )
                os.close(fd)
                have_lock = True
            except FileExistsError:
                time.sleep(0.05)
                continue
            break
        else:
            have_lock = False

        try:
            # Force set refcount to 0 and mark as closing
            if os.path.exists(self.REGISTRY_PATH):
                reg = self._read_registry()
                if reg:
                    reg["refcount"] = 0
                    reg["closing"] = True
                    self._write_registry(reg)

            # Close the cluster
            client = self.dask_client
            cluster = getattr(client, "cluster", None)

            self._retire_all_workers(client)
            time.sleep(1.0)  # allow heartbeats to stop before scheduler closes

            with suppress(Exception):
                client.close()
            with suppress(Exception):
                if cluster:
                    cluster.close()

            self._remove_registry()
            self.dask_client = None

        finally:
            if have_lock:
                with suppress(Exception):
                    os.remove(self.REGISTRY_LOCK_PATH)

    async def _stop_watchdog(self) -> None:
        """Stop the watchdog task."""
        self._watchdog_stop.set()
        if self._watchdog_task:
            with suppress(Exception):
                await asyncio.wait([self._watchdog_task], timeout=5)
            self._watchdog_task = None

    # ---------- close ----------
    def _close_dask_client(self) -> None:
        """Close the Dask client with proper cleanup."""
        if not self.dask_client:
            return

        # acquire simple file lock
        for _ in range(20):
            try:
                fd = os.open(
                    self.REGISTRY_LOCK_PATH, os.O_CREAT | os.O_EXCL | os.O_WRONLY
                )
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
                self.logger.warning(
                    "Close requested with inflight tasks; skipping close."
                )
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
                        time.sleep(
                            1.0
                        )  # allow heartbeats to stop before scheduler closes
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
    n_workers: int = 4,
    threads_per_worker: int = 2,
    processes: bool = False,
    memory_limit: str = "auto",
    local_directory: Optional[str] = None,
    silence_logs: int = logging.WARNING,
    resources: Optional[Dict[str, Any]] = None,
    timeout: int = 30,
    watchdog: bool = True,
    dashboard_address: str = ":0",
) -> Client:
    """Get a persistent Dask client with shared cluster management."""
    global _persistent_mixin
    if _persistent_mixin is None or _persistent_mixin.dask_client is None:
        _persistent_mixin = DaskClientMixin(logger=logger or _default_logger)
        _persistent_mixin._init_dask_client(
            use_remote_cluster=use_remote_cluster,
            scheduler_address=scheduler_address,
            n_workers=n_workers,
            threads_per_worker=threads_per_worker,
            processes=processes,
            memory_limit=memory_limit,
            local_directory=local_directory,
            silence_logs=silence_logs,
            resources=resources,
            timeout=timeout,
            watchdog=watchdog,
            dashboard_address=dashboard_address
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

# Add a global function to force close persistent client
def force_close_persistent_client():
    """Force close the persistent client and cluster."""
    global _persistent_mixin
    if _persistent_mixin:
        _persistent_mixin._force_close_persistent_cluster()
        _persistent_mixin = None
