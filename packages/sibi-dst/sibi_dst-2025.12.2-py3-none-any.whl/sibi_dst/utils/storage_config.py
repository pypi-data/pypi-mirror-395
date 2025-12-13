from threading import RLock
from typing import Dict, Any
import time

from sibi_dst.utils import Logger
from .credentials import ConfigManager
from .storage_manager import StorageManager


class StorageConfig:
    """
    Initializes filesystem configuration for file, S3, or WebDAV backends.
    Produces a StorageManager instance with proper fsspec options.
    """
    def __init__(self, config: ConfigManager, depots: dict = None,
                 clear_existing: bool = False, write_mode: str = "full-access"):
        self.conf = config
        self.depots = depots
        self._initialize_storage()

        self.storage_manager = StorageManager(
            self.base_storage, self.filesystem_type, self.filesystem_options
        )

        if self.depots is not None:
            (
                self.depot_paths,
                self.depot_names,
            ) = self.storage_manager.rebuild_depot_paths(
                depots,
                clear_existing=clear_existing,
                write_mode=write_mode,
            )
        else:
            self.depot_paths = None
            self.depot_names = None

    def _initialize_storage(self):
        fs_type = self.conf.get("fs_type", "file")
        fs_path = self.conf.get("fs_path", "local_storage/")
        self.filesystem_type = fs_type
        self.base_storage = fs_path

        if fs_type == "file":
            fs_options = {}

        elif fs_type == "s3":
            fs_options = {
                "key": self.conf.get("fs_key", ""),
                "secret": self.conf.get("fs_secret"),
                "token": self.conf.get("fs_token"),
                "skip_instance_cache": True,
                "use_listings_cache": False,
                "client_kwargs": {
                    "endpoint_url": self.conf.get("fs_endpoint")
                },
                "config_kwargs": {
                    "signature_version": "s3v4",
                    "s3": {"addressing_style": "path"},
                },
            }

        elif fs_type == "webdav":
            verify_ssl = self.conf.get("fs_verify_ssl", True)
            if isinstance(verify_ssl, str) and verify_ssl.lower() == "false":
                verify_ssl = False
            fs_options = {
                "base_url": self.conf.get("fs_endpoint", ""),
                "username": self.conf.get("fs_key", ""),
                "password": self.conf.get("fs_secret", ""),
                "token": self.conf.get("fs_token", ""),
                "verify": verify_ssl,
            }

        else:
            # Fallback to local filesystem
            self.filesystem_type = "file"
            fs_options = {}

        # Remove empty values
        self.filesystem_options = {k: v for k, v in fs_options.items() if v}


class FsRegistry:
    """
    Thread-safe registry and cache for filesystem instances.
    Provides TTL-based invalidation and integrates fsspec cache clearing.
    """

    def __init__(self, debug: bool = False, logger: Logger = None, ttl_seconds: int = 3600):
        self._storage_registry: Dict[str, Any] = {}
        self._fs_instance_cache: Dict[str, tuple] = {}  # {name: (fs, timestamp)}
        self._lock = RLock()
        self.ttl_seconds = ttl_seconds

        self.logger = logger or Logger.default_logger(logger_name="FsRegistry")
        self.logger.set_level(Logger.DEBUG if debug else Logger.INFO)
        self.debug = debug

    # ----------------------------------------------------------------------
    # Registration
    # ----------------------------------------------------------------------
    def register(self, name: str, manager: Any):
        """
        Register a storage manager that provides get_fs_instance().
        """
        if not hasattr(manager, "get_fs_instance"):
            raise TypeError("Manager must have a 'get_fs_instance' method.")
        with self._lock:
            self._storage_registry[name] = manager
            self.logger.debug(f"Registered storage '{name}'")

    # ----------------------------------------------------------------------
    # Retrieval
    # ----------------------------------------------------------------------
    def get_fs_instance(self, name: str = "source", reload: bool = False):
        """
        Retrieve a filesystem instance by name.
        - Uses cache unless TTL expired or reload=True.
        - Automatically clears fsspec cache to avoid FileExpired errors.
        """
        now = time.time()
        with self._lock:
            cached = self._fs_instance_cache.get(name)

            # TTL check
            if (
                cached
                and not reload
                and (now - cached[1]) < self.ttl_seconds
            ):
                fs = cached[0]
                return fs

            manager = self._storage_registry.get(name)
            if not manager:
                raise ValueError(
                    f"Storage '{name}' not registered. "
                    f"Available: {list(self._storage_registry.keys())}"
                )

            fs = manager.get_fs_instance()

            # Invalidate fsspec internal cache
            if hasattr(fs, "invalidate_cache"):
                try:
                    fs.invalidate_cache()
                    self.logger.debug(f"Cleared fsspec cache for '{name}'")
                except Exception as e:
                    self.logger.warning(f"Failed to invalidate cache for '{name}': {e}")

            self._fs_instance_cache[name] = (fs, now)
            self.logger.debug(f"Refreshed fs instance for '{name}'")
            return fs

    # ----------------------------------------------------------------------
    # Cache control
    # ----------------------------------------------------------------------
    def invalidate_fs(self, name: str):
        """
        Invalidate and remove cached fs instance for a given name.
        """
        with self._lock:
            if name in self._fs_instance_cache:
                del self._fs_instance_cache[name]
                self.logger.debug(f"Invalidated fs cache for '{name}'")
            else:
                self.logger.debug(f"No cached fs found for '{name}'")

    def clear_fs_cache(self):
        """
        Clear all cached filesystem instances.
        """
        with self._lock:
            self._fs_instance_cache.clear()
            self.logger.debug("Cleared all filesystem caches")

    def unregister_fs(self, name: str):
        """
        Unregister a storage configuration and clear its cached instance.
        """
        with self._lock:
            self._storage_registry.pop(name, None)
            self._fs_instance_cache.pop(name, None)
            self.logger.debug(f"Unregistered storage '{name}' and cleared cache")

