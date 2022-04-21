# example of using yfinance package to source prices and other data for financial instruments
# pip install yfinance to get the package
import yfinance as yf
import pandas as pd


def get_historical_prices(ticker_name: str, period: str) -> pd.DataFrame:

    assert (
        len(ticker_name.split(" ")) == 1
    ), "get_historica_prices works with one ticker only"

    tick = yf.Ticker(ticker_name)

    return tick.history(period)
