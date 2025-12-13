from __future__ import annotations

import asyncio
from concurrent.futures import ThreadPoolExecutor
from typing import Type, Any, List

import pandas as pd
import dask.dataframe as dd

from sibi_dst.utils import ManagedResource, ParquetSaver
from sibi_dst.df_helper import ParquetReader
from sibi_dst.utils.dask_utils import dask_is_empty, _safe_persist, _safe_compute, DaskClientMixin


class DateRangeHelper:
    @staticmethod
    def generate_daily_ranges(start_date: str, end_date: str, date_format: str = "%Y-%m-%d") -> List[str]:
        start = pd.to_datetime(start_date)
        end = pd.to_datetime(end_date)
        return [d.strftime(date_format) for d in pd.date_range(start, end, freq="D")]

    @staticmethod
    def generate_monthly_ranges(start_date: str, end_date: str, date_format: str = "%Y-%m-%d") -> List[tuple[str, str]]:
        start = pd.to_datetime(start_date)
        end = pd.to_datetime(end_date)
        ranges = []
        current = start.replace(day=1)
        while current <= end:
            month_end = (current + pd.offsets.MonthEnd(0)).normalize()
            ranges.append((
                current.strftime(date_format),
                min(month_end, end).strftime(date_format)
            ))
            current += pd.DateOffset(months=1)
        return ranges


class BasePipeline(ManagedResource):
    def __init__(
        self,
        start_date: str,
        end_date: str,
        dataset_cls: Type,
        parquet_storage_path: str,
        *,
        fs: Any,
        filename: str = "dataset",
        date_field: str = "date",
        max_workers: int = 4,
        dataset_kwargs: dict = None,
        **kwargs,
    ):
        kwargs["fs"] = fs
        super().__init__(**kwargs)
        self.start_date = start_date
        self.end_date = end_date
        self.filename = filename
        self.date_field = date_field
        self.max_workers = max_workers
        self.storage_path = parquet_storage_path.rstrip("/")
        self.df: dd.DataFrame | None = None
        self.dask_client = kwargs.get("dask_client", None)
        self.ds = dataset_cls(start_date=self.start_date, end_date=self.end_date, **kwargs)

    # ------------------------------------------------------------------
    # Pipeline entrypoints
    # ------------------------------------------------------------------
    async def aload(self, **kwargs) -> dd.DataFrame:
        await self.emit("status", message="Loading dataset...", progress=5)
        self.df = await self.ds.aload(**kwargs)
        nparts = getattr(self.df, "npartitions", 0)
        self.logger.debug(f"Dataset loaded: {nparts} partitions, {self.df.columns.size} columns")
        return self.df

    # ------------------------------------------------------------------
    # Write to Parquet
    # ------------------------------------------------------------------
    async def to_parquet(self, **kwargs) -> None:
        df = await self.ds.aload(**kwargs)

        if dask_is_empty(df, dask_client=self.dask_client):
            self.logger.warning("No data to save.")
            return

        # Persist once for efficient I/O
        df = _safe_persist(df, dask_client=self.dask_client)

        # Efficient row count
        n_rows = await asyncio.to_thread(lambda: _safe_compute(df.map_partitions(len).sum(), self.dask_client))
        self.logger.debug(f"Preparing to save {int(n_rows)} rows to Parquet.")

        # Add partition column
        df = df.assign(
            partition_date=dd.to_datetime(df[self.date_field], errors="coerce").dt.date.astype(str)
        )

        out_path = self.storage_path.rstrip("/")
        self.logger.debug("Saving dataset to %s", out_path)

        ps = ParquetSaver(
            df_result=df,
            parquet_storage_path=out_path,
            engine="pyarrow",
            fs=self.fs,
            partition_on=["partition_date"],
            write_index=False,
        )
        await asyncio.to_thread(ps.save_to_parquet)

        await self.emit("complete", message="All partitions written.")

    # ------------------------------------------------------------------
    # Read from Parquet
    # ------------------------------------------------------------------
    async def from_parquet(self, **kwargs) -> dd.DataFrame:
        reader = ParquetReader(
            parquet_start_date=self.start_date,
            parquet_end_date=self.end_date,
            parquet_storage_path=self.storage_path,
            fs=self.fs,
            debug=self.debug,
            logger=self.logger,
            dask_client=self.dask_client,
        )
        self.logger.debug(f"Reading from Parquet path: {self.storage_path}")
        return await reader.aload(**kwargs)

    # ------------------------------------------------------------------
    # Write to ClickHouse
    # ------------------------------------------------------------------
    async def to_clickhouse(self, clk_conf: dict, **kwargs):
        from sibi_dst.utils import ClickHouseWriter

        df = await self.from_parquet(**kwargs)
        if dask_is_empty(df, dask_client=self.dask_client):
            self.logger.warning("No data to write to ClickHouse.")
            return

        df = df.assign(
            _date_col=dd.to_datetime(df[self.date_field], errors="coerce")
        )
        df = _safe_persist(df, dask_client=self.dask_client)

        # Get unique dates
        unique_dates_series = df["_date_col"].dt.date.dropna().unique()
        unique_dates = await asyncio.to_thread(lambda: _safe_compute(unique_dates_series, self.dask_client))
        unique_dates = list(pd.Series(unique_dates).dropna().dt.date.unique())

        if not unique_dates:
            self.logger.warning("No valid dates found for partitioning.")
            return

        clk_conf['table'] = self.filename
        clk_conf['debug'] = self.debug
        clk_conf['logger'] = self.logger
        clk = ClickHouseWriter(**clk_conf)
        loop = asyncio.get_running_loop()
        tasks = []

        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            for date_val in unique_dates:
                df_day = df[df["_date_col"].dt.date == date_val].drop(columns=["_date_col"])
                if dask_is_empty(df_day, dask_client=self.dask_client):
                    continue

                # Count rows (optional)
                n_rows = await asyncio.to_thread(
                    lambda: _safe_compute(df_day.map_partitions(len).sum(), self.dask_client))
                self.logger.debug(f"[ClickHouse] Writing {int(n_rows)} rows for {date_val}")

                tasks.append(
                    loop.run_in_executor(executor, clk.save_to_clickhouse, df_day)
                )

            await asyncio.gather(*tasks)

        self.logger.info(f"ClickHouse write complete for {len(unique_dates)} daily partitions.")

__all__ = ["BasePipeline"]