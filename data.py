import os
import subprocess
import pandas as pd
import numpy as np


def stocks_returns(assets, weights, from_date, to_date):
    """
    Constructs the returns of stock portfolio
    Args:
    assets - tickers of assets
    weights - weights of portfolio, should sum up to one
    from_date - start date, mm/dd/yyyy
    to_date - end_date, mm/dd/yyyy
    """
    check_data_download()
    data = construct_data('stocks', assets)
    return construct_portfolio(data, assets, weights, from_date, to_date)


def commodities_returns(assets, weights, from_date, to_date):
    """
    Constructs the returns of commodities portfolio
    Args:
    assets - tickers of assets
    weights - weights of portfolio, should sum up to one
    from_date - start date, mm/dd/yyyy
    to_date - end_date, mm/dd/yyyy
    """
    check_data_download()
    data = construct_data('commodities', assets)
    return construct_portfolio(data, assets, weights, from_date, to_date)


def cryptocurrencies_returns(assets, weights, from_date, to_date):
    """
    Constructs the returns of crypto portfolio
    Args:
    assets - tickers of assets
    weights - weights of portfolio, should sum up to one
    from_date - start date, mm/dd/yyyy
    to_date - end_date, mm/dd/yyyy
    """
    check_data_download()
    data = construct_data('crypto', assets, from_date, to_date)
    return construct_portfolio(data, assets, weights, from_date, to_date)


def check_data_download():
    """
    Checks whether data has been downloaded locally
    """
    if 'data' not in os.listdir():
        subprocess.run(['wget', 'https://www.dropbox.com/s/vq15wiopso1wm76/data_sampling.zip?dl=0', '-O', 'data.zip', '-q'])
        subprocess.run(['unzip', '-q', 'data.zip'])
        subprocess.run(['rm', 'data.zip'])
        subprocess.run(['rm', '-r', '__MACOSX'])


def construct_data(folder, assets):
    """
    Constructs pd.DataFrame of selected assets from a folder
    Args:
    assets - list of assets
    folder - options: stocks, commodities, crypto
    from_date - start date
    to_date - end date
    """
    data = pd.DataFrame()
    for asset in assets:
        path = os.path.join('data',folder,asset + '.csv')
        # Read data and set datetime index
        series = pd.read_csv(path)
        series['Date'] = pd.to_datetime(series['Date'])
        series = series.set_index('Date')
        data[asset] = series['Price']

    # Reverse data so upper row is latest value
    return data[::-1]


def construct_portfolio(data, assets, weights, from_date, to_date):
    """
    Constructs portfolio of returns from data
    Args:
    data - data constructed in construct_data
    assets - list of assets
    weights - weights of portfolio, should sum up to one
    """
    assert abs(sum(weights) - 1) < .001, 'Weights of portfolio are incorrect!'

    weights_ =  {asset : weight for asset, weight in zip(assets, weights)}

    # Construct portfolio
    portfolio = sum([weights_[asset] * data[asset] for asset in assets])
    portfolio = portfolio.pct_change().fillna(0)
    # Slice data according to dates
    portfolio = portfolio[(portfolio.index >= from_date) & (portfolio.index <= to_date)]

    return portfolio
