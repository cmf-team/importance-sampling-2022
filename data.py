import pandas as pd
import numpy as np
import investiny

def stocks_returns(assets, weights, from_date, to_date):
    st_data = []
    i = 0
    for sec in assets:
        sec_id = investiny.search_assets(query=sec, limit=1, exchange="NASDAQ")[0]['ticker']
        data = investiny.historical_data(sec_id, from_date, to_date)
        dates = data['date']
        st_data.append([j * weights[i] for j in data['close']])
        i += 1
    res = pd.DataFrame(data = np.array(st_data), columns = dates).T 
    res = res.sum(axis=1)
    res = (res.diff()/res.shift(1)).dropna()
    return(res)

def commodities_returns(assets, weights, from_date, to_date):
    st_data = []
    i = 0
    for sec in assets:
        sec_id = investiny.search_assets(query=comm[0], limit=1, type='Commodity')[0]["ticker"]
        data = investiny.historical_data(sec_id, from_date, to_date)
        dates = data['date']
        st_data.append([j * weights[i] for j in data['close']])
        i += 1
    res = pd.DataFrame(data = np.array(st_data), columns = dates).T 
    res = res.sum(axis=1)
    res = (res.diff()/res.shift(1)).dropna()
    return(res)

def cryptocurrencies_returns(assets, weights, from_date, to_date):
    st_data = []
    i = 0
    for sec in assets:
        sec_id = investiny.search_assets(query=comm[0], limit=1)[0]["ticker"]
        data = investiny.historical_data(sec_id, from_date, to_date)
        dates = data['date']
        st_data.append([j * weights[i] for j in data['close']])
        i += 1
    res = pd.DataFrame(data = np.array(st_data), columns = dates).T 
    res = res.sum(axis=1)
    res = (res.diff()/res.shift(1)).dropna()
    return(res)
