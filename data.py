import pandas as pd
import numpy as np
import gdown

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


def _get_returns(data, assets, weights, from_date, to_date):
    data.index = pd.to_datetime(data.index)
    portfolio = (data[assets] * weights).sum(axis=1)
    from_mask = portfolio.index >= pd.to_datetime(from_date)
    to_mask = portfolio.index <= pd.to_datetime(to_date)
    return (portfolio / portfolio.shift() - 1)[from_mask & to_mask]


def stocks_returns(assets, weights, from_date, to_date):
    url = 'https://drive.google.com/file/d/1lLQV4oc30mo1_m39p4JXlpd1gV6pLw6A/view?usp=sharing'
    gdown.download(url, 'stocks.csv', fuzzy=True)
    data = pd.read_csv('stocks.csv', index_col=0)
    return _get_returns(data, assets, weights, from_date, to_date)


def commodities_returns(assets, weights, from_date, to_date):
    url = 'https://drive.google.com/file/d/1GFq1jcV00BjFEa7hmZSO1xD7K4j4gv3O/view?usp=sharing'
    gdown.download(url, 'commodities.csv', fuzzy=True)
    data = pd.read_csv('commodities.csv', index_col=0)
    return _get_returns(data, assets, weights, from_date, to_date)


def cryptocurrencies_returns(assets, weights, from_date, to_date):
    url = 'https://drive.google.com/file/d/1mPP5Vb57Jc2mYPeLYZPgAJM8ogjiguSO/view?usp=sharing'
    gdown.download(url, 'cryptocurrencies.csv', fuzzy=True)
    data = pd.read_csv('cryptocurrencies.csv', index_col=0)
    return _get_returns(data, assets, weights, from_date, to_date)
