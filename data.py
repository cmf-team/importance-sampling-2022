import pandas as pd
import numpy as np
import gdown
from datetime import datetime, timedelta

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

def prev_date(date):
    to_date_tmp = datetime.strptime(date, '%m/%d/%Y')
    to_date_tmp = to_date_tmp + timedelta(days=-1)
    date = to_date_tmp.strftime('%m/%d/%Y')
    return date


def get_portfolio(prices, assets, weights, from_date_new, to_date):
    prices.index = pd.to_datetime(prices.index)
    prices_assets = prices.loc[from_date_new:to_date, assets]
    i = 0
    for column in prices_assets:
        prices_assets.loc[:, column] = prices_assets[column] * weights[i]
        i += 1
    prices_assets['price'] = prices_assets.loc[:, :].sum(axis=1)
    return prices_assets


def get_returns(portfolio, from_date_new):
    returns = []
    for i in range(1, len(portfolio)):
        day_return = (portfolio['price'][i] - portfolio['price'][i - 1]) / portfolio['price'][i - 1]
        returns.append(day_return)
    portfolio = portfolio.drop(index=[from_date_new])
    portfolio['return'] = returns
    return portfolio['return']


def stocks_returns(assets, weights, from_date, to_date):
    url = 'https://drive.google.com/file/d/1GnXJN5m3UvBoSnlS-MH3HEQvNnNDlIkl/view?usp=sharing'
    gdown.download(url, 'stock_prices.csv', fuzzy=True)
    stock_prices = pd.read_csv('stock_prices.csv', index_col='Date')
    from_date_new = prev_date(from_date)
    portfolio = get_portfolio(stock_prices, assets, weights, from_date_new, to_date)
    stocks_returns = get_returns(portfolio, from_date_new)
    return stocks_returns


def commodities_returns(assets, weights, from_date, to_date):
    url = 'https://drive.google.com/file/d/1LBKJyk95z46gB9nl4_0sYS3b4bYMmIQ4/view?usp=sharing'
    gdown.download(url, 'commodities_prices.csv', fuzzy=True)
    commodities_prices = pd.read_csv('commodities_prices.csv', index_col='Date')
    from_date_new = prev_date(from_date)
    portfolio = get_portfolio(commodities_prices, assets, weights, from_date_new, to_date)
    commodities_returns = get_returns(portfolio, from_date_new)
    return commodities_returns


def cryptocurrencies_returns(assets, weights, from_date, to_date):
    url = 'https://drive.google.com/file/d/1NLvOCVyvUkVwYBeLL7DjRKlWzQvHh46z/view?usp=sharing'
    gdown.download(url, 'crypto_prices.csv', fuzzy=True)
    crypto_prices = pd.read_csv('crypto_prices.csv', index_col='Date')
    from_date_new = prev_date(from_date)
    portfolio = get_portfolio(crypto_prices, assets, weights, from_date_new, to_date)
    cryptocurrencies_returns = get_returns(portfolio, from_date_new)
    return cryptocurrencies_returns


