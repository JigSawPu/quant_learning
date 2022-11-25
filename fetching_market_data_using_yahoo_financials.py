#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 25 21:40:09 2021

@author: aryakumar
"""

import yfinance as yf
import pandas as pd
import datetime as dt
from yahoofinancials import YahooFinancials

data = yf.download('MSFT', period = '1mo', interval = '5m')

stocks = ['AMZN', 'MSFT', 'GOOG', 'INFY.NS']
start = dt.datetime.today() - dt.timedelta(30)
end = dt.datetime.today()
close_price = pd.DataFrame()


for ticker in stocks:
   close_price[ticker] = yf.download(ticker,start, end)['Adj Close']
   
# to store entire ohlcv values, create dict, then pass dict to for loop
# ex: ohlcv = {} then ohlcv[ticker] = yf downlaod etc

ticker1 = 'MSFT'
yahoo_financials = YahooFinancials(ticker1)
data = yahoo_financials.get_historical_price_data('2021-07-27','2021-08-26','daily')
