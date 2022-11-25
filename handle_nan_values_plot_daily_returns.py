#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 27 21:38:28 2021

@author: aryakumar
"""

import datetime as dt
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt


stocks = ['AMZN', 'MSFT', 'FB', 'GOOG']
start = dt.datetime.today() - dt.timedelta(3650)
end = dt.datetime.today()
close_price = pd.DataFrame()

for ticker in stocks:
    close_price[ticker] = yf.download(ticker, start, end)['Adj Close']

close_price = close_price.iloc[::-1]

#fillna(method = 'bfill',axis=1) fills na value with first non  na value
close_price.dropna(inplace=True)

daily_return = close_price.pct_change() #maybe close_price[ticker].pct_change()
daily_return.mean()

daily_return.rolling(10, min_periods=10).mean()
daily_return.ewm(com=10, min_periods=10).mean()

close_price.plot(subplots = True, layout = (2,2))

fig, ax = plt.subplots()
plt.style.use('ggplot')
ax.set(title='mean daliy return', xlabel = 'stocks', ylabel='mean return')
plt.bar(x=daily_return.columns,height=daily_return.mean())
plt.bar(x=daily_return.columns,height=daily_return.std())
