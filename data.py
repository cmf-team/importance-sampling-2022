import pandas as pd
import numpy as np
import gdown
import datetime

def stocks_returns(assets, weights, from_date, to_date):
    url = 'https://drive.google.com/file/d/1lLQV4oc30mo1_m39p4JXlpd1gV6pLw6A/view?usp=sharing'
    gdown.download(url, 'stocks.csv', fuzzy=True)
    stocks = pd.read_csv('stocks.csv', index_col=0)
    stocks.index = pd.to_datetime(stocks.index)
    start_time=datetime.datetime.strptime(from_date, '%m/%d/%Y') - datetime.timedelta(days=1)
    end_time=datetime.datetime.strptime(to_date, '%m/%d/%Y')
    
    return calc_returns(stocks, assets, weights, start_time, end_time)

def commodities_returns(assets, weights, from_date, to_date):
    url = 'https://drive.google.com/file/d/1GFq1jcV00BjFEa7hmZSO1xD7K4j4gv3O/view?usp=sharing'
    gdown.download(url, 'commodities.csv', fuzzy=True)
    commodities = pd.read_csv('commodities.csv', index_col=0)
    commodities.index = pd.to_datetime(commodities.index)
    start_time=datetime.datetime.strptime(from_date, '%m/%d/%Y') - datetime.timedelta(days=1)
    end_time=datetime.datetime.strptime(to_date, '%m/%d/%Y')
    
    return calc_returns(commodities, assets, weights, start_time, end_time)

def cryptocurrencies_returns(assets, weights, from_date, to_date):
    url = 'https://drive.google.com/file/d/1mPP5Vb57Jc2mYPeLYZPgAJM8ogjiguSO/view?usp=sharing'
    gdown.download(url, 'cryptocurrencies.csv', fuzzy=True)
    cryptocurrencies = pd.read_csv('cryptocurrencies.csv', index_col=0)
    cryptocurrencies.index = pd.to_datetime(cryptocurrencies.index)
    start_time=datetime.datetime.strptime(from_date, '%m/%d/%Y') - datetime.timedelta(days=1)
    end_time=datetime.datetime.strptime(to_date, '%m/%d/%Y')
    
    return calc_returns(cryptocurrencies, assets, weights, start_time, end_time)

def calc_returns(data, assets, weights, start_time, end_time):
    
    df=data.loc[start_time:end_time, assets]
    for i in range(df.shape[1]):
        df.iloc[:, i] *= weights[i] 
    
    df['total'] = df.sum(axis=1)
    df['returns'] = (df['total'] - df['total'].shift(1))/df['total'].shift(1)
    df.dropna(axis='rows', inplace=True)
    
    return df['returns']    
