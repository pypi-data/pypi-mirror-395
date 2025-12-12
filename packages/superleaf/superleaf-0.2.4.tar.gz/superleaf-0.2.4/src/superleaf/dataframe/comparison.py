import pandas as pd


def nan_eq(df1: pd.DataFrame, df2: pd.DataFrame, pass_either_nan=False) -> bool:
    """Check if two dataframes are equal, treating NaNs as equal."""
    if df1.shape != df2.shape:
        return False
    if pass_either_nan:
        return bool(((df1 == df2) | df1.isna() | df2.isna()).all().all())
    else:
        return bool(((df1 == df2) | (df1.isna() & df2.isna())).all().all())
