import pandas as pd
import datetime as dt
import numpy as np
import investiny as inv

def get_price(assets, weights, from_date, to_date, **exchange):
    returns = pd.DataFrame()
    from_date = (dt.datetime.strptime(from_date, '%m/%d/%Y')-dt.timedelta(days=1)).strftime('%m/%d/%Y')
    to_date= (dt.datetime.strptime(to_date, '%m/%d/%Y')+dt.timedelta(days=1)).strftime('%m/%d/%Y')
    for asset in assets:
        ticker = int(inv.search_assets(query=asset, limit=1, **exchange)[0]['ticker'])
        data = pd.DataFrame(inv.historical_data(investing_id=ticker, from_date=from_date, to_date=to_date)).set_index('date').drop(columns=['open','low','volume','high'])
        returns = pd.concat([returns,data.diff().rename(columns={'close': 'diff_'+asset}),data.rename(columns={'close': asset})],axis = 1)
    del data
    returns['wipim1'] = 0
    returns['widiff'] = 0
    for i in range(len(assets)):
        returns['wipim1'] += returns[assets[i]] * weights[i]
        returns['widiff'] += returns['diff_'+assets[i]] * weights[i]
    returns['wipim1'] = returns.wipim1.shift(1)
    return (returns['widiff']/returns['wipim1']).dropna();
def stocks_returns(assets, weights, from_date, to_date):
    return get_price(assets, weights, from_date, to_date, exchange = 'NASDAQ')
    
def commodities_returns(assets, weights, from_date, to_date):
    return get_price(assets, weights, from_date, to_date, exchange = 'ICE')

def cryptocurrencies_returns(assets, weights, from_date, to_date):
    return get_price(assets, weights, from_date, to_date, exchange = 'Binance')
