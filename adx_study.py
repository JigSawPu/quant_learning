#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep  2 21:42:07 2021

@author: aryakumar
"""

import yfinance as yf
import numpy as np

tickers = ['^NSEI']
ohlcv_data = {}

for ticker in tickers:
    temp = yf.download(ticker, period = '5y', interval = '1d')
    temp.dropna(inplace=True)
    ohlcv_data[ticker] = temp

temp.to_csv('nifty5yr.csv')

# formula for ema: current_value(com/(1+span)) + ema_yesterday(1-(com/(1+span))) 
# day21 price is first ema value if span is 20

def atr(DF, n = 14):
    df = DF.copy()
    df['h-l'] = df['High'] - df['Low']
    df['h-pc'] = df['High'] - df['Adj Close'].shift()
    df['l-pc'] = df['Low'] - df['Adj Close'].shift()
    df['tr'] = df[['h-l','h-pc','l-pc']].max(axis=1,skipna=False)
    df['atr'] = df['tr'].ewm(com=n,min_periods=n).mean()
    return df['atr']


def adx(DF, n = 20):
    df = DF.copy()
    df['atr'] = atr(df,n)
    df['upmove'] = df['High'] - df['High'].shift()
    df['downmove'] = df['Low'].shift()- df['Low']   
    #usage of np.where syntax: where condition: yield x, else yield y
    df['+dm'] = np.where((df['upmove']>df['downmove']) & df['upmove']>0, df['upmove'], 0)
    df['-dm'] = np.where((df['downmove']>df['upmove']) & df['downmove']>0, df['downmove'], 0)
    df['+di'] = 100 * (df['+dm']/df['atr']).ewm(span = n, min_periods=n).mean()
    df['-di'] = 100 * (df['-dm']/df['atr']).ewm(span = n, min_periods=n).mean()
    df['adx'] = 100 * abs((df['+di'] - df['-di'])/(df['+di'] + df['-di'])).ewm(span=n,min_periods=n).mean()
    return df['adx']


for ticker in ohlcv_data:
    ohlcv_data[ticker]['adx'] = adx(ohlcv_data[ticker])
    
    
    # adx values varies from platform to platform signifiacntnly, bt underlying concept remain the same, 
    # somethims try changing 'com' and 'span' 