#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep  5 16:54:51 2021

@author: aryakumar
"""

import yfinance as yf
import numpy as np
import pandas as pd

tickers = ['AMZN','GOOG','MSFT']
ohlcv_data = {}

for ticker in tickers:
    temp = yf.download(ticker, period='7mo', interval = '1d')
    temp.dropna(how= 'any', inplace=True)
    ohlcv_data[ticker] = temp 

    
def CAGR(DF):
    df = DF.copy()
    df["return"] = df["Adj Close"].pct_change()
    df['cum return'] = (1+df['return']).cumprod()
    n = len(df)/252
    CAGR = (df['cum return'][-1])**(1/n) - 1
    return CAGR


for ticker in tickers:
    print(f'cagr for {ticker} is {CAGR(ohlcv_data[ticker])}')
    
    
    
#use std for volatility calc
# to annualize multiply by sqrt 252/52/12 as per time periso
#just copy paster vol code

def volatility(DF):
    "function to calculate annualized volatility of a trading strategy"
    df = DF.copy()
    df["return"] = df["Adj Close"].pct_change()
    vol = df["daily_ret"].std() * np.sqrt(252)
    return vol


def sharpe(DF, rf = 0.03):
    df = DF.copy()
    return (CAGR(df)-rf)/volatility(df)


#although useless lets do 

def sortino(DF, rf = 0.03):
    df = DF.copy()
    df['return'] = df['Adj Close'].pct_change()
    neg_return = np.where(df['return']>0,0,df['return'])
    neg_vol = pd.Series(neg_return[neg_return!=0]).std()*np.sqrt(252)
    return (CAGR(df)-rf)/neg_vol


for ticker in tickers:
    print(f'sortino for {ticker} is {sortino(ohlcv_data[ticker])}')
    