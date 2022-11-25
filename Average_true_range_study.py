#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 29 20:49:18 2021

@author: aryakumar
"""

import yfinance as yf

tickers = ['AMZN', 'GOOG', 'MSFT']
ohlcv_data = {}

for ticker in tickers:
    temp = yf.download(ticker, period = '1mo', interval = '5m')
    temp.dropna(inplace=True)
    ohlcv_data[ticker] = temp
    
def atr(DF, n = 14):
    df = DF.copy()
    df['h-l'] = df['High'] - df['Low']
    df['h-pc'] = df['High'] - df['Adj Close'].shift()
    df['l-pc'] = df['Low'] - df['Adj Close'].shift()
    df['tr'] = df[['h-l','h-pc','l-pc']].max(axis=1,skipna=False)
    df['atr'] = df['tr'].ewm(com=n,min_periods=n).mean()
    return df['atr']

for ticker in ohlcv_data:
    ohlcv_data[ticker]['atr'] = atr(ohlcv_data[ticker]) 
    
    #for bollinger band ddof=0, for whole popualtion