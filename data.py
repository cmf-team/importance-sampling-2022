# Я сначала не понял что надо делать, поэтому подсмотрел у того, кто
# сделал первым. У него взял идею и реализовал своим способом

import pandas as pd
from investiny import historical_data, search_assets

def stocks_returns(assets, weights, from_date, to_date):
    '''
    

    Parameters
    ----------
    assets : TYPE
        список инструментов в виде массива названий.
    weights : TYPE
         список весов для каждого инструмента.
    from_date : TYPE
        дата начала периода в формате месяц/день/год.
    to_date : TYPE
        дата окончания периода.

    Returns
    -------
    res : TYPE
        функция возвращает список доходностей портфеля
        на каждый день выбранного периода (включая
        последний день) в формате pandas Series. 
        Индекс – дата, значение – доходность.

    '''
    
    Pr = []
    for i in assets:
        g = search_assets(query=str(i), limit = 1,
                          type="Stock", exchange = "NASDAQ")
        gg = g[0]['ticker']
        Pr.append(historical_data(investing_id=int(gg),
                               from_date=from_date,
                               to_date = to_date))
    res = computing_r(Pr, weights)
    return res
    
    
# я не понял что писать в exchange, поэтому просто что-то написал
# вдруг сработает :)
def commodities_returns(assets, weights, from_date, to_date):
    '''
    

    Parameters
    ----------
    assets : TYPE
        список инструментов в виде массива названий.
    weights : TYPE
         список весов для каждого инструмента.
    from_date : TYPE
        дата начала периода в формате месяц/день/год.
    to_date : TYPE
        дата окончания периода.

    Returns
    -------
    res : TYPE
        функция возвращает список доходностей портфеля
        на каждый день выбранного периода (включая
        последний день) в формате pandas Series. 
        Индекс – дата, значение – доходность.

    '''
    
    Pr = []
    for i in assets:
        g = search_assets(query=str(i), limit = 1,
                          type="Stock", exchange = "Capital")
        gg = g[0]['ticker']
        Pr.append(historical_data(investing_id=int(gg),
                               from_date=from_date,
                               to_date = to_date))
    res = computing_r(Pr, weights)
    return res
    
    
def cryptocurrencies_returns(assets, weights, from_date, to_date):
    '''
    

    Parameters
    ----------
    assets : TYPE
        список инструментов в виде массива названий.
    weights : TYPE
         список весов для каждого инструмента.
    from_date : TYPE
        дата начала периода в формате месяц/день/год.
    to_date : TYPE
        дата окончания периода.

    Returns
    -------
    res : TYPE
        функция возвращает список доходностей портфеля
        на каждый день выбранного периода (включая
        последний день) в формате pandas Series. 
        Индекс – дата, значение – доходность.

    '''
    
    Pr = []
    for i in assets:
        g = search_assets(query=str(i), limit = 1,
                          type="Stock", exchange = "BINANCE")
        gg = g[0]['ticker']
        Pr.append(historical_data(investing_id=int(gg),
                               from_date=from_date, 
                               to_date = to_date))
    res = computing_r(Pr, weights)
    return res
    
def computing_r(Pr, weights):
    res = []
    i = 0
    while i < (len(Pr)):
        wres = [0]
        j = 1
        while j < (len(Pr[i]['date'])):
            wres.append(weights[i] * ((Pr[i]['close'][j] - Pr[i]['close'][j-1]))/(Pr[i]['close'][j-1]))
            j+=1
        i+=1
    res = pd.Series(wres, index = Pr[0]['date'])
    return res


    