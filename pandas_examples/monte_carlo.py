# xlslim examples of Monte Carlo Simulations

import pandas as pd
from numpy import random, exp, sqrt, mean

def monte_carlo_stock_price(s0:float, r:float, sigma:float, mat:float, strike:float=0.0, N=10000)->pd.DataFrame:
    """
        s0:     current stock price
        r:      interest rate for discounting
        sigma:  stock volatility
        mat:    option maturity
        strike: optional strike to calculate call option payout
        N:      optional number of simulations
    """
    assert mat>0, "Maturity should be positive"
    
    random.seed = 11
    z = random.standard_normal(size=N)
    df_stock = pd.DataFrame(data = {'sim_stock': s0*exp((r-0.5*sigma*sigma)*mat + sigma*sqrt(mat)*z)})
    
    
    if strike !=0.0:
        df_stock['payout'] = df_stock.apply(lambda x: exp(-r*mat)*max((x.sim_stock-strike), 0.0), axis=1)
        
    return df_stock
        
    
def average_payout(df: pd.DataFrame)->float:
    
    assert 'payout' in df.columns, "Passed Dataframe should have payout column"
    
    return mean(df['payout']) 
    