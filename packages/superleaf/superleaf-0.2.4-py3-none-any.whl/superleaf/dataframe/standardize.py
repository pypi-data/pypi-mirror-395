import warnings
from typing import Iterable

import pandas as pd


def _is_iter(obj):
    try:
        iter(obj)
        return True
    except TypeError:
        return False


def standardize_columns(
        df: pd.DataFrame,
        to_datetime: bool | str | Iterable[str] | None = False,
        force_datetime: bool | None = None,
        quiet=False,
) -> pd.DataFrame:
    """Standardize DataFrame column names and optionally convert columns to datetime.

    This function returns a copy of the input DataFrame with column names stripped of
    leading/trailing whitespace, lowercased, and spaces replaced by underscores. Optionally,
    specified columns (or auto-detected date/time columns) are converted to pandas datetime.

    Parameters
    ----------
    df : pd.DataFrame
        The input DataFrame whose column names will be standardized.
    to_datetime : bool, str, Iterable[str], or None, optional
        If False (default), no datetime conversion is attempted.
        If True, attempts to convert columns named 'date', 'datetime', 'time', or 'timestamp'.
        If a string or non-iterable, converts the specified column name.
        If an iterable of strings, converts the listed column names.
    force_datetime : bool or None, optional
        If True, forces conversion to datetime and raises on errors.
        If False, quietly coerces invalid parsing to NaT and may emit warnings.
        If None (default), set to True when converting specific columns (str or iterable),
        otherwise False.
    quiet : bool, default False
        If False, prints a message when a column cannot be converted to datetime under
        non-forced mode.

    Returns
    -------
    pd.DataFrame
        A new DataFrame with standardized column names and datetime-converted columns.

    Examples
    --------
    >>> df = pd.DataFrame({
    ...     ' Date ': ['2021-01-01', '2021-02-01'],
    ...     'Value': [10, 20]
    ... })
    >>> standardize_columns(df, to_datetime=True)
      date  value
    0 2021-01-01     10
    1 2021-02-01     20
    """

    df = df.copy()
    df.columns = [col.strip().lower().replace(' ', '_') for col in df.columns]

    if to_datetime is None:
        dt_cols = []
    elif isinstance(to_datetime, bool):
        dt_cols = [col for col in df.columns if col in {'date', 'datetime', 'time', 'timestamp'}]
    elif isinstance(to_datetime, str) or not _is_iter(to_datetime):
        dt_cols = [to_datetime]
        if force_datetime is None:
            force_datetime = True
    else:
        dt_cols = to_datetime
        if force_datetime is None:
            force_datetime = True

    for col in dt_cols:
        if col in df.columns:
            if not force_datetime:
                with warnings.catch_warnings():
                    warnings.simplefilter('error')
                    try:
                        df[col] = pd.to_datetime(df[col], errors='coerce')
                    except UserWarning:
                        if not quiet:
                            print(f"Could not convert column '{col}' to datetime")
            else:
                df[col] = pd.to_datetime(df[col])

    return df
