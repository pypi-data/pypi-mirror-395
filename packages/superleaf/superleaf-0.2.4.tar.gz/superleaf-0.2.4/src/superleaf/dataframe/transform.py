import json
from typing import Optional

import numpy as np
import pandas as pd

from superleaf.collections import OrderedSet


def notna(x) -> bool:
    try:
        # Faster operation is to use x==x, but list of null would return True
        return x is not None and not np.isnan(x)
    except ValueError:
        return x is not None and not np.any(np.isnan(x))
    except TypeError:
        return x is not None


def expand_dict_to_cols(
        df: pd.DataFrame,
        cols,
        fields=None,
        with_col_prefix=True,
        prefix='',
        prefix_fun=None,
        sep='_',
        drop=True,
        dropna=False,
        col_renamer=None,
        recursive=False,
        uniform_keys=False,
        default=np.nan,
) -> pd.DataFrame:
    """Expand dictionary-like values in one or more DataFrame columns into new, flat columns.

    For each column in ``cols``, dictionary-like entries are unpacked into separate
    columns (one per key). You can control which keys to expand, how to name the new
    columns, whether to drop the original columns, and whether nested dictionaries
    should be expanded recursively.

    Parameters
    ----------
    df : pd.DataFrame
        The input DataFrame.
    cols : str or Sequence[str]
        Column name or list of column names whose values are dicts to expand.
    fields : str or Sequence[str], optional
        Specific keys to extract from each dict. If None, all keys encountered
        (or, if ``uniform_keys=True``, the keys from the first non-null dict) will
        be used.
    with_col_prefix : bool, optional
        If True, prefix new column names with the source column name and ``sep``.
        If False, only ``prefix`` (if provided) is used.
    prefix : str, optional
        A string to prepend to all new column names.
    prefix_fun : callable, optional
        Function mapping (col_name, current_prefix) to a new prefix.
    sep : str, optional
        Separator between prefix and field name. Default is '_'.
    drop : bool, optional
        If True, drop the original columns from the output DataFrame.
    dropna : bool, optional
        If True, omit creating new columns when all values for a given key are null.
    col_renamer : dict or callable, optional
        Mapping or function to rename generated column names.
    recursive : bool, optional
        If True, expand nested dict values recursively.
    uniform_keys : bool, optional
        If True, assume all dicts have the same keys and extract from the first non-null entry.
    default : scalar, optional
        Value to use when a key is missing in a particular row.

    Returns
    -------
    pd.DataFrame
        A new DataFrame with each specified dict-column expanded into its own column(s).

    Raises
    ------
    TypeError
        If a non-dict-like value is encountered when expanding.

    Examples
    --------
    >>> df = pd.DataFrame({
    ...     'metadata': [
    ...         {'id': 1, 'score': 9},
    ...         {'id': 2, 'score': 7, 'extra': 5},
    ...         None
    ...     ]
    ... })
    >>> expand_dict_to_cols(df, 'metadata')
       metadata_id  metadata_score  metadata_extra
    0            1             9.0             NaN
    1            2             7.0             5.0
    2          NaN             NaN             NaN
    """

    def has_vals(meta: Optional[dict]) -> bool:
        try:
            return notna(meta) and len(meta) > 0
        except TypeError:
            raise TypeError(f"Expected a dictionary-like object, got {type(meta)} instead.")

    def get_field(key):
        def getter(meta: Optional[dict]):
            if notna(meta):
                return meta.get(key, default)
            else:
                return default

        return getter

    def get_new_col_name(col):
        if callable(col_renamer):
            return col_renamer(col)
        elif isinstance(col_renamer, dict) and col in col_renamer:
            if callable(col_renamer[col]):
                return col_renamer[col](col)
            else:
                return col_renamer[col]
        else:
            return col

    def add_new_cols(df: pd.DataFrame, values: pd.Series, field: str, prefix: str) -> pd.DataFrame:
        new_df = df.copy()
        if values.isna().all():
            if not dropna:
                new_col = get_new_col_name(prefix + str(field))
                new_df[new_col] = default
        elif isinstance(values[values.notna()].iloc[0], dict) and recursive:
            new_cols = expand_dict_to_cols(
                pd.DataFrame(index=values.index, data={field: values}),
                field,
                fields=None,
                prefix=f"{prefix}{field}{sep}",
                with_col_prefix=with_col_prefix,
                col_renamer=col_renamer,
                recursive=True,
                uniform_keys=uniform_keys,
                default=default,
            )
            for col in new_cols:
                vals = new_cols[col]
                _notna = vals.notna()
                new_df.loc[_notna, col] = vals[_notna]
        else:
            new_col = get_new_col_name(prefix + str(field))
            _notna = values.notna()
            new_df.loc[_notna, new_col] = values[_notna]
        return new_df

    if isinstance(fields, str):
        fields = [fields]
    if isinstance(cols, str):
        cols = [cols]

    if drop:
        new_df = df.drop(columns=[col for col in cols if col in df])
    else:
        new_df = df.copy()

    new_col_map = {}
    for col in cols:
        current_cols = list(new_df.columns)
        if col in df and df[col].map(has_vals).any():
            if isinstance(df.iloc[0][col], str):
                df[col] = df[col].map(lambda v: json.loads(v) if v else None)
            if fields is None:  # expand all
                if uniform_keys:  # same keys in each item, allowing for increased efficiency
                    first_one = df[df[col].map(has_vals)][col].iloc[0]
                    current_fields = list(first_one.keys())
                else:
                    current_fields = OrderedSet(df[col].dropna().map(lambda d: OrderedSet(d.keys())).sum())
            else:
                current_fields = fields
            for field in current_fields:
                values = df[col].map(get_field(field))
                if with_col_prefix:
                    col_prefix = prefix or f"{col}{sep}"
                else:
                    col_prefix = prefix
                if prefix_fun:
                    col_prefix = prefix_fun(col, col_prefix)
                new_df = add_new_cols(new_df, values, field, col_prefix)
        new_col_map[col] = [col for col in new_df.columns if col not in current_cols]

    # Reorder columns so that expansions in place of original column
    col_order = []
    for col in df.columns:
        if col in cols:
            if not drop:
                col_order.append(col)
            col_order.extend(new_col_map[col])
        else:
            col_order.append(col)

    return pd.DataFrame(new_df[col_order])
