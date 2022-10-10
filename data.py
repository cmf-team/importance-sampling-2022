from datetime import datetime, timedelta
import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import requests
import json

stock_tickers = ['AAPL','AMD','TSLA','AMZN','NVDA','INTC','MU','MSFT','META','GOOGL']
comm_tickers = ['BZ=F', 'CL=F', 'NG=F', 'HO=F', 'GC=F', 'SI=F', 'HG=F', 'KC=F','ZC=F']
crypto_tickers = ['BTC','ETH','USDT','BNB','XRP','SOL','DOGE']

def stocks_returns(assets, weights, from_date, to_date):
    from_date_1 = from_date
    to_date_1 = to_date
    from_date = datetime(int(from_date_1[-4:]),int(from_date_1[:2]),int(from_date_1[3:5]))
    to_date = datetime(int(to_date_1[-4:]),int(to_date_1[:2]),int(to_date_1[3:5]))
    delta = (to_date - from_date).days
    ind_date = []
    for i in range(delta+1):
        ind_date.append(from_date+timedelta(days = i))
    returns = pd.DataFrame(np.ones((delta+1,len(assets))), index = range(len(ind_date)), columns = assets)
    returns['return'] = np.ones(len(returns))
    ret = np.zeros(len(ind_date)-1)
    data = {}
    for i in range(len(assets)):
        data[str(assets[i])] = yf.download(str(assets[i]), start = from_date, end = to_date+timedelta(days=1))
        data[str(assets[i])]['return'] = np.ones(len(data[str(assets[i])]))
        for j in range(1, len(data[str(assets[i])])):#здесь было без +1
            data[str(assets[i])].loc[data[str(assets[i])].index[j], 'delta'] = (data[str(assets[i])].loc[data[str(assets[i])].index[j], 'Close'] - data[str(assets[i])].loc[data[str(assets[i])].index[j-1], 'Close'])
    final_returns = np.ones((len(data[str(assets[0])]), len(assets)))
    portfolio_0 = np.zeros(len(ind_date))
    portfolio_1 = np.zeros(len(ind_date))
    for j in range(1,len(data[str(assets[i])].index)):
        for i in range(len(assets)):
            portfolio_0[j] +=  weights[i]*data[str(assets[i])]['Close'][j-1]
            portfolio_1[j] = portfolio_1[j] + weights[i]*data[str(assets[i])]['delta'][j]
    final = []
    for j in range(1,len(data[str(assets[i])].index)):
        final.append(portfolio_1[j]/portfolio_0[j])
    final = pd.Series(data=final, index=data[str(assets[i])].index[1:])
    return final

        

def commodities_returns(assets, weights, from_date, to_date):
    from_date_1 = from_date
    to_date_1 = to_date
    from_date = datetime(int(from_date_1[-4:]),int(from_date_1[:2]),int(from_date_1[3:5]))
    to_date = datetime(int(to_date_1[-4:]),int(to_date_1[:2]),int(to_date_1[3:5]))
    delta = (to_date - from_date).days
    ind_date = []
    for i in range(delta+1):
        ind_date.append(from_date+timedelta(days = i))
    returns = pd.DataFrame(np.ones((delta+1,len(assets))), index = range(len(ind_date)), columns = assets)
    returns['return'] = np.ones(len(returns))
    ret = np.zeros(len(ind_date)-1)
    data = {}
    for i in range(len(assets)):
        data[str(assets[i])] = yf.download(str(assets[i]), start = from_date, end = to_date+timedelta(days=1))
        data[str(assets[i])]['return'] = np.ones(len(data[str(assets[i])]))
        for j in range(1, len(data[str(assets[i])])):#здесь было без +1
            data[str(assets[i])].loc[data[str(assets[i])].index[j], 'delta'] = (data[str(assets[i])].loc[data[str(assets[i])].index[j], 'Close'] - data[str(assets[i])].loc[data[str(assets[i])].index[j-1], 'Close'])
    final_returns = np.ones((len(data[str(assets[0])]), len(assets)))
    portfolio_0 = np.zeros(len(ind_date))
    portfolio_1 = np.zeros(len(ind_date))
    for j in range(1,len(data[str(assets[i])].index)):
        for i in range(len(assets)):
            portfolio_0[j] +=  weights[i]*data[str(assets[i])]['Close'][j-1]
            portfolio_1[j] = portfolio_1[j] + weights[i]*data[str(assets[i])]['delta'][j]
    final = []
    for j in range(1,len(data[str(assets[i])].index)):
        final.append(portfolio_1[j]/portfolio_0[j])
    final = pd.Series(data=final, index=data[str(assets[i])].index[1:])
    return final

def ftx_download(category: str):
        ftx_endpoint = 'https://ftx.com/api/'
        cat_list = requests.get(ftx_endpoint + category).json()['result']
        cat_df = pd.DataFrame(cat_list)
        return cat_df

def cryptocurrencies_returns(assets, weights, from_date, to_date):
    from_date_1 = from_date
    to_date_1 = to_date
    from_date = datetime(int(from_date_1[-4:]),int(from_date_1[:2]),int(from_date_1[3:5]))
    to_date = datetime(int(to_date_1[-4:]),int(to_date_1[:2]),int(to_date_1[3:5]))
    delta = (to_date - from_date).days
    ind_date = []
    for i in range(delta+1):
        ind_date.append(from_date+timedelta(days = i))
    returns = pd.DataFrame(np.ones((delta+1,len(assets))), index = range(len(ind_date)), columns = assets)
    returns['return'] = np.ones(len(returns))
    ret = np.zeros(len(ind_date)-1)
    data = {}
    for i in range(len(assets)):
        ftx_endpoint = 'https://ftx.com/api/'
        markets = ftx_download('markets')
        market_name = str(assets[i])+'/USD'#'ETH/USD'
        t_start = (pd.to_datetime(from_date)- pd.Timestamp("1970-01-01"))// pd.Timedelta('1s')
        t_end = (pd.to_datetime(to_date)- pd.Timestamp("1970-01-01"))// pd.Timedelta('1s')
        res = 86400
        hist_path = ftx_endpoint + f'markets/{market_name}/candles?resolution={res}&start_time={t_start}&end_time={t_end}'
        hist = requests.get(hist_path).json()
        data[str(assets[i])] = pd.DataFrame(hist['result'])
        data[str(assets[i])]['return'] = np.ones(len(data[str(assets[i])]))
        for j in range(1, len(data[str(assets[i])])):#здесь было без +1
            data[str(assets[i])].loc[data[str(assets[i])].index[j], 'delta'] = (data[str(assets[i])].loc[data[str(assets[i])].index[j], 'close'] - data[str(assets[i])].loc[data[str(assets[i])].index[j-1], 'close'])
    final_returns = np.ones((len(data[str(assets[0])]), len(assets)))
    portfolio_0 = np.zeros(len(ind_date))
    portfolio_1 = np.zeros(len(ind_date))
    for j in range(1,len(data[str(assets[i])].index)):
        for i in range(len(assets)):
            portfolio_0[j] +=  weights[i]*data[str(assets[i])]['close'][j-1]
            portfolio_1[j] = portfolio_1[j] + weights[i]*data[str(assets[i])]['delta'][j]
    final = []
    for j in range(1,len(data[str(assets[i])].index)):
        final.append(portfolio_1[j]/portfolio_0[j])
    final = pd.Series(data=final, index=data[str(assets[i])].index[1:])
    return final

def test_stocks_returns():
    assets = ['AAPL']
    weights = [1.]
    returns = stocks_returns(assets, weights, from_date='09/02/2022', to_date='09/07/2022')
    test_returns = pd.Series(
        data=[-0.0136, -0.0082, 0.0093], 
        index=pd.to_datetime(['09/02/2022', '09/06/2022', '09/07/2022']),
    )
    assert np.allclose(returns, test_returns, atol=0.0001)
    
    assets = ['AAPL', 'GOOGL']
    weights = [0.3, 0.7]
    returns = stocks_returns(assets, weights, from_date='09/02/2022', to_date='09/07/2022')
    test_returns = pd.Series(
        data=[-0.0158, -0.0091, 0.0188], 
        index=pd.to_datetime(['09/02/2022', '09/06/2022', '09/07/2022']),
    )
    assert np.allclose(returns, test_returns, atol=0.0001)

    
#test_stocks_returns()
