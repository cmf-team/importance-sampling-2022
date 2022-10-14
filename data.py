import investiny
import pandas as pd
import numpy as np
import yfinance as yf
from investiny import historical_data, search_assets


def com_n_crypto(assets, weights, from_date, to_date):
    stock_data = pd.Series()
    asset_number = 0
    arr_of_day_price = []
    to_date = pd.to_datetime(to_date) + pd.DateOffset(1)
    to_date =  str(to_date.month) + "/" + str(to_date.day) + "/" + str(to_date.year)
    print(to_date)
    for asset in assets:
        history = historical_data(investiny.search_assets(query=asset, limit=1)[0]["ticker"], from_date=from_date,
                                  to_date=to_date)
        date_history = history["date"]
        price_history = history["close"]


        for price in range(0, len(price_history)):
            try:
                arr_of_day_price.append(price_history[price] * weights[asset_number % len(assets)])
            except:
                arr_of_day_price[price] += price_history[price] * weights[asset_number % len(assets)]
        asset_number += 1

    for day in range(1, len(price_history)):
        try:
            stock_data[pd.to_datetime(date_history[day])] += (arr_of_day_price[day] - arr_of_day_price[day - 1]) / \
                                                             arr_of_day_price[day - 1]
        except:
            stock_data[pd.to_datetime(date_history[day])] = (arr_of_day_price[day] - arr_of_day_price[day - 1]) / \
                                                            arr_of_day_price[day - 1]
    print(stock_data)
    return stock_data


def stocks_returns(assets, weights, from_date, to_date):
    stock_data = pd.Series()
    asset_number = 0
    arr_of_day_price = []
    for asset in assets:
        history = yf.Ticker(asset).history(start=pd.to_datetime(from_date), end=pd.to_datetime(to_date) + pd.DateOffset(1))
        date_history = history.index
        price_history = history["Close"]

        for price in range(0, len(price_history)):
            if (len(arr_of_day_price) - 1 < price):
                arr_of_day_price.append(price_history[price] * weights[asset_number % len(assets)])
            else:
                arr_of_day_price[price] += price_history[price] * weights[asset_number % len(assets)]
        asset_number += 1

    for day in range(1, len(price_history)):
        # today_return +=
        try:
            stock_data[date_history[day]] += (arr_of_day_price[day]-arr_of_day_price[day-1])/arr_of_day_price[day-1]
        except:
            stock_data[date_history[day]] = (arr_of_day_price[day]-arr_of_day_price[day-1])/arr_of_day_price[day-1]
    print(stock_data)
    return stock_data
# stocks_returns(["AAPL"], [1], "9/1/2022", "09/07/2022")


def commodities_returns(assets, weights, from_date, to_date):
    return com_n_crypto(assets, weights, from_date, to_date)


def cryptocurrencies_returns(assets, weights, from_date, to_date):
    return com_n_crypto(assets, weights, from_date, to_date)


# cryptocurrencies_returns(["ETH", "BTC"], [0.3, 0.7], "09/01/2022", "09/07/2022")

