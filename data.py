import pandas as pd
import numpy as np
import yfinance as yf
from datetime import datetime as dt
from datetime import timedelta

def stocks_returns(assets, weights, from_date, to_date):
    if len(assets) != len(weights):
        raise ValueError("Length of weights does not match number of assets")
    weights = np.array(weights)
    weights /= sum(weights)
    try:
        to_date = dt.strftime(dt.strptime(to_date, '%d/%m/%Y'), '%Y-%m-%d')
        from_date = dt.strftime(dt.strptime(from_date, '%d/%m/%Y'), '%Y-%m-%d')
    except:
        raise ValueError("Dates format do not match format '%d/%m/%Y'")
    portfolio = yf.download(assets, dt.strftime(dt.strptime(from_date,
            '%Y-%m-%d') - timedelta(days=1), '%Y-%m-%d'), dt.strftime(dt.strptime(to_date,
            '%Y-%m-%d') + timedelta(days=1), '%Y-%m-%d'))['Adj Close']
    if len(assets) == 1:
        portfolio = pd.DataFrame(portfolio)
        portfolio['return'] = portfolio['Adj Close'] / portfolio['Adj Close'].shift(1) - 1
    else:
        portfolio['portfolio'] = portfolio.values @ weights 
        # I personally feel that this is wrong way to calculate the portfolio returns. But it is done
        # exactly according to provided google document. I also attach here another (commented) chunk that
        # I belive calculates the portfolio returns right - by weighting returns of each asset, not their price:
        # for asset in assets:
        #     portfolio[asset] = portfolio[asset] / portfolio[asset].shift(1) - 1
        # portfolio['return'] = portfolio.values @ weights
        portfolio['return'] = portfolio['portfolio'] / portfolio['portfolio'].shift(1) - 1
    portfolio.reset_index(inplace=True)
    portfolio['Date'] = pd.to_datetime(portfolio['Date'].dt.strftime('%Y-%m-%d'))
    portfolio = portfolio[(portfolio['Date'] >= from_date) & (portfolio['Date'] <= to_date)]
    portfolio.set_index('Date', drop=True, inplace=True)
    return portfolio['return']

def commodities_returns(assets, weights, from_date, to_date):
    dict = {'BZ=F': 'Brent Oil Futures', 'CL=F': 'Crude Oil WTI Futures', 'NG=F': 'Natural Gas Futures',
     'HO=F': 'Heating Oil Futures',
     'GC=F': 'Gold Futures', 'SI=F': 'Silver Futures', 'HG=F': 'Copper Futures', 'PL=F': 'Platinum Futures',
     'KC=F': 'US Coffee C Futures', 'ZC=F': 'US Corn Futures'}
    assets = [dict[asset] for asset in assets]
    if len(assets) != len(weights):
        raise ValueError("Length of weights does not match number of assets")
    weights = np.array(weights)
    weights /= sum(weights)
    try:
        to_date = dt.strftime(dt.strptime(to_date, '%d/%m/%Y'), '%Y-%m-%d')
        from_date = dt.strftime(dt.strptime(from_date, '%d/%m/%Y'), '%Y-%m-%d')
    except:
        raise ValueError("Dates format do not match format '%d/%m/%Y'")
    portfolio = yf.download(assets, dt.strftime(dt.strptime(from_date,
            '%Y-%m-%d') - timedelta(days=1), '%Y-%m-%d'), dt.strftime(dt.strptime(to_date,
            '%Y-%m-%d') + timedelta(days=1), '%Y-%m-%d'))['Adj Close']
    if len(assets) == 1:
        portfolio = pd.DataFrame(portfolio)
        portfolio['return'] = portfolio['Adj Close'] / portfolio['Adj Close'].shift(1) - 1
    else:
        portfolio['portfolio'] = portfolio.values @ weights
        portfolio['return'] = portfolio['portfolio'] / portfolio['portfolio'].shift(1) - 1
    portfolio.reset_index(inplace=True)
    portfolio['Date'] = pd.to_datetime(portfolio['Date'].dt.strftime('%Y-%m-%d'))
    portfolio = portfolio[(portfolio['Date'] >= from_date) & (portfolio['Date'] <= to_date)]
    portfolio.set_index('Date', drop=True, inplace=True)
    return portfolio['return']

def cryptocurrencies_returns(assets, weights, from_date, to_date):
    dict = {'BTC':'BTC-USD', 'ETH':'ETH-USD', 'USDT':'USDT-USD', 'USDC':'USDC-USD', 'BNB':'BNB-USD',
            'XRP':'XRP-USD', 'BUSD':'BUSD-USD', 'ADA':'ADA-USD', 'SOL':'SOL-USD',
            'DOGE':'DOGE-USD'}
    assets = [dict[asset] for asset in assets]
    if len(assets) != len(weights):
        raise ValueError("Length of weights does not match number of assets")
    weights = np.array(weights)
    weights /= sum(weights)
    try:
        to_date = dt.strftime(dt.strptime(to_date, '%d/%m/%Y'), '%Y-%m-%d')
        from_date = dt.strftime(dt.strptime(from_date, '%d/%m/%Y'), '%Y-%m-%d')
    except:
        raise ValueError("Dates format do not match format '%d/%m/%Y'")
    portfolio = yf.download(assets, dt.strftime(dt.strptime(from_date,
            '%Y-%m-%d') - timedelta(days=1), '%Y-%m-%d'), dt.strftime(dt.strptime(to_date,
            '%Y-%m-%d') + timedelta(days=1), '%Y-%m-%d'))['Adj Close']
    if len(assets) == 1:
        portfolio = pd.DataFrame(portfolio)
        portfolio['return'] = portfolio['Adj Close'] / portfolio['Adj Close'].shift(1) - 1
    else:
        portfolio['portfolio'] = portfolio.values @ weights
        portfolio['return'] = portfolio['portfolio'] / portfolio['portfolio'].shift(1) - 1
    portfolio.reset_index(inplace=True)
    portfolio['Date'] = pd.to_datetime(portfolio['Date'].dt.strftime('%Y-%m-%d'))
    portfolio = portfolio[(portfolio['Date'] >= from_date) & (portfolio['Date'] <= to_date)]
    portfolio.set_index('Date', drop=True, inplace=True)
    return portfolio['return']
