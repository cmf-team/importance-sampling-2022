import pandas as pd
import numpy as np
import gdown
from datetime import datetime, timedelta


def the_day_before_start(date, days_count):
#the_day_before_start is designed to get the date a day earlier than the required one.
    to_date_tmp = datetime.strptime(date, '%m/%d/%Y')
    to_date_tmp = to_date_tmp + timedelta(days=days_count)
    date = to_date_tmp.strftime('%m/%d/%Y')
    return date

def portfolio(prices, assets, weights, from_date, to_date):
#portfolio takes prices dataframe, assets, weights and dates. Return portfolio daily return.
  prices.index = pd.to_datetime(prices.index)
  from_date_new = the_day_before_start(from_date, -1)
  prices_assets = prices.loc[from_date_new:to_date, assets]
  count = 0
  for column in prices_assets:
    prices_assets.loc[:, column] = prices_assets[column] * weights[count]
    count+=1
  prices_assets['price'] = prices_assets.loc[:, :].sum(axis=1)
  returns = []
  for i in range(1, len(prices_assets)):
    day_return = (prices_assets['price'][i] - prices_assets['price'][i-1]) / prices_assets['price'][i-1]
    returns.append(day_return)
  prices_assets = prices_assets.drop(index=[from_date_new])
  prices_assets['return'] = returns
  prices_assets['return']
  return prices_assets['return']

def stocks_returns(assets, weights, from_date, to_date):
#stocks_returns downloads data and applies portfolio function.
  url = 'https://drive.google.com/file/d/1hG9vEXemZMY8a8dnX0an_KGr8suCijwU/view?usp=sharing'
  gdown.download(url, 'stock_prices.csv', fuzzy=True)
  stock_prices = pd.read_csv('stock_prices.csv', index_col='date')
  stock_returns = portfolio(stock_prices, assets, weights, from_date, to_date)
  return stock_returns

def commodities_returns(assets, weights, from_date, to_date):
#commodities_returns downloads data and applies portfolio function.
  url = 'https://drive.google.com/file/d/1ZlGW41Zcc5uWbmRVSelcDsZLf4y49L6M/view?usp=sharing'
  gdown.download(url, 'commodities_prices.csv', fuzzy=True)
  commodities_prices = pd.read_csv('commodities_prices.csv', index_col='date')
  commodities_returns = portfolio(commodities_prices, assets, weights, from_date, to_date)
  return commodities_returns

def cryptocurrencies_returns(assets, weights, from_date, to_date):
#cryptocurrencies_returns downloads data and applies portfolio function.
  url = 'https://drive.google.com/file/d/1XMn8f_iGPtqB1iJQQ63pN_AQ0UynVzct/view?usp=sharing'
  gdown.download(url, 'cryptocurrencies_prices.csv', fuzzy=True)
  cryptocurrencies_prices = pd.read_csv('cryptocurrencies_prices.csv', index_col='date')
  cryptocurrencies_returns = portfolio(cryptocurrencies_prices, assets, weights, from_date, to_date)
  return cryptocurrencies_returns
