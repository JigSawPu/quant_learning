#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep  3 20:28:58 2021

@author: aryakumar
"""

import numpy as np
import pandas as pd
import yfinance as yf

tickers = ['RELIANCE.NS','HDFCBANK.NS','TCS.NS','INFY.NS','ICICIBANK.NS','JUBLFOOD.NS']
ohlcv_data = {}
stocks = pd.DataFrame()

for ticker in tickers:
    temp = yf.download(ticker, period = '15y', interval = '1d')
    temp.dropna(inplace=True)
    ohlcv_data[ticker] = temp
    stocks[ticker] = ohlcv_data[ticker]['Adj Close']

    
log_returns = np.log(stocks/stocks.shift(1))
    
    
np.random.seed(101)

num_portflio = 5000
all_weights = np.zeros((num_portflio,len(stocks.columns)))
retns_arr = np.zeros(num_portflio)
voltily_arr = np.zeros(num_portflio)
sr_arr = np.zeros(num_portflio)

for ind in range(num_portflio):

    weights = np.array(np.random.random(len(stocks.columns)))
    weights = weights/np.sum(weights)
    
    all_weights[ind,:] = weights
    
    #expected return
    retns_arr[ind] = np.sum(log_returns.mean()*weights*252)

    #expected volatilily
    voltily_arr[ind] = np.sqrt(np.dot(weights.T,np.dot(log_returns.cov()*252,weights)))

    #sharpe ratio
    sr_arr[ind] = retns_arr[ind]/voltily_arr[ind]


