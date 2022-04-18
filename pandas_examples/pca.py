# example of performing pca on historical prices of indices

from typing import List
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

def pca(prices:List[pd.DataFrame], num_comp:int=-1)->np.ndarray:
    """
    prices: list of pandas dataframes extracted using yfinance historical data prices (assumes prices are for the same dates)
    num_comp: int number of components to keep, if -1 then all components are kept
    """
    
    # extract the data for close of day prices
    # calculate pct change
    assert len(prices)>0, "prices should have at least one dataframe"
    df_close = pd.DataFrame()
    
    for i in range(len(prices)):
        df_close['stock_'+str(i+1)] = prices[0]['Close'].pct_change().fillna(0)
    
    if num_comp==-1:    
        pca = PCA(random_state=11)
    else:
        pca = PCA(n_components=num_comp, random_state=11)
    
    df_close_scaled = StandardScaler().fit_transform(df_close)
    pca.fit(df_close_scaled)
    
    return pca.transform(df_close_scaled)
    
    
    

