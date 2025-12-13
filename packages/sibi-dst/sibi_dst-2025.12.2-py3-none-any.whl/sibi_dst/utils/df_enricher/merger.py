from __future__ import annotations

from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple, Union

import pandas as pd
import dask.dataframe as dd

from sibi_dst.utils import ManagedResource

DdfLike = Union[dd.DataFrame, pd.DataFrame]


class DfMerger(ManagedResource):
    """
    Generic Dask/Pandas DataFrame merger with integrated join-key normalization.

    Responsibilities:
      - Normalize incoming objects to Dask DataFrames.
      - Normalize join-key dtypes (left/right) to 'string' when mismatched.
      - Apply a sequence of left merges according to a merge plan.

    Parameters (via **kwargs):
      - logger, debug: handled by ManagedResource.
      - dask_client: optional, kept for symmetry with other components.
    """

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.dask_client = kwargs.get("dask_client")
        # Track dtype normalization changes for logging/inspection
        self._dtype_changes: Dict[str, Dict[str, str]] = {}

    # ------------------------------------------------------------------
    # Normalization helpers (from MergeNormalizer)
    # ------------------------------------------------------------------

    @staticmethod
    def _cast_to_string(part: pd.DataFrame, columns_to_cast: List[str]) -> pd.DataFrame:
        """Convert specified columns to string dtype safely within a partition."""
        for col in columns_to_cast:
            if col in part.columns:
                part[col] = part[col].astype("string")
        return part

    def _normalize_merge_dtypes(
        self,
        df: dd.DataFrame,
        results: Dict[str, Optional[dd.DataFrame]],
        merge_plan: Iterable[Tuple[str, List[str], List[str], List[str]]],
        persist: bool = False,
    ) -> Tuple[dd.DataFrame, Dict[str, Optional[dd.DataFrame]]]:
        """
        Normalize join key dtypes to 'string' across the base df and related result dfs.

        Returns
        -------
        (normalized_df, normalized_results)
        """
        if not results:
            return df, results

        columns_to_normalize = set()

        # Identify mismatched dtypes on left side
        for key, left_on, right_on, _ in merge_plan:
            other = results.get(key)
            if other is None:
                continue
            for lcol, rcol in zip(left_on, right_on):
                if lcol in df.columns and rcol in other.columns:
                    if df[lcol].dtype != other[rcol].dtype:
                        columns_to_normalize.add(lcol)

        if not columns_to_normalize:
            # Nothing to normalize
            return df, results

        # Record planned conversions
        self._dtype_changes.clear()
        for col in columns_to_normalize:
            base_dtype = str(df[col].dtype)
            self._dtype_changes[col] = {base_dtype: "string"}

        # Normalize base DataFrame
        cols_in_df = [c for c in columns_to_normalize if c in df.columns]
        if cols_in_df:
            meta_df = df._meta.astype({c: "string" for c in cols_in_df})
            df = df.map_partitions(
                self._cast_to_string,
                columns_to_cast=cols_in_df,
                meta=meta_df,
            )

        # Normalize related DataFrames
        normalized_results: Dict[str, Optional[dd.DataFrame]] = {}
        for key, other in results.items():
            if other is None:
                normalized_results[key] = None
                continue

            # Determine which right-side columns to normalize for this key
            right_cols: List[str] = []
            for plan_key, left_on, right_on, _ in merge_plan:
                if plan_key == key:
                    for lcol, rcol in zip(left_on, right_on):
                        if lcol in columns_to_normalize and rcol in other.columns:
                            right_cols.append(rcol)
                    break

            if right_cols:
                meta_other = other._meta.astype({c: "string" for c in right_cols})
                other = other.map_partitions(
                    self._cast_to_string,
                    columns_to_cast=right_cols,
                    meta=meta_other,
                )

            normalized_results[key] = other

        # Optional persistence for large DAGs
        if persist:
            df = df.persist()
            normalized_results = {
                k: v.persist() if isinstance(v, dd.DataFrame) else v
                for k, v in normalized_results.items()
            }

        return df, normalized_results

    def log_normalization_changes(self) -> None:
        """Log dtype normalization actions (left join keys)."""
        if not self.logger or not self._dtype_changes:
            return

        for col, mapping in self._dtype_changes.items():
            self.logger.info(f"Join key {col!r} normalized to 'string'")
            for src, tgt in mapping.items():
                self.logger.debug(f"  Cast {col!r}: {src} → {tgt}")

    def normalization_changes_as_dataframe(self) -> pd.DataFrame:
        """Return dtype changes as a pandas DataFrame for inspection."""
        records = []
        for col, mapping in self._dtype_changes.items():
            for src, tgt in mapping.items():
                records.append(
                    {"column": col, "source_dtype": src, "target_dtype": tgt}
                )
        return pd.DataFrame.from_records(records)

    # ------------------------------------------------------------------
    # Generic Dask/Pandas helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _to_ddf(obj: Any) -> Optional[dd.DataFrame]:
        """Normalize arbitrary objects into a Dask DataFrame or None."""
        if obj is None:
            return None
        if isinstance(obj, dd.DataFrame):
            return obj
        if isinstance(obj, pd.DataFrame):
            return dd.from_pandas(obj, npartitions=1)
        if isinstance(obj, dict):
            return dd.from_pandas(pd.DataFrame([obj]), npartitions=1)
        if isinstance(obj, list) and obj and all(isinstance(r, dict) for r in obj):
            return dd.from_pandas(pd.DataFrame(obj), npartitions=1)
        raise TypeError(f"Unexpected type for merge: {type(obj)}")

    @staticmethod
    def _drop_cols(df: dd.DataFrame, cols_to_drop: Sequence[str]) -> dd.DataFrame:
        """Drop columns that actually exist in the frame."""
        to_drop = [c for c in cols_to_drop if c in df.columns]
        return df.drop(columns=to_drop) if to_drop else df

    # ------------------------------------------------------------------
    # Single merge (assumes dtypes already normalized)
    # ------------------------------------------------------------------

    def _merge_left(
        self,
        left: dd.DataFrame,
        right_like: Optional[dd.DataFrame],
        *,
        left_on: Sequence[str],
        right_on: Sequence[str],
    ) -> dd.DataFrame:
        """
        Perform a left merge between `left` and `right_like` on the given keys.
        Assumes join-key dtypes have already been normalized.
        """
        if right_like is None:
            return left

        right = right_like
        return left.merge(
            right,
            how="left",
            left_on=list(left_on),
            right_on=list(right_on),
        )

    # ------------------------------------------------------------------
    # Merge driver
    # ------------------------------------------------------------------

    def apply_merges(
        self,
        base_df: DdfLike,
        results: Dict[str, Optional[DdfLike]],
        merge_plan: Iterable[Tuple[str, List[str], List[str], List[str]]],
        *,
        normalize_persist: bool = False,
    ) -> dd.DataFrame:
        """
        Apply a sequence of left merges defined by `merge_plan`.

        Parameters
        ----------
        base_df:
            Base DataFrame (Pandas or Dask) to be enriched.
        results:
            Mapping from merge key to auxiliary frame (or None).
        merge_plan:
            Iterable of tuples:
              (key, left_on, right_on, drop_cols)
        normalize_persist:
            If True, persist base and auxiliary frames after dtype normalization.

        Returns
        -------
        dd.DataFrame
            Enriched Dask DataFrame.
        """
        # Ensure we work with Dask for the base
        df = base_df if isinstance(base_df, dd.DataFrame) else dd.from_pandas(base_df, npartitions=1)

        # Ensure all auxiliary results are dd.DataFrame or None
        dd_results: Dict[str, Optional[dd.DataFrame]] = {}
        for key, val in results.items():
            dd_results[key] = self._to_ddf(val) if val is not None else None

        # Normalize join-key dtypes across base and related frames
        df, norm_results = self._normalize_merge_dtypes(df, dd_results, merge_plan, persist=normalize_persist)
        self.log_normalization_changes()

        # Apply merges
        out = df
        for key, left_on, right_on, drop_cols in merge_plan:
            other = norm_results.get(key)
            if other is None:
                continue
            out = self._merge_left(out, other, left_on=left_on, right_on=right_on)
            out = self._drop_cols(out, drop_cols)

        return out


