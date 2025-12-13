from __future__ import annotations

import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import ClassVar, Dict, Optional, Any, Iterable

import pandas as pd
import dask.dataframe as dd
import clickhouse_connect
import numpy as np

from sibi_dst.utils import ManagedResource


def _to_bool(val: Any) -> bool:
    if isinstance(val, bool):
        return val
    if isinstance(val, (int, float)):
        return bool(val)
    if isinstance(val, str):
        return val.strip().lower() in ("1", "true", "yes", "on")
    return False


class ClickHouseWriter(ManagedResource):
    """
    Write a Dask DataFrame to ClickHouse safely with:
      - Dtype normalization for PyArrow, NumPy, and Pandas
      - Partitioned parallel inserts
      - Nullable schema inference
      - Optional table overwrite
      - Per-thread ClickHouse clients
    """

    DTYPE_MAP: ClassVar[Dict[str, str]] = {
        # ---- Integer types ----
        "int8": "Int8",
        "int16": "Int16",
        "int32": "Int32",
        "int64": "Int64",
        "uint8": "UInt8",
        "uint16": "UInt16",
        "uint32": "UInt32",
        "uint64": "UInt64",
        # ---- Floating point ----
        "float": "Float64",
        "float16": "Float32",  # ClickHouse lacks Float16
        "float32": "Float32",
        "float64": "Float64",
        # ---- Boolean ----
        "bool": "UInt8",
        "boolean": "UInt8",  # Pandas nullable boolean
        # ---- String / object ----
        "object": "String",  # generic fallback
        "string": "String",
        "category": "String",
        # ---- Datetime ----
        "datetime64[ns]": "DateTime64(3)",  # sub-second precision
        "datetime64[ns, UTC]": "DateTime64(3, 'UTC')",
        "datetime64[ns, utc]": "DateTime64(3, 'UTC')",
        "datetime64[ms]": "DateTime64(3)",
        "datetime64[s]": "DateTime",
        # ---- Timedelta ----
        "timedelta64[ns]": "Int64",  # store as microseconds integer
        # ---- Complex / unsupported ----
        "complex64": "String",
        "complex128": "String",
        # ---- Miscellaneous ----
        "bytes": "String",
        "decimal": "Decimal(18,6)",  # custom, adjust precision as needed
        "json": "String",  # often stored as raw JSON text
        "dict": "String",
        "list": "Array(String)",
        "array": "Array(Float64)",  # adjust per context
    }

    def __init__(
        self,
        *,
        host: str = "localhost",
        port: int = 8123,
        database: str = "sibi_data",
        user: str = "default",
        password: str = "",
        secure: bool = False,
        verify: bool = False,
        ca_cert: str = "",
        client_cert: str = "",
        compression: str = "",
        table: str = "test_sibi_table",
        order_by: str = "id",
        engine: Optional[str] = None,
        max_workers: int = 4,
        insert_chunksize: int = 50_000,
        overwrite: bool = False,
        **kwargs: Any,
    ):
        super().__init__(**kwargs)
        self.host = host
        self.port = int(port)
        self.database = database
        self.user = user
        self.password = password
        self.secure = _to_bool(secure)
        self.verify = _to_bool(verify)
        self.ca_cert = ca_cert
        self.client_cert = client_cert
        self.compression = compression
        self.table = table
        self.order_by = order_by
        self.engine = engine
        self.max_workers = int(max_workers)
        self.insert_chunksize = int(insert_chunksize)
        self.overwrite = _to_bool(overwrite)

        self._tlocal = threading.local()
        if self.overwrite:
            self._command(f"DROP TABLE IF EXISTS {self._ident(self.table)}")
            self.logger.debug(f"Dropped table {self.table} (overwrite=True)")

    # ---------------------- Public API ----------------------

    def save_to_clickhouse(self, df: dd.DataFrame) -> None:
        if not isinstance(df, dd.DataFrame):
            raise TypeError(
                "ClickHouseWriter.save_to_clickhouse expects a dask.dataframe.DataFrame."
            )

        head = df.head(1, npartitions=-1, compute=True)
        if head.empty:
            self.logger.debug("Dask DataFrame is empty; nothing to write.")
            return
        df = df.map_partitions(
            self._process_partition_for_clickhouse_compatible, meta=df._meta
        )
        # Schema generation
        dtypes = df._meta_nonempty.dtypes
        schema_sql = self._generate_clickhouse_schema(dtypes)
        engine_sql = self._default_engine_sql() if not self.engine else self.engine

        schema_command = f"CREATE TABLE IF NOT EXISTS {self._ident(self.table)} ({schema_sql}) {engine_sql}"
        self._command(schema_command)
        self.logger.debug(f"Ensured table {self.table} exists")

        # Write partitions concurrently
        parts = list(df.to_delayed())
        if not parts:
            self.logger.debug("No partitions to write.")
            return

        self.logger.debug(
            f"Writing {len(parts)} partitions to ClickHouse (max_workers={self.max_workers})"
        )
        with ThreadPoolExecutor(max_workers=self.max_workers) as ex:
            futures = {
                ex.submit(self._write_one_partition, part, i): i
                for i, part in enumerate(parts)
            }
            for fut in as_completed(futures):
                i = futures[fut]
                try:
                    fut.result()
                except Exception as e:
                    self.logger.error(f"Partition {i} failed: {e}", exc_info=self.debug)
                    raise
        self.logger.info(f"Completed writing {len(parts)} partitions to {self.table}")

    # ---------------------- Schema and Types ----------------------

    def _generate_clickhouse_schema(self, dask_dtypes: pd.Series) -> str:
        parts = []
        for col, dtype in dask_dtypes.items():
            ch_type = self._map_dtype(dtype)
            if self._should_mark_nullable(dtype):
                ch_type = f"Nullable({ch_type})"
            parts.append(f"{self._ident(col)} {ch_type}")
        return ", ".join(parts)

    def _map_dtype(self, dtype: Any) -> str:
        if isinstance(dtype, pd.StringDtype):
            return "String"
        if isinstance(dtype, pd.BooleanDtype):
            return "UInt8"
        if isinstance(dtype, pd.Int64Dtype):
            return "Int64"
        if isinstance(dtype, pd.Int32Dtype):
            return "Int32"
        if isinstance(dtype, pd.Float64Dtype):
            return "Float64"

        dtype_str = str(dtype).lower()
        if "datetime64" in dtype_str:
            return "DateTime"
        if "[pyarrow]" in dtype_str:
            if "int32" in dtype_str:
                return "Int32"
            if "int64" in dtype_str:
                return "Int64"
            if "float32" in dtype_str:
                return "Float32"
            if "float64" in dtype_str or "double" in dtype_str:
                return "Float64"
            if "bool" in dtype_str:
                return "UInt8"
            if "timestamp" in dtype_str:
                return "DateTime"
            if "timestamp[ns]" in dtype_str:
                return "DateTime"

            if "string" in dtype_str:
                return "String"
            return "String"
        return self.DTYPE_MAP.get(str(dtype), "String")

    @staticmethod
    def _should_mark_nullable(dtype: Any) -> bool:
        dtype_str = str(dtype).lower()
        if "[pyarrow]" in dtype_str:
            return any(x in dtype_str for x in ["string", "timestamp"])
        if isinstance(
            dtype,
            (
                pd.StringDtype,
                pd.BooleanDtype,
                pd.Int64Dtype,
                pd.Int32Dtype,
                pd.Float64Dtype,
            ),
        ):
            return True
        if "datetime64" in dtype_str or dtype_str in ("object", "category", "string"):
            return True
        return False

    def _default_engine_sql(self) -> str:
        order_by = (
            self.order_by if self.order_by.startswith("(") else f"(`{self.order_by}`)"
        )
        return f"ENGINE = MergeTree ORDER BY {order_by} SETTINGS allow_nullable_key = 1"

    # ---------------------- Partition Write ----------------------

    def _write_one_partition(self, part, index: int) -> None:
        pdf: pd.DataFrame = part.compute()
        if pdf.empty:
            self.logger.debug(f"Partition {index} empty; skipping")
            return

        # iterate by row count, not by column values
        nrows = len(pdf)
        for start in range(0, nrows, self.insert_chunksize):
            batch = pdf.iloc[start : start + self.insert_chunksize]
            if batch.empty:
                continue
            self._insert_df(list(batch.columns), batch)

        self.logger.debug(f"Partition {index} inserted ({nrows} rows)")

    def _insert_df(self, cols: Iterable[str], df: pd.DataFrame) -> None:
        client = self._get_client()
        client.insert_df(
            self.table,
            df[cols],
            settings={"async_insert": 1, "wait_end_of_query": 1},
        )

    # ---------------------- Type Normalization ----------------------

    @staticmethod
    def _to_builtin_scalar(x: Any) -> Any:
        if x is None or (isinstance(x, float) and pd.isna(x)):
            return None
        if isinstance(x, (np.integer,)):
            return int(x)
        if isinstance(x, (np.floating,)):
            return float(x)
        if isinstance(x, (np.bool_,)):
            return bool(x)
        if isinstance(x, (np.ndarray,)):
            return x.tolist()
        return x

    @staticmethod
    def _normalize_arrow_dtype(s: pd.Series) -> pd.Series:
        dtype_str = str(s.dtype).lower()
        # Skip non-pyarrow dtypes early
        if "[pyarrow]" not in dtype_str:
            return s
        if "string" in dtype_str:
            return s.astype("string")
        if "int32" in dtype_str:
            return s.astype("Int32")
        if "double" in dtype_str:
            return s.astype("Float64")
        if "int64" in dtype_str:
            return s.astype("Int64")
        if "float32" in dtype_str:
            return s.astype("Float32")
        if "float64" in dtype_str or "double" in dtype_str:
            return s.astype("Float64")
        if "bool" in dtype_str:
            return s.astype("boolean")
        if "timestamp" in dtype_str:
            # Fully normalize timestamp
            s = pd.Series(pd.to_datetime(s, errors="coerce", utc=True))
            # Strip tz only if present
            try:
                s = s.dt.tz_localize(None)
            except (TypeError, AttributeError):
                pass
            # Force pandas-native dtype
            s = s.astype("datetime64[ns]")
            s = s.convert_dtypes(dtype_backend="numpy_nullable")
            return s

        return s.astype("string")

    @staticmethod
    def _process_partition_for_clickhouse_compatible(pdf: pd.DataFrame) -> pd.DataFrame:
        pdf = pdf.copy()
        for col in pdf.columns:
            s = ClickHouseWriter._normalize_arrow_dtype(pdf[col])
            s = s.replace({pd.NA: np.nan})
            if pd.api.types.is_integer_dtype(s):
                s = s.astype("Int64")
            elif pd.api.types.is_bool_dtype(s):
                s = s.astype("boolean")
            elif pd.api.types.is_float_dtype(s):
                s = pd.to_numeric(s, errors="coerce").astype("Float64")
            elif pd.api.types.is_datetime64_any_dtype(s) or "timestamp" in str(s.dtype):
                s = (
                    pd.to_datetime(s, errors="coerce", utc=True)
                    .dt.tz_localize(None)
                    .astype("datetime64[ns]")
                )
            elif isinstance(s, pd.CategoricalDtype) or pd.api.types.is_string_dtype(
                s
            ):
                s = s.astype("string")
            else:
                s = s.map(ClickHouseWriter._to_builtin_scalar).astype("string")

            pdf[col] = s
        pdf = pdf.convert_dtypes(dtype_backend="numpy_nullable")
        return pdf

    # ---------------------- Low-Level ----------------------

    def _get_client(self):
        cli = getattr(self._tlocal, "client", None)
        if cli:
            return cli
        cli = clickhouse_connect.get_client(
            host=self.host,
            port=self.port,
            database=self.database,
            username=self.user,
            password=self.password,
            secure=self.secure,
            verify=self.verify,
            ca_cert=self.ca_cert or None,
            client_cert=self.client_cert or None,
            compression=self.compression or None,
        )
        self._tlocal.client = cli
        return cli

    def _command(self, sql: str) -> None:
        self._get_client().command(sql)

    @staticmethod
    def _ident(name: str) -> str:
        return (
            f"`{name}`" if not (name.startswith("`") and name.endswith("`")) else name
        )

    def _cleanup(self):
        cli = getattr(self._tlocal, "client", None)
        try:
            if cli:
                cli.close()
        except Exception:
            pass
        finally:
            if hasattr(self._tlocal, "client"):
                delattr(self._tlocal, "client")
