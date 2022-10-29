#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep  5 22:33:57 2021

@author: aryakumar
"""

import yfinance as yf

tickers = ['AMZN','GOOG','MSFT']
ohlcv_data = {}

for ticker in tickers:
    temp = yf.download(ticker, period='7mo', interval = '1d')
    temp.dropna(how= 'any', inplace=True)
    ohlcv_data[ticker] = temp 

def max_drawdown(DF):
    df = DF.copy()
    df['return'] = df['Adj Close'].pct_change()
    df['cum return'] = (1 + df['return']).cumprod()
    df['cum rolling max'] =  df['cum return'].cummax()
    df['drawdown'] = df['cum rolling max'] - df['cum return']
    return (df['drawdown']/df['cum rolling max']).max()


def CAGR(DF):
    df = DF.copy()
    df["return"] = df["Adj Close"].pct_change()
    df['cum return'] = (1+df['return']).cumprod()
    n = len(df)/252
    CAGR = (df['cum return'][-1])**(1/n) - 1
    return CAGR


for ticker in tickers:
    print(f'max drawdown for {ticker} is {max_drawdown(ohlcv_data[ticker])}')
    
    
def calmar(DF):
    df = DF.copy()
    return CAGR(df)/max_drawdown(df)