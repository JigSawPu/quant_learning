#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 11 21:36:01 2021

@author: aryakumar
"""

import numpy as np
import pandas as pd
import yfinance as yf
import copy
import time


def atr(DF, n = 14):
    df = DF.copy()
    df['h-l'] = df['High'] - df['Low']
    df['h-pc'] = df['High'] - df['Close'].shift()
    df['l-pc'] = df['Low'] - df['Close'].shift()
    df['tr'] = df[['h-l','h-pc','l-pc']].max(axis=1,skipna=False)
    df['atr'] = df['tr'].ewm(com=n,min_periods=n).mean()
    return df['atr']


def CAGR(DF):
    df = DF.copy()
    # 78 is the no of 5 min candles per day
    df['cum return'] = (1+df['ret']).cumprod()
    n = len(df)/(252*78)
    return (df['cum return'][-1])**(1/n) - 1


def volatility(df): 
    return df["ret"].std() * np.sqrt(252*78)


def sharpe(df, rf = 0.03):
    return (CAGR(df)-rf)/volatility(df)


def max_drawdown(DF):
    df = DF.copy()
    df['cum return'] = (1 + df['ret']).cumprod()
    df['cum rolling max'] =  df['cum return'].cummax()
    df['drawdown'] = df['cum rolling max'] - df['cum return']
    return (df['drawdown']/df['cum rolling max']).max()


tickers = ["MSFT","AAPL","FB","AMZN","INTC", "CSCO","VZ","IBM","TSLA","AMD"]

ohlc_intraday = {ticker:yf.download(ticker,period='1mo',interval='5m') for ticker in tickers}
for ticker in tickers:
    ohlc_intraday[ticker].dropna(inplace=True)

ohlc_dict = copy.deepcopy(ohlc_intraday)
tickers_signal,tickers_ret = {ticker:"" for ticker in tickers},{ticker:[] for ticker in tickers}

for ticker in tickers:
    print(f'calculationg atr and roll max price for {ticker}')
    ohlc_dict[ticker]['ATR'],ohlc_dict[ticker]['roll_max_cp'],ohlc_dict[ticker]['roll_min_cp'],ohlc_dict[ticker]['roll_max_vol']  = atr(ohlc_dict[ticker],20),ohlc_dict[ticker]['High'].rolling(20).max(),ohlc_dict[ticker]['Low'].rolling(20).max(),ohlc_dict[ticker]['Volume'].rolling(20).max()
    ohlc_dict[ticker].dropna(inplace=True)
    
