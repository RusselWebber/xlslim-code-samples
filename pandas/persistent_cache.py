import logging
import os
import pandas as pd

LOG = logging.getLogger(__name__)

def read_dataframe_from_pickle_or_url(url: str, path: str) -> pd.DataFrame:
    """Read JSON data from the URL and convert to a pandas dataframe.
    
    The dataframe is cached locally at the supplied path.
    
    Pickle is used to cache the dataframe.
    """
    df = None
    path = os.path.expandvars(path)
    # If the pickle file exists use it
    if os.path.exists(path):    
        LOG.info("Reading data from %s", path)
        df = pd.read_pickle(path)
    # Else fetch the data from the URL
    else:
        LOG.info("Fetching data from %s", url)
        df = pd.read_json(url)
        # Important to pickle the dataframe so the pickle file
        # is available the next time the function runs
        LOG.info("Pickling dataframe to %s", path)
        df.to_pickle(path)        
    return df


if __name__ == "__main__":
    logging.basicConfig(level="INFO")
    url =  "https://jsonplaceholder.typicode.com/todos"
    path = r"%TEMP%\df.pickle" 
    df = read_dataframe_from_pickle_or_url(url, path)
    print(df.head())

