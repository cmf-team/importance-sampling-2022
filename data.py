import pandas as pd
import numpy as np
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
            
            
import gdown as gd

def _inc(data, assets, weights, from_date, to_date):
    data.index = pd.to_datetime(data.index)
    portfolio = (data[assets] * weights).sum(axis=1)
    from_mask = portfolio.index >= pd.to_datetime(from_date)
    to_mask = _portfolio.index <= pd.to_datetime(to_date)
    return (portfolio / portfolio.shift() - 1)[from_mask & to_mask]

def stocks_returns(assets, weights, from_date, to_date):
    gd.download('https://drive.google.com/file/d/1c0TBGNWis5fT6CT1HFEpJ4s7kPWLI4s1/view?usp=sharing', 'stocks.csv', fuzzy=True)
    data = pd.read_csv('shares.csv', index_col=0)
    return _inc(data, assets, weights, from_date, to_date)


def commodities_returns(assets, weights, from_date, to_date):
    gd.download('https://drive.google.com/file/d/10vxYliiGjhhwsYMV1diR2IV5jnJLaIiJ/view?usp=sharing', 'commodities.csv', fuzzy=True)
    data = pd.read_csv('commodities.csv', index_col=0)
    return _inc(data, assets, weights, from_date, to_date)


def cryptocurrencies_returns(assets, weights, from_date, to_date):
    gd.download('https://drive.google.com/file/d/1kjY92ZsMQcu_j4ylazwc9zxFKGGacawJ/view?usp=share_link', '_crypto.csv', fuzzy=True)
    data = pd.read_csv('_crypto.csv', index_col=0)
    return _inc(data, assets, weights, from_date, to_date)