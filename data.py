import pandas as pd
import numpy as np
import yfinance as yf
from datetime import datetime
from datetime import timedelta
from pandas_datareader import data as pdr


def get_portfolio(assets, weights, start, end):
    yf.pdr_override()
    data = pdr.get_data_yahoo(assets,
                              start=pd.to_datetime(datetime.strptime(start, '%m/%d/%Y').strftime('%m/%d/%Y')),
                              end=pd.to_datetime(datetime.strptime(end, '%m/%d/%Y').strftime('%m/%d/%Y'))+timedelta(days=1))['Close']
    data.dropna(inplace=True)
    if len(assets) != 1:
        return pd.Series(data=np.dot(data, weights),
                         index=data.index)
    else:
        return pd.Series(data=data * weights,
                         index=data.index)


def stocks_returns(assets, weights, from_date, to_date):
    d = get_portfolio(assets, weights, from_date, to_date)
    return (d / d.shift(1) - 1)[1:]


def commodities_returns(assets, weights, from_date, to_date):
    d = get_portfolio(assets, weights, from_date, to_date)
    return (d / d.shift(1) - 1)[1:]


def cryptocurrencies_returns(assets, weights, from_date, to_date):
    d = get_portfolio(assets, weights, from_date, to_date)
    return (d / d.shift(1) - 1)[1:]
