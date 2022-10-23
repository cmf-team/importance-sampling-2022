import gdown
import pandas as pd
from datetime import datetime, timedelta

def stocks_returns(assets, weights, from_date, to_date):
    url = 'https://drive.google.com/file/d/1wlHowk6HPpwt4DJqAXJL7hODc1Sjf_GG/view?usp=sharing'
    gdown.download(url, 'shares.csv', fuzzy=True)
    prices = pd.read_csv('shares.csv', index_col = 'Date')
    return computing_r(assets, weights, from_date, to_date, prices)
    
def commodities_returns(assets, weights, from_date, to_date):
    url = 'https://drive.google.com/file/d/1m63lYpYlCtbTTyk21fYw_pyuHGL-vS-Q/view?usp=sharing'
    gdown.download(url, 'commodities.csv', fuzzy=True)
    prices = pd.read_csv('commodities.csv', index_col= 'Date')
    return computing_r(assets, weights, from_date, to_date, prices)
    
def cryptocurrencies_returns(assets, weights, from_date, to_date):
    url = 'https://drive.google.com/file/d/1dr4jKLiACtgcWzM4u4ZkNuQz_kwG03Mf/view?usp=sharing'
    gdown.download(url, 'crypto.csv', fuzzy=True)
    prices = pd.read_csv('crypto.csv', index_col= 'Date')
    return computing_r(assets, weights, from_date, to_date, prices)
    
def computing_r(assets, weights, from_date, to_date, prices):
    from_date = datetime.strftime((datetime.strptime(from_date, '%m/%d/%Y') - timedelta(days = 1)), '%Y-%m-%d')
    to_date = datetime.strftime(datetime.strptime(to_date, '%m/%d/%Y'), '%Y-%m-%d')
    prices = prices[from_date: to_date]
    prices = prices[assets]
    answer = []
    i = 0
    for column in prices:
        prices.loc[:, column] = prices[column] * weights[i]
        i += 1
    prices['summ'] = prices.loc[:,:].sum(axis=1)
    for i in range(1, len(prices)):
        day_answer = (prices['summ'][i] - prices['summ'][i-1]) / prices['summ'][i-1]
        answer.append(day_answer)
    prices = prices.drop(index=[from_date])
    prices['return'] = answer
    return prices['return']