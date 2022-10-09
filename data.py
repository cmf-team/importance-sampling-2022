import pandas as pd
import numpy as np
import gdown

def stocks_returns(assets, weights, from_date, to_date):
  url = 'https://drive.google.com/file/d/1k9yqsSTtteN6FADDWH8In_9LkFhKJlq_/view?usp=sharing'
  gdown.download(url, 'stock_prices.csv', fuzzy=True)
  stock_prices = pd.read_csv('stock_prices.csv', index_col='date')
  stock_prices = stock_prices.drop(['Unnamed: 0'], axis=1)
  stock_prices.index = pd.to_datetime(stock_prices.index)
  stock_prices_cut = stock_prices[from_date:to_date]
  stock_prices_assets = stock_prices_cut[assets]
  count = 0
  for column in stock_prices_assets:
    stock_prices_assets.loc[:, column] = stock_prices_assets[column] * weights[count]
    count+=1
  stock_prices_assets['price'] = stock_prices_assets.loc[:, :].sum(axis=1)
  returns = [np.NaN]
  for i in range(1, len(stock_prices_asset)):
    day_return = (stock_prices_assets['price'][i] - stock_prices_assets['price'][i-1]) / stock_prices_assets['price'][i-1]
    returns.append(day_return)
  stock_prices_assets['return'] = returns
  stock_prices_assets['return']
  return stock_prices_assets['return']

def commodities_returns(assets, weights, from_date, to_date):
  url = 'https://drive.google.com/file/d/1hVasCNz-qZcBYqvvdlrGAcuc5rNDfPw1/view?usp=sharing'
  gdown.download(url, 'commodities_prices.csv', fuzzy=True)
  commodities_prices = pd.read_csv('commodities_prices.csv', index_col='date')
  commodities_prices = commodities_prices.drop(['Unnamed: 0'], axis=1)
  commodities_prices.index = pd.to_datetime(commodities_prices.index)
  commodities_prices_cut = commodities_prices[from_date:to_date]
  commodities_prices_assets = commodities_prices_cut[assets]
  count = 0
  for column in commodities_prices_assets:
    commodities_prices_assets.loc[:, column] = commodities_prices_assets[column] * weights[count]
    count+=1
  commodities_prices_assets['price'] = commodities_prices_assets.loc[:, :].sum(axis=1)
  returns = [np.NaN]
  for i in range(1, len(commodities_prices_assets)):
    day_return = (commodities_prices_assets['price'][i] - commodities_prices_assets['price'][i-1]) / commodities_prices_assets['price'][i-1]
    returns.append(day_return)
  commodities_prices_assets['return'] = returns
  commodities_prices_assets['return']
  return commodities_prices_assets['return']

def cryptocurrencies_returns(assets, weights, from_date, to_date):
  url = 'https://drive.google.com/file/d/1_t11ugm0P2Yat-jFjRoqnyQ_8PFmxsd9/view?usp=sharing'
  gdown.download(url, 'cryptocurrencies_prices.csv', fuzzy=True)
  cryptocurrencies_prices = pd.read_csv('cryptocurrencies_prices.csv', index_col='date')
  cryptocurrencies_prices = cryptocurrencies_prices.drop(['Unnamed: 0'], axis=1)
  cryptocurrencies_prices.index = pd.to_datetime(cryptocurrencies_prices.index)
  cryptocurrencies_prices_cut = cryptocurrencies_prices[from_date:to_date]
  cryptocurrencies_prices_assets = cryptocurrencies_prices_cut[assets]
  count = 0
  for column in cryptocurrencies_prices_assets:
    cryptocurrencies_prices_assets.loc[:, column] = cryptocurrencies_prices_assets[column] * weights[count]
    count+=1
  cryptocurrencies_prices_assets['price'] = cryptocurrencies_prices_assets.loc[:, :].sum(axis=1)
  returns = [np.NaN]
  for i in range(1, len(cryptocurrencies_prices_assets)):
    day_return = (cryptocurrencies_prices_assets['price'][i] - cryptocurrencies_prices_assets['price'][i-1]) / cryptocurrencies_prices_assets['price'][i-1]
    returns.append(day_return)
  cryptocurrencies_prices_assets['return'] = returns
  cryptocurrencies_prices_assets['return']
  return cryptocurrencies_prices_assets['return']
