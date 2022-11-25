# -*- coding: utf-8 -*-
"""
Spyder Editor

@author: aryakumar
"""

import numpy as np
import pandas as pd
import yfinance as yf 
import matplotlib.pyplot as plt


def CAGR(DF):
    df = DF.copy()
    df['cum return'] = (1+df['mon_ret']).cumprod()
    n = len(df)/12
    return (df['cum return'].tolist()[-1])**(1/n) - 1


def volatility(df):
    return df["mon_ret"].std() * np.sqrt(12)


def sharpe(df,rf = 0.03):
    return (CAGR(df)-rf)/volatility(df)


def max_drawdown(DF):
    df = DF.copy()
    df['cum return'] = (1 + df['mon_ret']).cumprod()
    df['cum rolling max'] =  df['cum return'].cummax()
    df['drawdown'] = df['cum rolling max'] - df['cum return']
    return (df['drawdown']/df['cum rolling max']).max()


tickers = ["MMM","AXP","T","BA","CAT","CSCO","KO", "XOM","GE","GS","HD",
           "IBM","INTC","JNJ","JPM","MCD","MRK","MSFT","NKE","PFE","PG","TRV",
           "UNH","VZ","V","WMT","DIS"]

ohlc_mon = {ticker:yf.download(ticker,period='10y',interval='1mo') for ticker in tickers}
for ticker in tickers:
    ohlc_mon[ticker].dropna(inplace=True)

return_df = pd.DataFrame([ohlc_mon[tickers[i]]["Adj Close"].pct_change() for i in range(len(tickers))]).T[1:]
return_df.columns = tickers

def pflio(DF,m,x):
    """Returns cumulative portfolio return
    DF = dataframe with monthly return info for all stocks
    m = number of stock in the portfolio
    x = number of underperforming stocks to be removed from portfolio monthly"""
    df = DF.copy()
    portfolio = []
    monthly_ret = [0]
    for i in range(len(df)):
        if len(portfolio) > 0:
            monthly_ret.append(df[portfolio].iloc[i,:].mean())
            bad_stocks = df[portfolio].iloc[i,:].sort_values(ascending=True)[:x].index.values.tolist()
            portfolio = [t for t in portfolio if t not in bad_stocks]
        fill = m - len(portfolio)
        new_picks = df.iloc[i,:].sort_values(ascending=False)[:fill].index.values.tolist()
        portfolio = portfolio + new_picks
        print(portfolio)
    return pd.DataFrame(np.array(monthly_ret),columns=["mon_ret"])


CAGR(pflio(return_df,6,3))
sharpe(pflio(return_df,6,3),0.025)
max_drawdown(pflio(return_df,6,3)) 

DJI = yf.download("^DJI",period='10y',interval='1mo')
DJI["mon_ret"] = DJI["Adj Close"].pct_change().fillna(0)
CAGR(DJI)
sharpe(DJI,0.025)
max_drawdown(DJI)

fig, ax = plt.subplots()
plt.plot((1+pflio(return_df,6,3)).cumprod())
plt.plot((1+DJI["mon_ret"].reset_index(drop=True)).cumprod())
plt.title("Index Return vs Strategy Return")
plt.ylabel("cumulative return")
plt.xlabel("months")
ax.legend(["Strategy Return","Index Return"])
