# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import yfinance as yf
import numpy as np

tickers = ['AMZN', 'GOOG', 'MSFT']
ohlcv_data = {}

for ticker in tickers:
    temp = yf.download(ticker, period = '1mo', interval = '5m')
    temp.dropna(inplace=True)
    ohlcv_data[ticker] = temp

def rsi(DF, n = 14):
    df = DF.copy()
    df['change'] = df['Adj Close'] - df['Adj Close'].shift()
    df['gain'] = np.where(df['change'] >= 0,df['change'],0)
    df['loss'] = np.where(df['change'] < 0,(-1)*df['change'],0)
    df['avg gain'] = df['gain'].ewm(alpha=1/n,min_periods=n).mean()
    df['avg loss'] = df['loss'].ewm(alpha=1/n,min_periods=n).mean()
    df['rs'] = df['avg gain']/df['avg loss']
    df['rsi'] = 100 - (100/(1+df['rs']))
    return df['rsi']

for ticker in ohlcv_data:
    ohlcv_data[ticker]['rsi'] = rsi(ohlcv_data[ticker])

