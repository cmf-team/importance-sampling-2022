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


def stocks_returns(assets, weights, from_date, to_date):
    raise Exception(NotImplementedError)


def commodities_returns(assets, weights, from_date, to_date):
    raise Exception(NotImplementedError)


def cryptocurrencies_returns(assets, weights, from_date, to_date):
    raise Exception(NotImplementedError)
