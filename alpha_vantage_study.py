#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 26 20:22:53 2021

@author: aryakumar
"""

from alpha_vantage.timeseries import TimeSeries
import pandas as pd
import time

api_key = 'QBXRLUZ4BVHEWPSF'

#ts = TimeSeries(key = api_key, output_format='pandas')
#data = ts.get_daily(symbol='MSFT', outputsize='full')[0]
#data.columns = ['Open', 'High', 'Low', 'Close', 'Volume']

all_tickers = ['AAPL', 'MSFT', 'FB', 'AMZN', 'GOOG', 'CSCO']
#5 tickers for alpha vantage free api key
close_prices = pd.DataFrame()

api_call_count = 0

for ticker  in all_tickers:
    start_time = time.time()
    ts = TimeSeries(key = api_key, output_format='pandas')
    data = ts.get_intraday(symbol=ticker, interval = '5min', outputsize='compact')[0]
    api_call_count += 1
    data.columns = ['Open', 'High', 'Low', 'Close', 'Volume']
    
    data = data.iloc[::-1]
    close_prices[ticker] = data.Close
    
    if api_call_count == 5:
        api_call_count = 0
        time.sleep(60 - (time.time() - start_time))

        