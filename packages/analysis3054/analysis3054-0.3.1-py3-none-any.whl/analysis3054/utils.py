"""
Utility functions for data manipulation and merging.

This module provides several helpers for combining and transforming
pandas DataFrames.  These utilities are designed to support typical
workflows encountered in commodity analysis, where disparate data
sources must be merged on a variety of keys or aligned in time.  In
addition to straightforward column and row merges, more advanced
matching strategies are implemented, such as nearest‑key joins and
coalescing overlaps.  All functions expect pandas DataFrames and
preserve the index and data types wherever possible.

Included are:

* :func:`conditional_column_merge` – Merge one or more columns from an
  auxiliary DataFrame into a primary DataFrame based on matching key
  values.  Supports matching on multiple values by splitting a
  delimiter‑separated key column.

* :func:`conditional_row_merge` – Append rows from an auxiliary
  DataFrame to a primary DataFrame when a specified column contains
  values found in a list of keys.  Useful for selectively augmenting
  a dataset with additional observations.

* :func:`nearest_key_merge` – Join two DataFrames by matching on the
  closest value of a numeric key within a specified tolerance.  This
  is helpful when exact matches are rare or when values represent
  continuous measurements (e.g. timestamps or price levels).

* :func:`coalesce_merge` – Merge two DataFrames on a set of keys and
  coalesce overlapping columns, preferring non‑null values from the
  left DataFrame.  This can be used to combine cleaned and raw
  datasets while retaining the most reliable data.

* :func:`rolling_fill` – Fill missing values in numeric columns using
  a rolling window statistic (mean, median, etc.).  This provides a
  simple yet effective way to impute gaps without distorting trends.

Each function is accompanied by a docstring explaining its usage and
parameters.  See the examples in the package documentation for
guidance on how to apply these utilities in your analyses.
"""

from __future__ import annotations

from typing import Iterable, List, Optional, Sequence, Tuple, Union

import numpy as np
import pandas as pd


def conditional_column_merge(
    df: pd.DataFrame,
    other: pd.DataFrame,
    *,
    df_key: Union[str, Sequence[str]],
    other_key: Union[str, Sequence[str]],
    columns: Union[str, List[str]],
    delimiter: str = '|',
    multiple: bool = False,
    suffix: str = '_y',
) -> pd.DataFrame:
    """Merge selected columns from ``other`` into ``df`` based on key values.

    This function performs a left join of ``df`` with ``other``, adding
    one or more columns from ``other`` when values in the key column(s)
    match.  When ``multiple`` is ``True``, the key column in ``df`` can
    contain delimiter‑separated lists of values; the merge will occur if
    **any** of the values matches the corresponding key in ``other``.

    Parameters
    ----------
    df : pandas.DataFrame
        Primary DataFrame to which columns will be added.
    other : pandas.DataFrame
        Auxiliary DataFrame containing the columns to merge.
    df_key : str or list of str
        Column(s) in ``df`` on which to match.  If ``multiple`` is
        ``True`` and a single string is provided, values in this column
        may be delimiter‑separated lists of keys.
    other_key : str or list of str
        Column(s) in ``other`` on which to match.  Must align with
        ``df_key``.  Composite keys are supported by providing lists.
    columns : str or list of str
        Name(s) of the column(s) in ``other`` to merge into ``df``.
    delimiter : str, default ``'|'``
        Delimiter used to split multi‑value keys when ``multiple`` is
        ``True``.
    multiple : bool, default ``False``
        Whether to treat the key column in ``df`` as containing
        delimiter‑separated lists of values.  If ``False``, an exact
        match on the key(s) is required.
    suffix : str, default ``'_y'``
        Suffix to append to merged column names if there is a
        collision with existing column names in ``df``.

    Returns
    -------
    pandas.DataFrame
        A copy of ``df`` with the selected columns from ``other``
        merged in.  Rows in ``df`` that do not match any key in
        ``other`` will contain ``NaN`` for the merged columns.
    """
    df_keys = [df_key] if isinstance(df_key, str) else list(df_key)
    other_keys = [other_key] if isinstance(other_key, str) else list(other_key)
    if len(df_keys) != len(other_keys):
        raise ValueError("df_key and other_key must have the same number of elements")
    columns_to_add = [columns] if isinstance(columns, str) else list(columns)
    other_merge = other[other_keys + columns_to_add].copy()
    if multiple and len(df_keys) == 1:
        key = df_keys[0]
        exploded = df[[key]].copy()
        exploded[key] = exploded[key].astype(str).str.split(delimiter)
        exploded = exploded.explode(key)
        exploded['_orig_index'] = exploded.index
        merged = exploded.merge(other_merge, left_on=key, right_on=other_keys[0], how='left')
        agg_dict = {col: 'first' for col in columns_to_add}
        aggregated = merged.groupby('_orig_index')[columns_to_add].agg(agg_dict)
        aggregated.index = df.index
        result = df.copy()
        for col in columns_to_add:
            new_name = col if col not in result.columns else f"{col}{suffix}"
            result[new_name] = aggregated[col]
        return result
    else:
        result = df.merge(other_merge, left_on=df_keys, right_on=other_keys, how='left', suffixes=('', suffix))
        for k in other_keys:
            if k in result.columns and k not in df_keys:
                result = result.drop(columns=k)
        return result


def conditional_row_merge(
    df: pd.DataFrame,
    other: pd.DataFrame,
    *,
    key_col: str,
    values: Iterable,
    how: str = 'append',
) -> pd.DataFrame:
    """Append or replace rows in ``df`` based on matches in ``other``.

    Parameters
    ----------
    df : pandas.DataFrame
        Primary DataFrame.
    other : pandas.DataFrame
        Secondary DataFrame from which rows are selected.
    key_col : str
        Column name in both DataFrames on which to match.
    values : iterable
        Values to match in ``other[key_col]``.
    how : {'append','replace'}, default 'append'
        If ``'append'``, matching rows from ``other`` are appended to
        ``df``.  If ``'replace'``, matching rows in ``df`` are removed
        before appending.

    Returns
    -------
    pandas.DataFrame
        DataFrame with rows appended or replaced.
    """
    sel = other[other[key_col].isin(values)]
    result = df.copy()
    if how not in ['append', 'replace']:
        raise ValueError("how must be 'append' or 'replace'")
    if how == 'replace':
        result = result[~result[key_col].isin(values)]
    combined = pd.concat([result, sel], axis=0, ignore_index=True)
    return combined


def nearest_key_merge(
    df: pd.DataFrame,
    other: pd.DataFrame,
    *,
    df_key: str,
    other_key: str,
    tolerance: Optional[float] = None,
    direction: str = 'nearest',
    suffix: str = '_y',
) -> pd.DataFrame:
    """Merge ``df`` and ``other`` on the nearest numeric key within a tolerance.

    See module documentation for details.
    """
    if df_key not in df.columns or other_key not in other.columns:
        raise KeyError("df_key or other_key column not found in the provided DataFrames")
    # Ensure both keys are numeric and comparable
    # Use astype(float) to align dtypes; invalid parsing will raise
    # Convert key columns to numeric once for efficient comparison
    # Avoid modifying original DataFrames; operate on shallow copies
    df_sorted = df.copy()
    other_sorted = other.copy()
    df_sorted[df_key] = pd.to_numeric(df_sorted[df_key], errors='coerce').astype(float)
    other_sorted[other_key] = pd.to_numeric(other_sorted[other_key], errors='coerce').astype(float)
    df_sorted = df_sorted.sort_values(df_key, kind='mergesort').reset_index(drop=True)
    other_sorted = other_sorted.sort_values(other_key, kind='mergesort').reset_index(drop=True)
    merged = pd.merge_asof(
        df_sorted,
        other_sorted,
        left_on=df_key,
        right_on=other_key,
        direction=direction,
        tolerance=tolerance,
        suffixes=('', suffix),
    )
    merged = merged.sort_index()
    return merged


def coalesce_merge(
    df: pd.DataFrame,
    other: pd.DataFrame,
    *,
    on: Union[str, List[str]],
    prefer: str = 'df',
    suffix: str = '_other',
) -> pd.DataFrame:
    """Merge and coalesce overlapping columns, preferring non‑null values.

    See module documentation for details.
    """
    on_cols = [on] if isinstance(on, str) else list(on)
    merged = df.merge(other, on=on_cols, how='outer', suffixes=('', suffix))
    result = merged.copy()
    overlap = set(df.columns).intersection(other.columns) - set(on_cols)
    for col in overlap:
        other_col = f"{col}{suffix}"
        if prefer == 'df':
            result[col] = merged[col].combine_first(merged[other_col])
        else:
            result[col] = merged[other_col].combine_first(merged[col])
        result = result.drop(columns=other_col)
    return result


def rolling_fill(
    df: pd.DataFrame,
    *,
    window: int = 3,
    method: str = 'mean',
    min_periods: Optional[int] = 1,
) -> pd.DataFrame:
    """Fill missing numeric values using a rolling window statistic.

    See module documentation for details.
    """
    numeric_cols = [c for c in df.columns if pd.api.types.is_numeric_dtype(df[c])]
    result = df.copy()
    for col in numeric_cols:
        series = df[col]
        if method == 'mean':
            stat = series.rolling(window, min_periods=min_periods).mean()
        elif method == 'median':
            stat = series.rolling(window, min_periods=min_periods).median()
        elif method == 'min':
            stat = series.rolling(window, min_periods=min_periods).min()
        elif method == 'max':
            stat = series.rolling(window, min_periods=min_periods).max()
        else:
            raise ValueError("method must be 'mean', 'median', 'min' or 'max'")
        filled = series.fillna(stat)
        result[col] = filled
    return result


def data_quality_report(df: pd.DataFrame) -> pd.DataFrame:
    """Generate a basic data quality report for a pandas DataFrame.

    This utility inspects each column of ``df`` and computes common
    diagnostics, including data type, number of missing values,
    percentage missing, number of unique values and example values.
    The resulting report is useful for quickly assessing the quality
    and characteristics of a dataset before proceeding with analysis.

    Parameters
    ----------
    df : pandas.DataFrame
        Input DataFrame to profile.

    Returns
    -------
    pandas.DataFrame
        A report with one row per column.  Columns include:

        ``'dtype'`` – the pandas dtype;
        ``'missing_count'`` – number of missing entries;
        ``'missing_pct'`` – percentage of missing entries;
        ``'unique_count'`` – number of unique values (up to a limit);
        ``'example'`` – a representative non‑missing value or None.

    Notes
    -----
    For columns with many unique values, counting all uniques may be
    expensive.  A heuristic is used to approximate the unique count
    when the number exceeds 10000.
    """
    report_data = []
    n_rows = len(df)
    for col in df.columns:
        series = df[col]
        dtype = series.dtype
        missing_count = series.isna().sum()
        missing_pct = missing_count / n_rows * 100 if n_rows > 0 else np.nan
        # Unique count with heuristic for large cardinality
        if series.nunique(dropna=True) > 10000:
            unique_count = '>10000'
        else:
            unique_count = series.nunique(dropna=True)
        # Example value
        example = None
        non_na = series.dropna()
        if not non_na.empty:
            example = non_na.iloc[0]
        report_data.append({
            'column': col,
            'dtype': str(dtype),
            'missing_count': int(missing_count),
            'missing_pct': float(missing_pct),
            'unique_count': unique_count,
            'example': example,
        })
    return pd.DataFrame(report_data).set_index('column')


def df_split(
    df: pd.DataFrame,
    date_col: str,
    target_col: str,
    *,
    split_date: Optional[Union[str, pd.Timestamp]] = None,
    split_index: Optional[int] = None,
    include_split: bool = False,
    dropna_target: bool = False,
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Split a time series DataFrame into historical and future parts.

    This utility partitions a DataFrame containing a datetime column and a
    target column into two subsets: one containing the historical data
    (training context) and the other containing the future horizon.  It
    provides several ways to define the split point.

    Parameters
    ----------
    df : pandas.DataFrame
        Input DataFrame containing at least a datetime column and a
        target column.  The DataFrame should be sorted by the datetime
        column in ascending order.
    date_col : str
        Name of the datetime column in ``df``.  This column is used to
        determine the split point when ``split_date`` is provided.
    target_col : str
        Name of the target column in ``df``.  When neither
        ``split_date`` nor ``split_index`` is specified, the function
        finds the last non‑missing value in this column and splits
        immediately after that observation.
    split_date : str or pandas.Timestamp, optional
        Explicit date at which to split.  All rows with
        ``df[date_col]`` strictly less than ``split_date`` (or
        ``<=`` when ``include_split`` is True) are placed in the
        historical DataFrame; the remainder belong to the future DataFrame.
        ``split_date`` is converted to ``datetime64`` using
        ``pandas.to_datetime``.
    split_index : int, optional
        Integer position at which to split the DataFrame.  If
        non‑negative, the first ``split_index`` rows go to the
        historical DataFrame.  Negative indices are interpreted as
        positions from the end.  If both ``split_date`` and
        ``split_index`` are provided, ``split_date`` takes precedence.
    include_split : bool, default False
        Whether to include the row that matches the split point in
        the historical DataFrame.  If ``True`` and ``split_date`` is
        provided, rows with ``df[date_col] == split_date`` are kept in
        the historical DataFrame; otherwise they are included in the
        future DataFrame.  Likewise, when splitting by index,
        ``include_split`` controls whether the row at ``split_index``
        belongs to the historical part.
    dropna_target : bool, default False
        If ``True``, drop rows where the target column is missing
        before determining the last non‑missing value.  When
        ``False``, the last non‑null value is searched in the original
        order including NaNs.

    Returns
    -------
    (pandas.DataFrame, pandas.DataFrame)
        A tuple ``(historical, future)`` where ``historical``
        contains the portion of the data before the split point and
        ``future`` contains the portion at or after the split point.

    Notes
    -----
    Use this helper to prepare datasets for forecasting functions.
    For example, you can train models on the historical DataFrame and
    evaluate forecasts against the future DataFrame.  You can also
    specify ``split_date`` to align the context with a known cut‑off
    point, such as the last observed value in a training set.
    """
    df = df.copy()
    if date_col not in df.columns:
        raise KeyError(f"date_col '{date_col}' not found in DataFrame")
    if target_col not in df.columns:
        raise KeyError(f"target_col '{target_col}' not found in DataFrame")
    # Ensure datetime conversion
    df[date_col] = pd.to_datetime(df[date_col], errors="coerce")
    # Determine split index
    if split_date is not None:
        # Convert and split by date
        split_ts = pd.to_datetime(split_date)
        if include_split:
            hist_mask = df[date_col] <= split_ts
        else:
            hist_mask = df[date_col] < split_ts
        historical = df.loc[hist_mask].copy()
        future = df.loc[~hist_mask].copy()
    elif split_index is not None:
        # Split by positional index
        if split_index < 0:
            split_index = len(df) + split_index
        if include_split:
            cut = split_index + 1
        else:
            cut = split_index
        historical = df.iloc[:cut].copy()
        future = df.iloc[cut:].copy()
    else:
        # Split after last non‑missing target
        series = df[target_col]
        if dropna_target:
            non_na_idx = series.dropna().index
        else:
            non_na_idx = series[series.notna()].index
        if non_na_idx.size == 0:
            # If no non‑missing values, return empty historical
            historical = df.iloc[[]].copy()
            future = df.copy()
        else:
            last_idx = non_na_idx.max()
            # Determine cut based on last non‑missing row
            cut = df.index.get_loc(last_idx)
            if include_split:
                cut += 1
            historical = df.iloc[:cut].copy()
            future = df.iloc[cut:].copy()
    return historical.reset_index(drop=True), future.reset_index(drop=True)
