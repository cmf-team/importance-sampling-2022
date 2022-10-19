#!/usr/bin/env python
# coding: utf-8

# In[151]:


import pandas as pd
import numpy as np
from datetime import datetime
from datetime import timedelta
from typing import List


import pandas_datareader as web
import investpy


# In[152]:


def get_data(asset: str, from_date: datetime, to_date: datetime, **kwargs) -> pd.DataFrame:
    dt = web.get_data_yahoo(symbols = asset, 
                            start = pd.to_datetime(datetime.strptime(from_date, '%m/%d/%Y').strftime('%m/%d/%Y'))-timedelta(days=1), 
                            end = pd.to_datetime(datetime.strptime(to_date, '%m/%d/%Y').strftime('%m/%d/%Y'))-timedelta(days=1))
    
    dt = dt[['Close']].dropna()
    return dt


# In[153]:


def weighted_portfolio (assets: list[str], 
                  weights: list[float], 
                  from_date: datetime, 
                  to_date: datetime, 
                  **kwargs) -> pd.DataFrame:

    dfs = [get_data(asset, 
                    from_date, 
                    to_date, **kwargs) for asset in assets]
    portfolio = sum([df*w for df, w in zip(dfs,weights)])
    portfolio['Return'] = (portfolio['Close'] - portfolio['Close'].shift(1))/portfolio['Close'].shift(1)
    portfolio = portfolio[(portfolio.index > from_date)]
    portfolio = portfolio[portfolio.index.dayofweek < 5]
    return portfolio.dropna()
    


# In[154]:


def stocks_returns(assets: list[str], weights: list[float], from_date: str, to_date: str) -> pd.Series:
    
    available_stocks = ['AAPL', 'AMD', 'TSLA', 'AMZN', 'NVDA', 'INTC', 'MU', 'MSFT', 'META', 'GOOGL']
    
    if np.setdiff1d(assets, available_stocks).size >= 1:
        print('Error. Make sure that tickers entered are in the tickers list:')
        print(available_stocks)
        
    if len(assets) != len(weights):
        print('Error. Number of assets is not equal to number of weights')
        
    if sum(weights) != 1:
        print('Error. Sum of weights must be 1')
        
    if datetime.strptime(from_date, '%m/%d/%Y') >= datetime.strptime(to_date, '%m/%d/%Y'):
        print('Error. Start date must be less than end date')
        
    if datetime.strptime(from_date, '%m/%d/%Y') < datetime.strptime('01/02/2020', '%m/%d/%Y'):
        print('Error. Start date must be less than 01/02/2020')
        
    if datetime.strptime(to_date, '%m/%d/%Y') > datetime.strptime('10/01/2022', '%m/%d/%Y'):
        print('Error. End date must be less than 10/01/2022')
        
        return None
    
    else:
        return weighted_portfolio(assets = assets, weights = weights, from_date = from_date, to_date = to_date)[['Return']]


# In[155]:


def cryptocurrencies_returns(assets: list[str], weights: list[float], from_date: str, to_date: str) -> pd.Series:
    
    available_crypto = ['BTC-USD', 'ETH-USD', 'USDT-USD', 'USDC-USD', 'BNB-USD', 'XRP-USD', 
                        'BUSD-USD', 'ADA-USD', 'SOL-USD', 'DOGE-USD']
    
    if np.setdiff1d(assets, available_crypto).size >= 1:
        print('Error. Make sure that tickers entered are in the tickers list:')
        print(available_crypto)
        
    if len(assets) != len(weights):
        print('Error. Number of assets is not equal to number of weights')
        
    if sum(weights) != 1:
        print('Error. Sum of weights must be 1')
        
    if datetime.strptime(from_date, '%m/%d/%Y') >= datetime.strptime(to_date, '%m/%d/%Y'):
        print('Error. Start date must be less than end date')
        
    if datetime.strptime(from_date, '%m/%d/%Y') < datetime.strptime('01/02/2020', '%m/%d/%Y'):
        print('Error. Start date must be less than 01/02/2020')
        
    if datetime.strptime(to_date, '%m/%d/%Y') > datetime.strptime('10/01/2022', '%m/%d/%Y'):
        print('Error. End date must be less than 10/01/2022')
        
        return None
    
    else:
        return weighted_portfolio(assets = assets, weights = weights, from_date = from_date, to_date = to_date)[['Return']]


# In[156]:


def commodities_returns(assets: list[str], weights: list[float], from_date: str, to_date: str) -> pd.Series:
    
    available_commodities = ['BZ=F','CL=F','NG=F','HO=F','GC=F', 'SI=F', 'HG=F', 'PL=F', 'KC=F', 'ZC=F']
    
    if np.setdiff1d(assets, available_commodities).size >= 1:
        print('Error. Make sure that tickers entered are in the tickers list:')
        print(available_tickers)
        
    if len(assets) != len(weights):
        print('Error. Number of assets is not equal to number of weights')
        
    if sum(weights) != 1:
        print('Error. Sum of weights must be 1')
        
    if datetime.strptime(from_date, '%m/%d/%Y') >= datetime.strptime(to_date, '%m/%d/%Y'):
        print('Error. Start date must be less than end date')
        
    if datetime.strptime(from_date, '%m/%d/%Y') < datetime.strptime('01/02/2020', '%m/%d/%Y'):
        print('Error. Start date must be less than 01/02/2020')
        
    if datetime.strptime(to_date, '%m/%d/%Y') > datetime.strptime('10/01/2022', '%m/%d/%Y'):
        print('Error. End date must be less than 10/01/2022')
        return None
    
    else:
        return weighted_portfolio(assets = assets, weights = weights, from_date = from_date, to_date = to_date)[['Return']]


# In[ ]:




