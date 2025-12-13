from __future__ import annotations

from dataclasses import dataclass
from typing import Awaitable, Callable, Dict, Iterable, List, Set, Union

import dask.dataframe as dd
import pandas as pd

DdfLike = Union[dd.DataFrame, pd.DataFrame]


@dataclass
class AttachmentSpec:
    """
    Declarative description of how to attach extra info.

    key:
        Identifier used for results and merge_plan.
    required_cols:
        Columns that must be present in the base df to trigger this attachment.
    attachment_fn:
        Async function returning a DataFrame-like object.
    col_to_kwarg:
        Mapping from base df column -> kwarg name for attachment_fn.
        The value of each column is passed as `kwarg_name=<list_of_unique_values>`.
    left_on / right_on / drop_cols:
        Merge instructions for DfMerger.
    """
    key: str
    required_cols: Set[str]
    attachment_fn: Callable[..., Awaitable[DdfLike]]
    col_to_kwarg: Dict[str, str]
    left_on: List[str]
    right_on: List[str]
    drop_cols: List[str]

    def is_applicable(self, available_cols: Iterable[str]) -> bool:
        return self.required_cols.issubset(set(available_cols))