from __future__ import annotations

from typing import Union
import pandas as pd
import dask.dataframe as dd

DdfLike = Union[dd.DataFrame, pd.DataFrame]