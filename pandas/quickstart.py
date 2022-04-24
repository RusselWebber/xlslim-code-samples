import pandas as pd
import numpy as np
from typing import List, Optional

XLSLIM_INWINDOWFUNC = None


def describe_df(x: pd.DataFrame) -> pd.DataFrame:
    """Describe this dataframe."""
    return x.describe()


def create_random_df(
    minimum: Optional[int] = 0,
    maximum: Optional[int] = 100,
    rows: Optional[int] = 1,
    columns: Optional[int] = 1,
) -> pd.DataFrame:
    """Create a dataframe of random integers."""
    return pd.DataFrame(
        np.random.randint(minimum, maximum, size=(rows, columns)),
        columns=[f"Col{i}" for i in range(columns)],
    )


def create_random_ds(rows: Optional[int] = 1) -> pd.Series:
    """Create a series of random integers"""
    return pd.Series(np.random.randint(0, rows, size=(rows,)), list(range(rows)))


def describe_ds(x: pd.Series) -> pd.Series:
    """Describe this series."""
    return x.describe()


def concat_two_ds(
    ds_a: pd.Series,
    ds_b: pd.Series,
    axis: Optional[int] = 0,
    join: Optional[str] = "outer",
    ignore_index: Optional[bool] = False,
) -> pd.Series:
    """Concatenate the two supplied series."""
    return concat_df([ds_a, ds_b], axis, join, ignore_index)


def concat_ds(
    series: List[pd.Series],
    axis: Optional[int] = 0,
    join: Optional[str] = "outer",
    ignore_index: Optional[bool] = False,
) -> pd.Series:
    """Concatenate the supplied series."""
    # Note how this global function can be used to skip
    # running slow code in the Excel function wizard
    if XLSLIM_INWINDOWFUNC and XLSLIM_INWINDOWFUNC():
        return pd.Series()
    return pd.concat(series, axis=axis, join=join, ignore_index=ignore_index)


def concat_two_df(
    df_a: pd.DataFrame,
    df_b: pd.DataFrame,
    axis: Optional[int] = 0,
    join: Optional[str] = "outer",
    ignore_index: Optional[bool] = False,
) -> pd.DataFrame:
    """Concatenate the two supplied dataframes."""
    return concat_df([df_a, df_b], axis, join, ignore_index)


def concat_df(
    dframes: List[pd.DataFrame],
    axis: Optional[int] = 0,
    join: Optional[str] = "outer",
    ignore_index: Optional[bool] = False,
) -> pd.DataFrame:
    """Concatenate the supplied dataframes."""
    # Note how this global function can be used to skip
    # running slow code in the Excel function wizard
    if XLSLIM_INWINDOWFUNC and XLSLIM_INWINDOWFUNC():
        return pd.DataFrame()
    return pd.concat(dframes, axis=axis, join=join, ignore_index=ignore_index)


if __name__ == "__main__":
    a = create_random_df(1, 100, 10, 2)
    b = create_random_ds(100)
    print(describe_df(a))
    print(describe_ds(b))
