import pandas as pd
import numpy as np
import yfinance as yf
from datetime import datetime
from datetime import timedelta
from pandas_datareader import data as pdr


class Dataloader:
    def __init__(
            self,
            series: pd.Series,
            window_size: int,
            step_size: int,
            horizon: int,
            first_pred: int
    ):
        self.series = series
        self.window_size = window_size
        self.step_size = step_size
        self.horizon = horizon
        self.first_pred = first_pred
        assert self.first_pred > self.window_size
        feat_idx = []
        target_idx = []
        for i in range(self.first_pred, self.series.shape[0], self.step_size):
            feat_idx.append(range(i - self.horizon - self.window_size, i - self.horizon))
            target_idx.append(i)
        self.feat_idx = feat_idx
        self.target_idx = target_idx

    def __len__(self):
        return len(self.feat_idx)

    def __iter__(self):
        self.iter = 0
        return self

    def __next__(self):
        if self.iter < len(self.feat_idx):
            feat = self.series.iloc[self.feat_idx[self.iter]]
            target = self.series.iloc[self.target_idx[self.iter]]
            self.iter += 1
            return feat, target
        else:
            raise StopIteration
            

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
