import pandas as pd
import datetime as dt
import investiny as inv


def cryptocurrencies_returns(assets, weights, from_date, to_date):
    from_date = (dt.datetime.strptime(from_date, '%m/%d/%Y')-dt.timedelta(days=1)).strftime('%m/%d/%Y')
    to_date= (dt.datetime.strptime(to_date, '%m/%d/%Y')+dt.timedelta(days=1)).strftime('%m/%d/%Y')
    returns = pd.DataFrame()
    for asset in assets:
        ticker = int(inv.search_assets(query=asset, limit=1, exchange='Binance')[0]['ticker'])
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
    from_date = (dt.datetime.strptime(from_date, '%m/%d/%Y')-dt.timedelta(days=1)).strftime('%m/%d/%Y')
    to_date= (dt.datetime.strptime(to_date, '%m/%d/%Y')+dt.timedelta(days=1)).strftime('%m/%d/%Y')
    returns = pd.DataFrame()
    for asset in assets:
        ticker = int(inv.search_assets(query=asset, limit=1, exchange='NASDAQ')[0]['ticker'])
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
def commodities_returns(assets, weights, from_date, to_date):
    from_date = (dt.datetime.strptime(from_date, '%m/%d/%Y')-dt.timedelta(days=1)).strftime('%m/%d/%Y')
    to_date= (dt.datetime.strptime(to_date, '%m/%d/%Y')+dt.timedelta(days=1)).strftime('%m/%d/%Y')
    returns = pd.DataFrame()
    for asset in assets:
        ticker = int(inv.search_assets(query=asset, limit=1, exchange='ICE')[0]['ticker'])
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

assets = ['APPL']
weights = [1.]
print(stocks_returns(assets, weights, from_date='09/02/2022', to_date='09/07/2022'))
# TEST DATA
# stocks = ['APPL','GOOGL']
# cryptos = ['BTCUSD','BNBUSD']
# commodities  = ['US Coffee C Futures','Crude Oil WTI Futures']

# weights = [0.3, 0.7]
# from_date="09/01/2022"
# to_date="09/07/2022"
# print(cryptos)
# print(cryptocurrencies_returns(cryptos, weights, from_date, to_date))
# print(stocks)
# print(stocks_returns(stocks, weights, from_date, to_date))
# print(commodities)
# print(commodities_returns(commodities, weights, from_date, to_date))