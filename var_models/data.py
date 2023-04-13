import pandas as pd
import numpy as np
import gdown

class Dataloader:
    def __init__(
            self,
            series: pd.DataFrame,
            window_size: int,
            step_size: int,
            horizon: int,
            first_pred: int,
            weights=None,
    ):
        self.series = series
        self.window_size = window_size
        self.step_size = step_size
        self.horizon = horizon
        self.first_pred = first_pred
        self.weights = weights
        assert self.first_pred > self.window_size
        if weights is not None:
            self.weights = np.array(weights)
            assert self.weights.sum() == 1
        feat_idx = []
        target_idx = []
        for i in range(self.first_pred, self.series.shape[0], self.step_size):
            feat_idx.append(range(i-self.horizon-self.window_size+1, i-self.horizon+1))
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
            if self.weights is not None:
                feat = feat @ self.weights
                target = target @ self.weights
            self.iter += 1
            return feat, target
        else:
            raise StopIteration

def get_returns(data, assets, from_date, to_date):
    portfolio = data[assets]
    from_mask = portfolio.index >= pd.to_datetime(from_date)
    to_mask = portfolio.index <= pd.to_datetime(to_date)
    return (portfolio / portfolio.shift() - 1)[from_mask & to_mask]

def get_logreturns(data, assets, from_date, to_date):
    returns = get_returns(data, assets, from_date, to_date)
    return np.log(1 + returns)

def stocks_data():
    url = 'https://drive.google.com/file/d/1lLQV4oc30mo1_m39p4JXlpd1gV6pLw6A/view?usp=sharing'
    data = gdown.download(url, 'stocks.csv', fuzzy=True)
    data = pd.read_csv('stocks.csv', index_col=0)
    data.index = pd.to_datetime(data.index)
    return data

def commodities_data():
    url = 'https://drive.google.com/file/d/1GFq1jcV00BjFEa7hmZSO1xD7K4j4gv3O/view?usp=sharing'
    gdown.download(url, 'commodities.csv', fuzzy=True)
    data = pd.read_csv('commodities.csv', index_col=0)
    data.index = pd.to_datetime(data.index)
    return data

def cryptocurrencies_data():
    url = 'https://drive.google.com/file/d/1mPP5Vb57Jc2mYPeLYZPgAJM8ogjiguSO/view?usp=sharing'
    gdown.download(url, 'cryptocurrencies.csv', fuzzy=True)
    data = pd.read_csv('cryptocurrencies.csv', index_col=0)
    data.index = pd.to_datetime(data.index)
    return data
