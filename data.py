import pandas as pd
import numpy as np
import gdown

def stocks_returns(assets, weights, from_date, to_date):
    url = 'https://drive.google.com/file/d/10HtNCH9L2G6irBpWjOIKRGA7zFFAH6Gd/view?usp=sharing'
    gdown.download(url, 'stock_prices.csv', fuzzy=True)
    stock_prices = pd.read_csv('stock_prices.csv', index_col='date')
    portfolio = (stock_prices[assets]*weights).sum(axis=1)
    portfolio.index = pd.to_datetime(portfolio.index)
    portfolio=portfolio[(portfolio.index >= (portfolio[portfolio.index < pd.to_datetime(from_date)].index[-1]))&(portfolio.index <= pd.to_datetime(to_date))]
    returns=[]
    for i in range(len(portfolio)):
        if i == len(portfolio)-1:
            break
        returns.append((portfolio[i+1]-portfolio[i])/portfolio[i])
    returns = pd.Series(data=returns, index=portfolio.index[1:])
    return returns

def commodities_returns(assets, weights, from_date, to_date):
    url = 'https://drive.google.com/file/d/1baSJfugJD20Dzn4fNWmefhHd2JFlFv72/view?usp=sharing'
    gdown.download(url, 'commodities.csv', fuzzy=True)
    stock_prices = pd.read_csv('stock_prices.csv', index_col='date')
    portfolio = (stock_prices[assets]*weights).sum(axis=1)
    portfolio.index = pd.to_datetime(portfolio.index)
    portfolio=portfolio[(portfolio.index >= (portfolio[portfolio.index < pd.to_datetime(from_date)].index[-1]))&(portfolio.index <= pd.to_datetime(to_date))]
    returns=[]
    for i in range(len(portfolio)):
        if i == len(portfolio)-1:
            break
        returns.append((portfolio[i+1]-portfolio[i])/portfolio[i])
    returns = pd.Series(data=returns, index=portfolio.index[1:])
    return returns

def cryptocurrencies_returns(assets, weights, from_date, to_date):
    url = 'https://drive.google.com/file/d/1u-zrk2syTIcn6D5sk8q-sjxtRpzK2S5o/view?usp=sharing'
    gdown.download(url, 'crypto.csv', fuzzy=True)
    stock_prices = pd.read_csv('crypto.csv', index_col='date')
    portfolio = (stock_prices[assets]*weights).sum(axis=1)
    portfolio.index = pd.to_datetime(portfolio.index)
    portfolio=portfolio[(portfolio.index >= (portfolio[portfolio.index < pd.to_datetime(from_date)].index[-1]))&(portfolio.index <= pd.to_datetime(to_date))]
    returns=[]
    for i in range(len(portfolio)):
        if i == len(portfolio)-1:
            break
        returns.append((portfolio[i+1]-portfolio[i])/portfolio[i])
    returns = pd.Series(data=returns, index=portfolio.index[1:])
    return returns
