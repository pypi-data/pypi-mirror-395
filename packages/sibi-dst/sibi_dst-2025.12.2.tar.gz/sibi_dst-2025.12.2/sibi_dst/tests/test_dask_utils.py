import asyncio

import numpy as np
import pandas as pd
import dask.dataframe as dd

from sibi_dst.utils.dask_utils import (
    dask_is_probably_empty,
    dask_is_empty,
    dask_is_empty_truthful,
    UniqueValuesExtractor,
)


def test_dask_is_probably_empty_true_for_no_columns():
    # Dask dataframe with no columns should be "probably empty"
    ddf = dd.from_pandas(pd.DataFrame(), npartitions=1)
    assert dask_is_probably_empty(ddf) is True


def test_dask_is_empty_true_for_empty_dataframe():
    # Empty dataframe (has columns but no rows) should be detected as empty
    df = pd.DataFrame({"x": []})
    ddf = dd.from_pandas(df, npartitions=2)
    assert dask_is_empty(ddf) is True
    assert dask_is_empty_truthful(ddf) is True


def test_dask_is_empty_false_for_nonempty_dataframe():
    # Non-empty dataframe should return False for emptiness checks
    df = pd.DataFrame({"x": list(range(8))})
    ddf = dd.from_pandas(df, npartitions=4)
    assert dask_is_empty(ddf) is False
    assert dask_is_empty_truthful(ddf) is False


def test_unique_values_extractor_pandas_and_dask():
    df = pd.DataFrame({"a": [1, 2, 2, None], "b": ["x", "y", "x", None]})
    extractor = UniqueValuesExtractor()

    # pandas DataFrame case (synchronous underlying structures)
    res_pd = asyncio.run(extractor.extract_unique_values(df, "a", "b"))
    assert set(res_pd["a"]) == {1, 2}
    assert set(res_pd["b"]) == {"x", "y"}

    # dask DataFrame case (requires compute)
    ddf = dd.from_pandas(df, npartitions=2)
    res_dd = asyncio.run(extractor.extract_unique_values(ddf, "a", "b"))
    assert set(res_dd["a"]) == {1, 2}
    assert set(res_dd["b"]) == {"x", "y"}


def test_compute_to_list_with_numpy_array():
    extractor = UniqueValuesExtractor()
    res = asyncio.run(extractor.compute_to_list(np.array([1, 2, 2, None])))
    assert set(res) == {1, 2}