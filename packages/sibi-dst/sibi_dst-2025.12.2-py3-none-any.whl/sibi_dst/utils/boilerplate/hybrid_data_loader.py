import datetime
from typing import Optional, Tuple, Iterable, Dict
import pandas as pd
import dask.dataframe as dd
from sibi_dst.utils import Logger
from sibi_dst.utils.dask_utils import dask_is_empty

TODAY = datetime.date.today()
YESTERDAY = TODAY - datetime.timedelta(days=1)
TODAY_STR = TODAY.strftime("%Y-%m-%d")
YESTERDAY_STR = YESTERDAY.strftime("%Y-%m-%d")


class HybridDataLoader:
    """
    Hybrid loader that merges historical (Parquet) and live (API/DB) data
    in a consistent, schema-safe, timezone-normalized way.
    """

    def __init__(
        self,
        start_date: str,
        end_date: str,
        historical_reader,
        live_reader,
        date_field: str,
        **kwargs,
    ):
        self.start_date = self._validate_date_format(start_date)
        self.end_date = self._validate_date_format(end_date)
        self.historical_reader = historical_reader
        self.live_reader = live_reader
        self.date_field = date_field

        self.logger = kwargs.get("logger", Logger.default_logger(logger_name=__name__))
        self.debug = kwargs.get("debug", False)
        self.logger.set_level(Logger.DEBUG if self.debug else Logger.INFO)

        self._validate_date_range()

        self._read_live_flag = self.end_date == TODAY_STR
        self._is_single_today = self.start_date == self.end_date == TODAY_STR
        self._is_single_historical = (
            self.start_date == self.end_date != TODAY_STR
        )

    # ------------------------------------------------------------------ #
    # Validation
    # ------------------------------------------------------------------ #
    @staticmethod
    def _validate_date_format(date_str: str) -> str:
        try:
            datetime.datetime.strptime(date_str, "%Y-%m-%d")
            return date_str
        except ValueError:
            raise ValueError(f"Date '{date_str}' is not in valid YYYY-MM-DD format")

    def _validate_date_range(self):
        start = datetime.datetime.strptime(self.start_date, "%Y-%m-%d").date()
        end = datetime.datetime.strptime(self.end_date, "%Y-%m-%d").date()
        if end < start:
            raise ValueError(
                f"End date ({self.end_date}) cannot be before start date ({self.start_date})"
            )

    # ------------------------------------------------------------------ #
    # Schema and dtype helpers
    # ------------------------------------------------------------------ #
    @staticmethod
    def _empty_like(df: dd.DataFrame) -> pd.DataFrame:
        """Return a concrete pandas meta sample."""
        try:
            return df._meta_nonempty.head(0)
        except Exception:
            return df.head(0, compute=True).iloc[0:0]

    @staticmethod
    def _safe_add_missing_columns(
        df: dd.DataFrame, missing: Iterable[str], meta_ref: pd.DataFrame
    ) -> dd.DataFrame:
        """Add missing columns with explicit dtypes from meta_ref."""
        if missing is None or len(missing) == 0:
            return df

        dtype_map: Dict[str, str] = {
            c: str(meta_ref.dtypes.get(c, "object")) for c in missing
        }

        def _add_cols(pdf: pd.DataFrame) -> pd.DataFrame:
            for c in missing:
                pdf[c] = pd.Series(pd.NA, index=pdf.index, dtype=dtype_map[c]) \
                    if dtype_map[c].startswith(
                        ("Int", "Float", "boolean", "string")
                    ) else pd.Series(None, index=pdf.index, dtype=dtype_map[c])
            return pdf

        new_meta = pd.concat(
            [HybridDataLoader._empty_like(df), meta_ref[list(missing)].iloc[0:0]],
            axis=1,
        )
        return df.map_partitions(
            _add_cols, meta=new_meta.reindex(columns=list(new_meta.columns))
        )

    @staticmethod
    def _unify_columns_and_dtypes(
        left: dd.DataFrame, right: dd.DataFrame
    ) -> Tuple[dd.DataFrame, dd.DataFrame]:
        """Make both DFs share identical columns and dtypes."""
        left_meta = HybridDataLoader._empty_like(left)
        right_meta = HybridDataLoader._empty_like(right)
        all_cols = pd.Index(sorted(set(left_meta.columns) | set(right_meta.columns)))

        # Build unified dtype reference
        union_dtypes = {}
        for c in all_cols:
            if c in right_meta.columns:
                union_dtypes[c] = right_meta.dtypes[c]
            elif c in left_meta.columns:
                union_dtypes[c] = left_meta.dtypes[c]
            else:
                union_dtypes[c] = "object"
        union_meta = pd.DataFrame(
            {c: pd.Series(dtype=union_dtypes[c]) for c in all_cols}
        )

        # Add missing columns with dtypes
        left = HybridDataLoader._safe_add_missing_columns(
            left, all_cols.difference(left_meta.columns), union_meta
        )
        right = HybridDataLoader._safe_add_missing_columns(
            right, all_cols.difference(right_meta.columns), union_meta
        )

        # Reorder and cast
        left = left[all_cols]
        right = right[all_cols]
        dtype_map = {c: union_meta.dtypes[c] for c in all_cols}

        def _astype(pdf: pd.DataFrame) -> pd.DataFrame:
            return pdf.astype(dtype_map, errors="ignore")

        left = left.map_partitions(_astype)
        right = right.map_partitions(_astype)
        return left, right

    @staticmethod
    def _normalize_datetimes(df: dd.DataFrame, cols: list[str]) -> dd.DataFrame:
        """Normalize datetime columns to UTC safely."""
        if not cols:
            return df

        def _to_ts(pdf: pd.DataFrame) -> pd.DataFrame:
            for c in cols:
                if c in pdf.columns:
                    pdf[c] = pd.to_datetime(pdf[c], errors="coerce", utc=True)
            return pdf

        return df.map_partitions(_to_ts)

    @staticmethod
    def _create_empty_dataframe(meta: Optional[pd.DataFrame] = None) -> dd.DataFrame:
        if meta is not None and not meta.empty:
            return dd.from_pandas(meta.iloc[0:0], npartitions=1)
        return dd.from_pandas(pd.DataFrame(), npartitions=1)

    # ------------------------------------------------------------------ #
    # Data loading methods
    # ------------------------------------------------------------------ #
    async def _load_today_data(self, **kwargs) -> Optional[dd.DataFrame]:
        """Load today's live data."""
        self.logger.debug("Loading today's live data...")
        date_filter = {f"{self.date_field}__date": TODAY_STR}
        filters = {**kwargs, **date_filter}

        try:
            reader_obj = self.live_reader(logger=self.logger, debug=self.debug)
            if not hasattr(reader_obj, "aload"):
                raise TypeError("live_reader must expose an async aload() method")
            today_df = await reader_obj.aload(**filters)
            if today_df is not None:
                today_df = self._normalize_datetimes(today_df, [self.date_field])
            return today_df
        except Exception as e:
            self.logger.error(f"Failed to load today's data: {e}")
            return None if not self.debug else (_ for _ in ()).throw(e)

    async def _load_historical_data(
        self, start_date: str, end_date: str, **kwargs
    ) -> dd.DataFrame:
        """Load historical data."""
        self.logger.debug(f"Loading historical data from {start_date} to {end_date}...")
        try:
            reader_obj = self.historical_reader(
                parquet_start_date=start_date,
                parquet_end_date=end_date,
                logger=self.logger,
                debug=self.debug,
            )
            if not hasattr(reader_obj, "aload"):
                raise TypeError("historical_reader must expose an async aload() method")
            df = await reader_obj.aload(**kwargs)
            df = self._normalize_datetimes(df, [self.date_field])
            return df
        except Exception as e:
            self.logger.error(f"Failed to load historical data: {e}")
            if self.debug:
                raise
            return self._create_empty_dataframe()

    # ------------------------------------------------------------------ #
    # Orchestrator
    # ------------------------------------------------------------------ #
    async def aload(self, **kwargs) -> dd.DataFrame:
        """Load and concatenate data from historical and live sources."""
        self.logger.debug(
            f"[HybridLoader] start={self.start_date}, end={self.end_date}, "
            f"read_live={self._read_live_flag}"
        )

        # Case 1: only today
        if self._is_single_today:
            today_df = await self._load_today_data(**kwargs)
            return today_df if today_df is not None else self._create_empty_dataframe()

        # Case 2: purely historical
        if not self._read_live_flag:
            return await self._load_historical_data(
                self.start_date, self.end_date, **kwargs
            )

        # Case 3: mixed historical + live
        hist_df = await self._load_historical_data(
            self.start_date, YESTERDAY_STR, **kwargs
        )
        live_df = await self._load_today_data(**kwargs)

        if live_df is not None and not dask_is_empty(live_df):
            if not dask_is_empty(hist_df):
                try:
                    hist_df, live_df = self._unify_columns_and_dtypes(hist_df, live_df)
                    return dd.concat(
                        [hist_df, live_df],
                        ignore_unknown_divisions=True,
                        interleave_partitions=True,
                    )
                except Exception as e:
                    self.logger.warning(f"Schema alignment failed: {e}")
            # Only live data
            _, live_df = self._unify_columns_and_dtypes(
                self._create_empty_dataframe(), live_df
            )
            return dd.concat(
                [live_df],
                ignore_unknown_divisions=True,
                interleave_partitions=True,
            )

        return hist_df

    # ------------------------------------------------------------------ #
    def __repr__(self):
        return (
            f"HybridDataLoader(start='{self.start_date}', end='{self.end_date}', "
            f"read_live={self._read_live_flag})"
        )

# import dask.dataframe as dd
# import datetime
# import pandas as pd
# from typing import Optional
# from sibi_dst.utils import Logger
# from sibi_dst.utils.dask_utils import dask_is_empty
#
# today = datetime.date.today()
# yesterday = today - datetime.timedelta(days=1)
# TODAY_STR = today.strftime('%Y-%m-%d')
# YESTERDAY_STR = yesterday.strftime('%Y-%m-%d')
#
#
# class HybridDataLoader:
#     """
#     A generic data loader that orchestrates loading from a historical
#     source and an optional live source.
#     """
#
#     def __init__(self, start_date: str, end_date: str, historical_reader, live_reader, date_field: str, **kwargs):
#         self.start_date = self._validate_date_format(start_date)
#         self.end_date = self._validate_date_format(end_date)
#         self.historical_reader = historical_reader
#         self.live_reader = live_reader
#         self.date_field = date_field
#
#         self.logger = kwargs.get('logger', Logger.default_logger(logger_name=__name__))
#         self.debug = kwargs.get('debug', False)
#         self.logger.set_level(Logger.DEBUG if self.debug else Logger.INFO)
#
#         # Validate date range
#         self._validate_date_range()
#
#         # Determine loading strategy
#         self._should_read_live = self.end_date == TODAY_STR
#         self._is_single_today = (self.start_date == TODAY_STR and self.end_date == TODAY_STR)
#         self._is_single_historical = (self.start_date == self.end_date and self.end_date != TODAY_STR)
#
#     def _validate_date_format(self, date_str: str) -> str:
#         """Validate that date string is in correct format."""
#         try:
#             datetime.datetime.strptime(date_str, '%Y-%m-%d')
#             return date_str
#         except ValueError:
#             raise ValueError(f"Date '{date_str}' is not in valid YYYY-MM-DD format")
#
#     def _validate_date_range(self):
#         """Validate that start date is not after end date."""
#         start = datetime.datetime.strptime(self.start_date, '%Y-%m-%d').date()
#         end = datetime.datetime.strptime(self.end_date, '%Y-%m-%d').date()
#         if end < start:
#             raise ValueError(f"End date ({self.end_date}) cannot be before start date ({self.start_date})")
#
#     def _align_schema_to_live(self, historical_df: dd.DataFrame, live_df: dd.DataFrame) -> dd.DataFrame:
#         """Forces the historical dataframe schema to match the live one."""
#         self.logger.debug("Aligning historical schema to match live schema.")
#         historical_cols = set(historical_df.columns)
#         live_cols = set(live_df.columns)
#
#         # Add missing columns to historical dataframe
#         for col in live_cols - historical_cols:
#             historical_df[col] = None
#
#         # Reorder columns to match live dataframe
#         return historical_df[list(live_df.columns)]
#
#     def _create_empty_dataframe(self) -> dd.DataFrame:
#         """Create an empty dask dataframe with proper structure."""
#         return dd.from_pandas(pd.DataFrame(), npartitions=1)
#
#     async def _load_today_data(self, **kwargs) -> Optional[dd.DataFrame]:
#         """Load today's data from the live reader."""
#         self.logger.debug(f"Loading today's live data...")
#         date_filter = {f"{self.date_field}__date": TODAY_STR}
#         filters = {**kwargs, **date_filter}
#
#         try:
#             today_df = await self.live_reader(
#                 logger=self.logger,
#                 debug=self.debug
#             ).aload(**filters)
#             return today_df
#         except Exception as e:
#             self.logger.error(f"Failed to load today's data: {e}")
#             if not self.debug:
#                 return None
#             raise
#
#     async def _load_historical_data(self, start_date: str, end_date: str, **kwargs) -> dd.DataFrame:
#         """Load historical data from the historical reader."""
#         self.logger.debug(f"Loading historical data from {start_date} to {end_date}...")
#
#         try:
#             return await self.historical_reader(
#                 parquet_start_date=start_date,
#                 parquet_end_date=end_date,
#                 logger=self.logger,
#                 debug=self.debug
#             ).aload(**kwargs)
#         except Exception as e:
#             self.logger.error(f"Failed to load historical data from {start_date} to {end_date}: {e}")
#             if not self.debug:
#                 return self._create_empty_dataframe()
#             raise
#
#     async def aload(self, **kwargs) -> dd.DataFrame:
#         """
#         Loads data from the historical source and, if required, the live source,
#         then concatenates them.
#         """
#         # Case 1: Only today's data requested
#         if self._is_single_today:
#             today_df = await self._load_today_data(**kwargs)
#             return today_df if today_df is not None else self._create_empty_dataframe()
#
#         # Case 2: Pure historical data (end date is not today)
#         if not self._should_read_live:
#             return await self._load_historical_data(self.start_date, self.end_date, **kwargs)
#
#         # Case 3: Mixed historical + live scenario (end date is today)
#         # Load historical data up to yesterday
#         historical_df = await self._load_historical_data(self.start_date, YESTERDAY_STR, **kwargs)
#
#         # Load today's data
#         today_df = await self._load_today_data(**kwargs)
#
#         # Combine dataframes
#         if today_df is not None and not dask_is_empty(today_df):
#             # Align schemas if needed
#             if len(historical_df.columns) > 0 and len(today_df.columns) > 0:
#                 try:
#                     historical_df = self._align_schema_to_live(historical_df, today_df)
#                 except Exception as e:
#                     self.logger.warning(f"Failed to align schemas: {e}")
#
#             return dd.concat([historical_df, today_df], ignore_index=True)
#         else:
#             return historical_df
#
#     def __repr__(self):
#         return (f"HybridDataLoader(start_date='{self.start_date}', "
#                 f"end_date='{self.end_date}', "
#                 f"loading_live={self._should_read_live})")
#
