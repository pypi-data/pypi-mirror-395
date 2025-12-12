import pandas as pd
from IPython.display import display


def set_max_columns(max_columns=None):
    """Set pandas’ display.max_columns option.

    Temporarily controls how many columns pandas will print when formatting DataFrames.

    Parameters
    ----------
    max_columns : int or None
        Maximum number of columns to show. If None, pandas will use its own default (usually 20).
    """
    pd.set_option('display.max_columns', max_columns)


def set_max_rows(max_rows=None):
    """Set pandas’ display.max_rows option.

    Temporarily controls how many rows pandas will print when formatting DataFrames.

    Parameters
    ----------
    max_rows : int or None
        Maximum number of rows to show. If None, pandas will use its own default (usually 60).
    """
    pd.set_option('display.max_rows', max_rows)


class _PandasDisplayCM:
    def __init__(self, all_columns=False, all_rows=False):
        self._value_store = {}
        self.all_columns = all_columns
        self.all_rows = all_rows

    def __enter__(self):
        if self.all_columns:
            self._value_store['max_columns'] = pd.get_option('display.max_columns')
            set_max_columns()
        if self.all_rows:
            self._value_store['max_rows'] = pd.get_option('display.max_rows')
            set_max_rows()

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.all_columns:
            pd.set_option('display.max_columns', self._value_store['max_columns'])
        if self.all_rows:
            pd.set_option('display.max_rows', self._value_store['max_rows'])
        return False


def show_all(df, mode=None, columns=True, rows=True):
    """Display a DataFrame with all rows and/or columns visible.

    Uses a context manager to temporarily override pandas’ display.max_columns
    and display.max_rows options, then calls IPython.display.display.

    Parameters
    ----------
    df : pd.DataFrame
        The DataFrame to render in the notebook.
    mode : str, optional
        One of:
        - 'columns': expand only columns
        - 'rows': expand only rows
        - None (default): use the ``columns`` and ``rows`` flags below
    columns : bool, optional
        When mode is None, if True (default) all columns are shown.
    rows : bool, optional
        When mode is None, if True (default) all rows are shown.
    """
    if mode == 'columns':
        cm = _PandasDisplayCM(all_columns=True)
    elif mode == 'rows':
        cm = _PandasDisplayCM(all_rows=True)
    else:
        cm = _PandasDisplayCM(all_columns=columns, all_rows=rows)
    with cm:
        display(df)
