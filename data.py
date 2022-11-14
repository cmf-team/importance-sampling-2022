import pandas as pd
import numpy as np

from utils import *


class Dataloader:
    def __init__(
        self,
        series: pd.Series,
        window_size: int,
        step_size: int,
        horizon: int,
        first_pred: int,
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
            feat_idx.append(
                range(i - self.horizon - self.window_size, i - self.horizon)
            )
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


def download_and_count(
    assets: list, weights: list, from_date: str, to_date: str
) -> pd.Series:
    from_date = pd.Timestamp(from_date)
    from_date = from_date - pd.Timedelta(days=1)

    download_info()
    df = get_full_data(assets)

    df["date"] = pd.to_datetime(df["date"])
    df = df[(df["date"] >= from_date) & (df["date"] <= to_date)]
    df = df.set_index("date")

    dict_mul = {col: mul for col, mul in zip(assets, weights)}
    df = df.multiply(dict_mul)

    df["price"] = df.sum(axis=1)
    df["return"] = df["price"].diff() / df["price"].shift()
    df = df[1:]
    df["return"] = df["return"].astype("float64")

    df = df["return"].squeeze()

    return df


def stocks_returns(
    assets: list, weights: list, from_date: str = None, to_date: str = None
) -> pd.Series:

    return_ = download_and_count(assets, weights, from_date, to_date)
    return return_


def commodities_returns(
    assets: list, weights: list, from_date: str = None, to_date: str = None
) -> pd.Series:

    return_ = download_and_count(assets, weights, from_date, to_date)
    return return_


def cryptocurrencies_returns(
    assets: list, weights: list, from_date: str = None, to_date: str = None
) -> pd.Series:

    return_ = download_and_count(assets, weights, from_date, to_date)
    return return_
