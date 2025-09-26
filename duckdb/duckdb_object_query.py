import pandas as pd

def read_csv(filepath: str) -> pd.DataFrame:
    """Read a csv and return the dataframe."""
    return pd.read_csv(filepath)
