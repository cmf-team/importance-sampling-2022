import yfinance as yf
import pandas as pd
import numpy as np
import datetime as dt

def stocks_returns(assets, weights, from_date, to_date):
    available_assets = ["AAPL", 'AMD', 'TSLA', 'AMZN', 'NVDA', 'INTC', 'MU', 'MSFT', 'META', 'GOOGL']
    flag = 0
    for requested_asset in assets[:]:
        if requested_asset not in available_assets:
            print('Cannot extract information on {}. See the list of available assets.'.format(requested_asset))
            assets.remove(requested_asset)
            flag = 1
    if flag == 1:
        print(available_assets)
        
    if len(assets) != len(weights):
        print('Assets and Weights lenght do not match. Correct the vectors.')
        return None
    symbols = yf.download(assets, from_date, to_date)
    symbols = symbols['Close'].reset_index()
    symbols['Date'] = pd.to_datetime(symbols['Date'].dt.strftime('%Y-%m-%d'))
    symbols.index = symbols['Date']
    symbols.drop('Date', axis = 1, inplace = True)
    for column in symbols.columns:
        symbols[column] = (symbols[column] - symbols[column].shift(1))/symbols[column]
    
    symbols = symbols.iloc[1:, :]
    symbols = symbols.fillna(0)
    
    if len(assets)==1:
        symbols.columns = assets
    
    symbols['portfolio'] = [0]*symbols.shape[0]
    
    for i in range(len(assets)):
        column = assets[i]
        weight = weights[i]
        symbols['portfolio'] += weight * symbols[column]
    
    return symbols['portfolio']

def commodities_returns(assets, weights, from_date, to_date):
    commodities_dict = {'Brent Oil Futures': 'BZ=F', 'Crude Oil WTI Futures': 'CL=F', 'Natural Gas Futures': 'NG=F', 'Heating Oil Futures': 'HO=F', 
                        'Gold Futures': 'GC=F', 'Silver Futures': 'SI=F', 'Copper Futures': 'HG=F', 'Platinum Futures': 'PL=F', 'US Coffe C Futures': 'KC=F', 'US Corn Futures': 'ZC=F'}
    flag = 0
    for requested_asset in assets[:]:
        if requested_asset not in commodities_dict.keys():
            print('Cannot extract information on {}. See the list of available assets.'.format(requested_asset))
            assets.remove(requested_asset)
            flag = 1
    if flag == 1:
        print(list(commodities_dict.keys()))
        
    if len(assets) != len(weights):
        print('Assets and Weights lenght do not match. Correct the vectors.')
        return None
    
    symbols_list = [commodities_dict[asset] for asset in assets]
    symbols = yf.download(symbols_list, from_date, to_date)
    symbols = symbols['Close'].reset_index()
    symbols['Date'] = pd.to_datetime(symbols['Date'].dt.strftime('%Y-%m-%d'))
    symbols.index = symbols['Date']
    symbols.drop('Date', axis = 1, inplace = True)
    for column in symbols.columns:
        symbols[column] = (symbols[column] - symbols[column].shift(1))/symbols[column]
    symbols = symbols.iloc[1:, :]
    symbols = symbols.fillna(0)
    
    if len(symbols_list)==1:
        symbols.columns = symbols_list
    
    symbols['portfolio'] = [0]*symbols.shape[0]
    for i in range(len(symbols_list)):
        column = symbols_list[i]
        weight = weights[i]
        symbols['portfolio'] += weight * symbols[column]
    
    return symbols['portfolio']

def cryptocurrencies_returns(assets, weights, from_date, to_date):
    available_assets = ['BTC-USD', 'ETH-USD', 'USDT-USD', 'USDC-USD', 'BNB-USD', 'XRP-USD', 'BUSD-USD', 'ADA-USD', 'SOL-USD', 'DOGE-USD']
    flag = 0
    for requested_asset in assets[:]:
        if requested_asset not in available_assets:
            print('Cannot extract information on {}. See the list of available assets.'.format(requested_asset))
            assets.remove(requested_asset)
            flag = 1
    if flag == 1:
        print(available_assets)
        
    if len(assets) != len(weights):
        print('Assets and Weights lenght do not match. Correct the vectors.')
        return None
    symbols = yf.download(assets, from_date, to_date)
    symbols = symbols['Close'].reset_index()
    symbols['Date'] = pd.to_datetime(symbols['Date'].dt.strftime('%Y-%m-%d'))
    symbols.index = symbols['Date']
    symbols.drop('Date', axis = 1, inplace = True)
    
    for column in symbols.columns:
        symbols[column] = (symbols[column] - symbols[column].shift(1))/symbols[column]
    symbols = symbols.iloc[1:, :]
    symbols = symbols.fillna(0)
    
    if len(assets)==1:
        symbols.columns = assets
    
    symbols['portfolio'] = [0]*symbols.shape[0]
    for i in range(len(assets)):
        column = assets[i]
        weight = weights[i]
        symbols['portfolio'] += weight * symbols[column]
    
    return symbols['portfolio']
