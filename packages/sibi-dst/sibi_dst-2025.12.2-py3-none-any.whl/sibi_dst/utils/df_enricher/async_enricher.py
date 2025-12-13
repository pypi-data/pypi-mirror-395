from __future__ import annotations

import asyncio
from typing import Any, Dict, List, Optional, Sequence, Tuple, Union

import pandas as pd
import dask.dataframe as dd

from sibi_dst.utils import ManagedResource
from .types import DdfLike
from .specs import AttachmentSpec
from .merger import DfMerger


class AsyncDfEnricher(ManagedResource):
    """
    Generic async DataFrame enricher driven by AttachmentSpec definitions.

    - Uses a base DataFrame (Pandas or Dask).
    - Chooses applicable AttachmentSpecs based on required_cols.
    - Extracts unique values per spec.col_to_kwarg.
    - Runs all attachment_fn calls concurrently.
    - Merges results using DfMerger.
    """

    def __init__(
        self,
        base_df: DdfLike,
        specs: Sequence[AttachmentSpec],
        **kwargs: Any,
    ) -> None:
        super().__init__(**kwargs)
        self.specs = list(specs)
        self.df: dd.DataFrame = (
            base_df if isinstance(base_df, dd.DataFrame)
            else dd.from_pandas(base_df, npartitions=1)
        )

    @staticmethod
    def _unique_list(series: Union[pd.Series, dd.Series]) -> List[Any]:
        if isinstance(series, pd.Series):
            return series.dropna().unique().tolist()
        return series.dropna().unique().compute().tolist()

    async def _run_attachments(
        self,
        cols: Sequence[str],
    ) -> Tuple[Dict[str, Optional[DdfLike]], List[AttachmentSpec]]:
        available_cols = [c for c in cols if c in self.df.columns]

        tasks: Dict[str, "asyncio.Task[Any]"] = {}
        used_specs: List[AttachmentSpec] = []

        for spec in self.specs:
            if not spec.is_applicable(available_cols):
                continue

            kwargs_for_fn: Dict[str, Any] = {}
            for col, kw in spec.col_to_kwarg.items():
                if col not in self.df.columns:
                    continue
                kwargs_for_fn[kw] = self._unique_list(self.df[col])

            if not kwargs_for_fn:
                continue

            tasks[spec.key] = asyncio.create_task(spec.attachment_fn(**kwargs_for_fn))
            used_specs.append(spec)

        results: Dict[str, Optional[DdfLike]] = {}
        if tasks:
            done = await asyncio.gather(*tasks.values(), return_exceptions=True)
            for name, result in zip(tasks.keys(), done):
                if isinstance(result, Exception):
                    self.logger.warning(f"Attachment %s failed: %s", name, result)
                    results[name] = None
                else:
                    results[name] = result

        return results, used_specs

    async def enrich(
        self,
        cols: Sequence[str],
        *,
        normalize_persist: bool = False,
        persist_result: bool = False,
    ) -> dd.DataFrame:
        if not cols:
            raise ValueError("Pass at least one column to drive enrichment.")

        results, used_specs = await self._run_attachments(cols)
        if not used_specs:
            return self.df.persist() if persist_result else self.df

        merge_plan: List[Tuple[str, List[str], List[str], List[str]]] = [
            (spec.key, spec.left_on, spec.right_on, spec.drop_cols)
            for spec in used_specs
        ]

        merger = DfMerger(logger=self.logger, debug=self.debug)
        enriched = merger.apply_merges(
            base_df=self.df,
            results=results,
            merge_plan=merge_plan,
            normalize_persist=normalize_persist,
        )

        if persist_result:
            enriched = enriched.persist()

        self.df = enriched
        return enriched