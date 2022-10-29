#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep  3 14:29:37 2021

@author: aryakumar
"""

import yfinance as yf
from stocktrends import Renko

tickers = ['AMZN', 'GOOG', 'MSFT']
ohlcv_data = {}
hour_data = {}
renko_data = {}

for ticker in tickers:
    temp = yf.download(ticker, period = '1mo', interval = '5m')
    temp.dropna(inplace=True)
    ohlcv_data[ticker] = temp
    temp = yf.download(ticker, period = '1y', interval = '1h')
    temp.dropna(inplace=True)
    hour_data[ticker] = temp
    

def atr(DF, n = 14):
    df = DF.copy()
    df['h-l'] = df['High'] - df['Low']
    df['h-pc'] = df['High'] - df['Adj Close'].shift()
    df['l-pc'] = df['Low'] - df['Adj Close'].shift()
    df['tr'] = df[['h-l','h-pc','l-pc']].max(axis=1,skipna=False)
    df['atr'] = df['tr'].ewm(com=n,min_periods=n).mean()
    return df['atr']


def renko(DF, hourly_df):
    df = DF.copy()
    df.drop('Close',axis=1,inplace=True)
    df.reset_index(inplace=True)
    df.columns = ['date','open','high','low','close','volume']
    df2 = Renko(df)
    df2.brick_size = round(3*atr(hourly_df,120).iloc[-1])
    renko_df = df2.get_ohlc_data()
    return renko_df


for ticker in ohlcv_data:
    renko_data[ticker] = renko(ohlcv_data[ticker], hour_data[ticker])
    
        