from typing import Sequence, Union

import numpy as np
import pandas as pd

from superleaf.dataframe.column_ops import Col, ColOp, Index
from superleaf.collections.ordered_set import OrderedSet


def _pass_filter(df: pd.DataFrame | pd.Series, *filters, **col_filters) -> np.ndarray[bool]:
    row_bools = np.ones(len(df)).astype(bool)
    for filt in filters:
        if isinstance(filt, ColOp):
            row_bools = row_bools & filt(df)
        elif callable(filt):
            if isinstance(df, pd.DataFrame):
                row_bools = row_bools & df.apply(filt, axis=1)
            else:
                row_bools = row_bools & filt(df)
        else:
            try:
                row_bools = row_bools & np.array(list(filt))
            except Exception:
                raise TypeError(
                    "Positional filters must be column operators or callables to apply to each row"
                )
    for col, filt in col_filters.items():
        if isinstance(df, pd.Series) and col.lower() == "index":
            col_getter = Index()
        else:
            col_getter = Col(col)
        if isinstance(filt, ColOp) or not callable(filt):
            row_bools = row_bools & (col_getter == filt)(df)
        elif callable(filt):
            row_bools = row_bools & col_getter.map(filt)(df)
        else:
            raise TypeError(
                "Keyword filters must be values, column operators, or callables to apply to each value in the column"
            )
    return row_bools


def dfilter(df: pd.DataFrame, *filters, **col_filters) -> pd.DataFrame:
    """Filters a DataFrame by applying provided conditions.

    Parameters
    ----------
    df : pd.DataFrame
        The DataFrame to filter.
    *filters
        Variable positional arguments that can be:
        - Instances of ColOp.
        - Callables applied row-wise, returning boolean values.
        - Iterable of boolean values indicating row selection.
    **col_filters
        Keyword arguments mapping column names to conditions, which can be:
        - Values (equality filter).
        - Instances of ColOp.
        - Callables applied element-wise to the specified column.

    Returns
    -------
    pd.DataFrame
        A copy of the DataFrame containing only rows satisfying all filters.

    Examples
    --------
    >>> filtered_df = dfilter(df, Col('age') > 30, status='active')
    """
    return df[_pass_filter(df, *filters, **col_filters)].copy()


def partition(df: pd.DataFrame, *filters, **col_filters) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Partitions a DataFrame into two subsets based on provided filtering conditions.

    Parameters
    ----------
    df : pd.DataFrame
        The DataFrame to partition.
    *filters
        Variable positional arguments (see ``dfilter`` documentation).
    **col_filters
        Keyword arguments (see ``dfilter`` documentation).

    Returns
    -------
    tuple[pd.DataFrame, pd.DataFrame]
        - First DataFrame contains rows matching the provided filters.
        - Second DataFrame contains rows that do not match.

    Example
    -------
    >>> passed_df, failed_df = partition(df, score=lambda x: x > 50)
    """
    row_bools = _pass_filter(df, *filters, **col_filters)
    return df[row_bools].copy(), df[~row_bools].copy()


def reorder_columns(
        df: pd.DataFrame,
        columns: Union[str, Sequence[str]],
        back=False,
        after=None,
        before=None,
) -> pd.DataFrame:
    """Reorders columns in a DataFrame based on the provided parameters.

    Parameters
    ----------
    df : pd.DataFrame
        The DataFrame whose columns to reorder.
    columns : Union[str, Sequence[str]])
        Column name or sequence of column names to reorder.
    back : bool, optional
        If True, moves specified columns to the end. Default is False.
    after : str, optional
        Column name after which the specified columns should be placed. Default is None.
    before : str, optional
        Column name before which the specified columns should be placed. Default is None.

    Returns
    -------
    pd.DataFrame
        A new DataFrame with reordered columns.

    Notes
    -----
    Exactly one of ``back``, ``after``, or ``before`` can be used at a time.

    Raises
    ------
    ValueError
        If more than one of ``back``, ``after``, or ``before`` parameters are provided simultaneously.

    Examples
    --------
    >>> reordered_df = reorder_columns(df, ['age', 'name'], after='id')
    """
    if isinstance(columns, str):
        columns = [columns]
    df_cols = OrderedSet(df.columns)
    columns = OrderedSet(columns)
    if sum([back, after is not None, before is not None]) > 1:
        raise ValueError("Only one of the following parameters can be used at a time: (back, after, before)")
    if back:
        col_order = list((df_cols - columns) + columns)
    elif after or before:
        if after:
            insert_idx = list(df.columns).index(after) + 1
        else:  # before -- already enforced that before and after cannot both be True
            insert_idx = list(df.columns).index(before)
        col_order = list((OrderedSet(df_cols[:insert_idx]) - columns) + columns + OrderedSet(df_cols[insert_idx:]))
    else:
        col_order = list(columns + df_cols)
    return pd.DataFrame(df[col_order])
