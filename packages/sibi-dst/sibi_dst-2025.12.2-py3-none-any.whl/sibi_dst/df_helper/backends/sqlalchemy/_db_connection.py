from __future__ import annotations

import os
import threading
import weakref
from typing import Any, Dict, Optional, Type

from pydantic import (
    BaseModel,
    Field,
    PrivateAttr,
    ConfigDict,
    SecretStr,
    model_validator,
)
from sqlalchemy import create_engine
from sqlalchemy.engine import url as sqlalchemy_url
from sqlalchemy.engine import Engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import QueuePool, NullPool, StaticPool, Pool

from sibi_dst.utils import Logger
from ._sql_model_builder import SqlAlchemyModelBuilder

# --- Global Engine Registry ---
_ENGINE_REGISTRY_LOCK = threading.RLock()
_ENGINE_REGISTRY: Dict[tuple, Any] = {}


def _release_engine_resource(key: tuple, logger: Optional[Logger] = None) -> None:
    """
    Standalone clean-up function for weakref.finalize.

    This function handles the reference counting decrement and disposal.
    It includes guards for interpreter shutdown scenarios where globals
    might already be set to None.
    """
    # Guard: Check if globals are None (happens during interpreter shutdown)
    if _ENGINE_REGISTRY_LOCK is None or _ENGINE_REGISTRY is None:
        return

    with _ENGINE_REGISTRY_LOCK:
        if key in _ENGINE_REGISTRY:
            wrapper = _ENGINE_REGISTRY[key]
            wrapper["ref_count"] -= 1

            if logger:
                try:
                    logger.debug(
                        f"Decremented DB Engine ref count to {wrapper['ref_count']} for key {key}"
                    )
                except (AttributeError, OSError, ValueError):
                    # Swallow specific errors:
                    # AttributeError: Logger internals might be None during shutdown.
                    # OSError/ValueError: Logging stream might be closed.
                    pass

            if wrapper["ref_count"] <= 0:
                try:
                    wrapper["engine"].dispose()
                    if logger:
                        try:
                            logger.debug(f"Disposed DB Engine for key {key}")
                        except (AttributeError, OSError, ValueError):
                            pass
                except (SQLAlchemyError, AttributeError, OSError):
                    # SQLAlchemyError: DB driver issues.
                    # AttributeError/OSError: Underlying socket/module clean-up issues.
                    pass
                finally:
                    # Safe removal using pop
                    _ENGINE_REGISTRY.pop(key, None)


class SqlAlchemyConnectionConfig(BaseModel):
    """
    Immutable, thread-safe SQLAlchemy connection manager.

    Architectural improvements:
    - Uses weakref for deterministic engine clean-up (fixes __del__ instability).
    - frozen=True prevents race conditions on configuration mutation.
    - pool_pre_ping=True replaces manual SELECT 1 validation (fixes Oracle compatibility).
    - SecretStr prevents password leakage in logs.
    """

    # --- Configuration ---
    model_config = ConfigDict(
        frozen=True,  # Immutable state for thread safety
        arbitrary_types_allowed=True,  # Allow complex types in PrivateAttr
        extra="forbid",  # Strict config validation
    )

    connection_url: SecretStr = Field(..., description="Database DSN (masked in logs)")
    table: Optional[str] = None
    debug: bool = False
    logger_extra: Optional[Dict[str, Any]] = Field(
        default_factory=lambda: {"sibi_dst_component": __name__}
    )

    # --- Pool Configuration (Validated) ---
    pool_size: int = Field(
        default_factory=lambda: int(os.environ.get("DB_POOL_SIZE", 5)), ge=0
    )
    max_overflow: int = Field(
        default_factory=lambda: int(os.environ.get("DB_MAX_OVERFLOW", 10)), ge=0
    )
    pool_timeout: int = Field(
        default_factory=lambda: int(os.environ.get("DB_POOL_TIMEOUT", 30)), ge=0
    )
    pool_recycle: int = Field(
        default_factory=lambda: int(os.environ.get("DB_POOL_RECYCLE", 1800)),
        description="Recycle connections before firewall timeouts (seconds)",
    )
    pool_pre_ping: bool = Field(
        default=True,
        description="Enables pessimistic disconnect handling (SELECT 1 check)",
    )
    poolclass: Type[Pool] = QueuePool

    # --- Runtime State (Private & Excluded from Serialization) ---
    _model: Optional[Any] = PrivateAttr(default=None)
    _engine: Optional[Engine] = PrivateAttr(default=None)
    _logger: Optional[Logger] = PrivateAttr(default=None)
    _session_factory: Optional[sessionmaker] = PrivateAttr(default=None)
    _engine_key_instance: Optional[tuple] = PrivateAttr(default=None)

    # Hold the finaliser to ensure it remains active as long as this object is alive
    _finalizer: Any = PrivateAttr(default=None)

    @model_validator(mode="after")
    def _initialize_resources(self) -> "SqlAlchemyConnectionConfig":
        """
        Initialises the Engine, Logger, and Model upon validation.
        Since the model is frozen, we must set PrivateAttr directly.
        """
        # 1. Setup Logger
        if self._logger is None:
            logger = Logger.default_logger(logger_name=self.__class__.__name__)
            logger.set_level(Logger.DEBUG if self.debug else Logger.INFO)
            self._logger = logger

        # 2. Generate Engine Key
        self._engine_key_instance = self._get_engine_key()

        # 3. Initialise or Acquire Engine
        self._init_engine()

        # 4. Build Model (if table specified)
        if self.table and self._engine:
            self._build_model()

        # 5. Create Session Factory
        if self._engine:
            self._session_factory = sessionmaker(
                bind=self._engine, expire_on_commit=False
            )

        return self

    def _get_engine_key(self) -> tuple:
        """
        Generates a unique key for the engine registry based on connection params.
        """
        # Unwrap SecretStr for internal use
        url_str = self.connection_url.get_secret_value()
        parsed = sqlalchemy_url.make_url(url_str)

        # Normalize query params to ensure consistent keys
        query = {k: v for k, v in parsed.query.items() if not k.startswith("pool_")}
        normalized_url = parsed.set(query=query)

        # Note: Depending on security requirements, one might want to hash this
        # URL string if it's ever logged, but for internal registry keys it is safe.
        key_parts: list[Any] = [str(normalized_url)]

        # Only include pool params if we are using a pool that supports them
        if self.poolclass not in (NullPool, StaticPool):
            key_parts.extend(
                [
                    self.pool_size,
                    self.max_overflow,
                    self.pool_timeout,
                    self.pool_recycle,
                    self.pool_pre_ping,
                ]
            )

        return tuple(key_parts)

    def _init_engine(self) -> None:
        """
        Acquires an engine from the global registry or creates a new one.
        Registers a weakref finalizer for clean-up.
        """
        key = self._engine_key_instance

        with _ENGINE_REGISTRY_LOCK:
            wrapper = _ENGINE_REGISTRY.get(key)
            if wrapper:
                self._engine = wrapper["engine"]
                wrapper["ref_count"] += 1
                if self.debug:
                    self._logger.debug(
                        f"Reusing DB engine. Ref count: {wrapper['ref_count']}",
                        extra=self.logger_extra,
                    )
            else:
                if self.debug:
                    self._logger.debug(
                        f"Creating new DB engine for key: {key}",
                        extra=self.logger_extra,
                    )
                try:
                    new_engine = create_engine(
                        self.connection_url.get_secret_value(),
                        pool_size=self.pool_size,
                        max_overflow=self.max_overflow,
                        pool_timeout=self.pool_timeout,
                        pool_recycle=self.pool_recycle,
                        pool_pre_ping=self.pool_pre_ping,
                        poolclass=self.poolclass,
                    )

                    _ENGINE_REGISTRY[key] = {
                        "engine": new_engine,
                        "ref_count": 1,
                        "active_connections": 0,
                    }
                    self._engine = new_engine
                except Exception as e:
                    self._logger.error(
                        f"Failed to create DB engine: {e}", extra=self.logger_extra
                    )
                    raise SQLAlchemyError(f"DB Engine creation failed: {e}") from e

        # Register clean-up to run when THIS instance is 'garbage collected'.
        # We pass the key and the global clean-up function, NOT a bound method.
        self._finalizer = weakref.finalize(
            self, _release_engine_resource, key, self._logger
        )

    def _build_model(self) -> None:
        try:
            builder = SqlAlchemyModelBuilder(self._engine, self.table)
            self._model = builder.build_model()
            if self.debug:
                self._logger.debug(
                    f"Built ORM model for table: {self.table}", extra=self.logger_extra
                )
        except Exception as e:
            self._logger.error(
                f"Failed to build ORM model: {e}", extra=self.logger_extra
            )
            raise ValueError(f"Model construction failed: {e}") from e

    def get_engine(self) -> Engine:
        """Returns the active SQLAlchemy Engine."""
        if not self._engine:
            raise RuntimeError("Engine not initialized")
        return self._engine

    def get_session(self) -> Session:
        """Returns a new Session instance."""
        if not self._session_factory:
            raise RuntimeError("Session factory not initialized")
        return self._session_factory()

    @property
    def engine(self) -> Engine:
        """
        Public accessor for the SQLAlchemy Engine.
        Required for backward compatibility with SqlAlchemyLoadFromDb.
        """
        if self._engine is None:
            raise RuntimeError("Cannot access 'engine': Engine not initialized.")
        return self._engine


    @property
    def model(self) -> Any:
        """
        Public accessor for the dynamically built SQLAlchemy model.
        Required for backward compatibility with SqlAlchemyLoadFromDb.
        """
        if self._model is None and self.table:
            # Lazy loading fallback if called before validation (edge case protection)
            if self._engine:
                self._build_model()
            else:
                raise RuntimeError("Cannot access 'model': Engine not initialized.")

        return self._model

    def with_updates(self, **kwargs) -> "SqlAlchemyConnectionConfig":
        """
        Creates a new configuration instance with updated fields.

        SAFE REPLACEMENT FOR model_copy():
        This ensures full validation runs on the new parameters and that
        a new engine reference is correctly acquired in the registry.
        """
        # Get current data, excluding private attrs and sensitive secrets
        current_data = self.model_dump(exclude={"connection_url"})

        # Add back the secret explicitly
        current_data["connection_url"] = self.connection_url.get_secret_value()

        # Merge updates
        current_data.update(kwargs)

        # Create a new instance (triggers all validation and init logic)
        return SqlAlchemyConnectionConfig(**current_data)

    def close(self) -> None:
        """
        Explicitly release the engine reference.
        Optional: The weakref finalizer will handle this automatically if skipped.
        """
        if self._finalizer:
            self._finalizer()


#
# from __future__ import annotations
# import os
# import threading
# from contextlib import contextmanager
# from typing import Any, Optional, ClassVar, Generator, Type, Dict
#
# from pydantic import BaseModel, field_validator, model_validator, ConfigDict
# from sqlalchemy import create_engine, event, text
# from sqlalchemy.engine import url as sqlalchemy_url
# from sqlalchemy.engine import Engine
# from sqlalchemy.exc import OperationalError, SQLAlchemyError
# from sqlalchemy.orm import sessionmaker, Session
# from sqlalchemy.pool import QueuePool, NullPool, StaticPool, Pool
#
# from sibi_dst.utils import Logger
# from ._sql_model_builder import SqlAlchemyModelBuilder
#
# _ENGINE_REGISTRY_LOCK = threading.RLock()
# _ENGINE_REGISTRY: Dict[tuple, Dict[str, Any]] = {}
#
#
# class SqlAlchemyConnectionConfig(BaseModel):
#     """
#     Thread-safe, registry-backed SQLAlchemy connection manager.
#     """
#
#     # --- Public Configuration ---
#     connection_url: str
#     table: Optional[str] = None
#     debug: bool = False
#     logger_extra: Optional[Dict[str, Any]] = {"sibi_dst_component": __name__}
#
#     # --- Pool Configuration ---
#     pool_size: int = int(os.environ.get("DB_POOL_SIZE", 5))
#     max_overflow: int = int(os.environ.get("DB_MAX_OVERFLOW", 10))
#     pool_timeout: int = int(os.environ.get("DB_POOL_TIMEOUT", 30))
#     pool_recycle: int = int(os.environ.get("DB_POOL_RECYCLE", 1800))
#     pool_pre_ping: bool = True
#     poolclass: Type[Pool] = QueuePool
#
#     # --- Internal & Runtime State (normal fields; Pydantic allowed) ---
#     model: Optional[Type[Any]] = None
#     engine: Optional[Engine] = None
#     logger: Optional[Logger] = None
#     _own_logger: bool = False
#     session_factory: Optional[sessionmaker] = None
#
#     # --- Private State (plain Python values only) ---
#     _engine_key_instance: tuple = ()
#     _closed: bool = False  # prevent double-closing
#     model_config = ConfigDict(arbitrary_types_allowed=True)
#
#     def __enter__(self) -> "SqlAlchemyConnectionConfig":
#         return self
#
#     def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
#         self.close()
#
#     @field_validator("pool_size", "max_overflow", "pool_timeout", "pool_recycle")
#     @classmethod
#     def _validate_pool_params(cls, v: int) -> int:
#         if v < 0:
#             raise ValueError("Pool parameters must be non-negative")
#         return v
#
#     @model_validator(mode="after")
#     def _init_all(self) -> "SqlAlchemyConnectionConfig":
#         self._init_logger()
#         self._engine_key_instance = self._get_engine_key()
#         self._init_engine()
#         self._validate_conn()
#         self._build_model()
#         if self.engine:
#             self.session_factory = sessionmaker(bind=self.engine, expire_on_commit=False)
#         return self
#
#     def _init_logger(self) -> None:
#         if self.logger is None:
#             self._own_logger = True
#             self.logger = Logger.default_logger(logger_name=self.__class__.__name__)
#             self.logger.set_level(Logger.DEBUG if self.debug else Logger.INFO)
#
#     def _get_engine_key(self) -> tuple:
#         parsed = sqlalchemy_url.make_url(self.connection_url)
#         query = {k: v for k, v in parsed.query.items() if not k.startswith("pool_")}
#         normalized_url = parsed.set(query=query)
#         key_parts = [str(normalized_url)]
#         if self.poolclass not in (NullPool, StaticPool):
#             key_parts += [
#                 self.pool_size, self.max_overflow, self.pool_timeout,
#                 self.pool_recycle, self.pool_pre_ping
#             ]
#         return tuple(key_parts)
#
#     def _init_engine(self) -> None:
#         with _ENGINE_REGISTRY_LOCK:
#             wrapper = _ENGINE_REGISTRY.get(self._engine_key_instance)
#             if wrapper:
#                 self.engine = wrapper["engine"]
#                 wrapper["ref_count"] += 1
#                 if self.debug:
#                     self.logger.debug(f"Reusing DB engine. Ref count: {wrapper['ref_count']}.", extra=self.logger_extra)
#             else:
#                 if self.debug:
#                     self.logger.debug(f"Creating new DB engine for key: {self._engine_key_instance}", extra=self.logger_extra)
#                 try:
#                     new_engine = create_engine(
#                         self.connection_url,
#                         pool_size=self.pool_size,
#                         max_overflow=self.max_overflow,
#                         pool_timeout=self.pool_timeout,
#                         pool_recycle=self.pool_recycle,
#                         pool_pre_ping=self.pool_pre_ping,
#                         poolclass=self.poolclass,
#                     )
#                     self.engine = new_engine
#                     self._attach_events()
#                     _ENGINE_REGISTRY[self._engine_key_instance] = {
#                         "engine": new_engine,
#                         "ref_count": 1,
#                         "active_connections": 0,
#                     }
#                 except Exception as e:
#                     self.logger.error(f"Failed to create DB engine: {e}", extra=self.logger_extra)
#                     raise SQLAlchemyError(f"DB Engine creation failed: {e}") from e
#
#     def close(self) -> None:
#         if self._closed:
#             if self.debug:
#                 self.logger.debug("Attempted to close an already-closed DB config instance.")
#             return
#
#         with _ENGINE_REGISTRY_LOCK:
#             key = self._engine_key_instance
#             wrapper = _ENGINE_REGISTRY.get(key)
#             if not wrapper:
#                 self.logger.warning("Attempted to close a DB config whose engine is not in the registry.", extra=self.logger_extra)
#             else:
#                 wrapper["ref_count"] -= 1
#                 if self.debug:
#                     self.logger.debug(f"Closing DB connection. Ref count now {wrapper['ref_count']}.", extra=self.logger_extra)
#                 if wrapper["ref_count"] <= 0:
#                     if self.debug:
#                         self.logger.debug(f"Disposing DB engine as reference count is zero. Key: {key}", extra=self.logger_extra)
#                     try:
#                         wrapper["engine"].dispose()
#                     finally:
#                         del _ENGINE_REGISTRY[key]
#         self._closed = True
#
#     def _attach_events(self) -> None:
#         if not self.engine:
#             return
#         event.listen(self.engine, "checkout", self._on_checkout)
#         event.listen(self.engine, "checkin", self._on_checkin)
#
#     def _on_checkout(self, *args) -> None:
#         with _ENGINE_REGISTRY_LOCK:
#             wrapper = _ENGINE_REGISTRY.get(self._engine_key_instance)
#             if wrapper:
#                 wrapper["active_connections"] += 1
#
#     def _on_checkin(self, *args) -> None:
#         with _ENGINE_REGISTRY_LOCK:
#             wrapper = _ENGINE_REGISTRY.get(self._engine_key_instance)
#             if wrapper:
#                 wrapper["active_connections"] = max(0, wrapper["active_connections"] - 1)
#
#     @property
#     def active_connections(self) -> int:
#         with _ENGINE_REGISTRY_LOCK:
#             wrapper = _ENGINE_REGISTRY.get(self._engine_key_instance)
#             return wrapper["active_connections"] if wrapper else 0
#
#     def _validate_conn(self) -> None:
#         try:
#             with self.managed_connection() as conn:
#                 conn.execute(text("SELECT 1"))
#             if self.debug:
#                 self.logger.debug("Database connection validated successfully.", extra=self.logger_extra)
#         except OperationalError as e:
#             self.logger.error(f"Database connection failed: {e}", extra=self.logger_extra)
#             raise ValueError(f"DB connection failed: {e}") from e
#
#     @contextmanager
#     def managed_connection(self) -> Generator[Any, None, None]:
#         if not self.engine:
#             raise RuntimeError("DB Engine not initialized. Cannot get a connection.")
#         conn = self.engine.connect()
#         try:
#             yield conn
#         finally:
#             conn.close()
#
#     def get_session(self) -> Session:
#         if not self.session_factory:
#             raise RuntimeError("Session factory not initialized. Cannot get a session.")
#         return self.session_factory()
#
#     def _build_model(self) -> None:
#         if not self.table or not self.engine:
#             return
#         try:
#             builder = SqlAlchemyModelBuilder(self.engine, self.table)
#             self.model = builder.build_model()
#             if self.debug:
#                 self.logger.debug(f"Successfully built ORM model for table: {self.table}", extra=self.logger_extra)
#         except Exception as e:
#             self.logger.error(f"Failed to build ORM model for table '{self.table}': {e}", extra=self.logger_extra)
#             raise ValueError(f"Model construction failed for table '{self.table}': {e}") from e
#
