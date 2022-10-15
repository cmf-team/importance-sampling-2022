import pandas as pd
import numpy as np
import investiny
from investiny import historical_data, search_assets
from datetime import timedelta, date, datetime


def change_date(date, days_count):
    to_date_tmp = datetime.strptime(date, '%m/%d/%Y')
    to_date_tmp = to_date_tmp + timedelta(days=days_count)
    date = to_date_tmp.strftime('%m/%d/%Y')
    return(date)

def get_lst_assets(assets, from_date, to_date, types = "False", exchange = "False"):
    lst= []
    for name in assets:
        if types == "False":
            results = investiny.search_assets(query=name, limit=1)
        else:
            if exchange != "False":
                results = investiny.search_assets(query=name, limit=1, type=types, exchange="NASDAQ")
            else:
                results = investiny.search_assets(query=name, limit=1, type=types)

        investing_id = int(results[0]["ticker"])
        data = investiny.historical_data(investing_id=investing_id, from_date=from_date, to_date=to_date)
        lst_date = data['date']
        lst.append(data['close'])
    res = pd.DataFrame(data = np.array(lst), columns = lst_date)
    return(res)

def stocks_returns(assets, weights, from_date, to_date):
    from_date = change_date(from_date, -1)
    to_date = change_date(to_date, 1)
    
    x = get_lst_assets(assets, from_date=from_date, to_date=to_date)
    x = x.T
    x.index = pd.to_datetime(x.index)
    for col in list(x.columns):
        x[col] = x[col] * weights[col]
    x = x.sum(axis=1)
    x = (x.diff()/x.shift(1)).dropna()
    return(x)

def commodities_returns(assets, weights, from_date, to_date):
    x = get_lst_assets(assets, from_date=from_date, to_date=to_date)
    x = x.T
    x.index = pd.to_datetime(x.index)
    for col in list(x.columns):
        x[col] = x[col] * weights[col]
    x = x.sum(axis=1)
    x = (x.diff()/x.shift(1)).dropna()
    return(x)

def cryptocurrencies_returns(assets, weights, from_date, to_date):
    x = get_lst_assets(assets, from_date=from_date, to_date=to_date)
    x = x.T
    x.index = pd.to_datetime(x.index)
    for col in list(x.columns):
        x[col] = x[col] * weights[col]
    x = x.sum(axis=1)
    x = (x.diff()/x.shift(1)).dropna()
    return(x)
