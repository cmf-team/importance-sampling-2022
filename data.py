"""
@author: Maria Zykova
"""

import investiny
import numpy as np
from datetime import timedelta, datetime

#сдвиг даты на любое кл-во дней - необходимо чтобы в результатах учитывался весь указанный период
def change_date(date, days_count):
    to_date_tmp = datetime.strptime(date, '%m/%d/%Y')
    to_date_tmp = to_date_tmp + timedelta(days=days_count)
    date = to_date_tmp.strftime('%m/%d/%Y')
    return date


#процесс получения данных по истории
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
        lst.append(data['close'])
    
    return np.array(lst)


#создание портфеля
def profit(data, weights):
    result = []
    new_data = np.array([data[i,:]*weights[i] for i in range(len(data))])
    new_data = new_data.sum(axis=0) #перемножение данных с весами и сложение
    
    #вычисление returns для портфеля
    for i in range(1, len(new_data)):
        result.append((new_data[i] - new_data[i-1])/new_data[i-1])

    return result


def stocks_returns(assets, weights, from_date, to_date):
    data = get_lst_assets(assets, from_date, to_date, types="Stock", exchange="NASDAQ")
    returns = profit(data, weights)
    
    return returns


def commodities_returns(assets, weights, from_date, to_date):
    data = get_lst_assets(assets, from_date, to_date, types="Commodity")
    returns = profit(data, weights)
    
    return returns


def cryptocurrencies_returns(assets, weights, from_date, to_date):
    data = get_lst_assets(assets, from_date, to_date)
    returns = profit(data, weights)
    
    return returns








