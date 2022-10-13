pip install -r requirements.txt
import pandas as pd
import numpy as np
import investiny
from investiny import historical_data
from investiny import search_assets
from datetime import datetime, timedelta



def stocks_returns(assets, weights, from_date, to_date):
    
    from_date = datetime.strftime(datetime.strptime(from_date, '%m/%d/%Y') - timedelta(days=1), '%m/%d/%Y')
    to_date = datetime.strftime(datetime.strptime(to_date, '%m/%d/%Y') + timedelta(days=1), '%m/%d/%Y')
    DATA = pd.DataFrame([])
    
    for i in range(len(assets)):
        search_results = search_assets(query = assets[i], limit=1, type="Stock", exchange="NASDAQ")
        investing_id = int(search_results[0]["ticker"]) # Assuming the first entry is the desired one (top result in Investing.com)
        data = pd.DataFrame(historical_data(investing_id=investing_id, from_date=from_date, to_date=to_date)).drop(['volume', 'high', 'low', 'open'], axis = 1)
        if DATA.empty:
            DATA = data 
            DATA.close = DATA.close * weights[i]
        else:
            DATA.close = DATA.close + (data.close * weights[i])
            
    DATA.close = DATA.close.pct_change()
    total_return = DATA.rename(columns = {'close': 'stocks_returns'}).set_index('date')['stocks_returns'].iloc[1:]
    return total_return

def commodities_returns(assets, weights, from_date, to_date):
    from_date = datetime.strftime(datetime.strptime(from_date, '%m/%d/%Y') - timedelta(days=1), '%m/%d/%Y')
    to_date = datetime.strftime(datetime.strptime(to_date, '%m/%d/%Y') + timedelta(days=1), '%m/%d/%Y')
    DATA = pd.DataFrame([])
    
    for i in range(len(assets)):
    
        search_results = search_assets(query = assets[i], limit=1, type="Commodity")
        investing_id = int(search_results[0]["ticker"]) # Assuming the first entry is the desired one (top result in Investing.com)
        data = pd.DataFrame(historical_data(investing_id=investing_id, from_date=from_date, to_date=to_date)).drop(['volume', 'high', 'low', 'open'], axis = 1)
        if DATA.empty:
            DATA = data 
            DATA.close = DATA.close * weights[i]
        else:
            DATA.close = DATA.close + (data.close * weights[i])
            
    DATA.close = DATA.close.pct_change()
    total_return = DATA.rename(columns = {'close': 'commodities_returns'}).set_index('date')['commodities_returns'].iloc[1:]
    return total_return

def cryptocurrencies_returns(assets, weights, from_date, to_date):
    from_date = datetime.strftime(datetime.strptime(from_date, '%m/%d/%Y') - timedelta(days=1), '%m/%d/%Y')
    to_date = datetime.strftime(datetime.strptime(to_date, '%m/%d/%Y') + timedelta(days=1), '%m/%d/%Y')
    DATA = pd.DataFrame([])
    
    for i in range(len(assets)):
        search_results = search_assets(query = assets[i], limit=1)
        investing_id = int(search_results[0]["ticker"]) # Assuming the first entry is the desired one (top result in Investing.com)
        data = pd.DataFrame(historical_data(investing_id=investing_id, from_date=from_date, to_date=to_date)).drop(['volume', 'high', 'low', 'open'], axis = 1)
        
        if DATA.empty:
            DATA = data 
            DATA.close = DATA.close * weights[i]
        else:
            DATA.close = DATA.close + (data.close * weights[i])
            
    DATA.close = DATA.close.pct_change()
    total_return = DATA.rename(columns = {'close': 'cryptocurrencies_returns'}).set_index('date')['cryptocurrencies_returns'].iloc[1:]
    return total_return
