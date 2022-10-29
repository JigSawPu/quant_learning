#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 26 19:32:02 2021

@author: aryakumar
"""

import pandas as pd
import datetime as dt
from yahoofinancials import YahooFinancials

all_tickers = ['AAPL', 'MSFT', 'CSCO', 'AMZN']

close_prices = pd.DataFrame()

end_date = dt.date.today().strftime('%Y-%m-%d')
start_date = (dt.date.today() - dt.timedelta(180)).strftime('%Y-%m-%d')

for ticker in all_tickers:
    yahoo_financials = YahooFinancials(ticker)
    json_obv = yahoo_financials.get_historical_price_data(start_date, end_date, 'daily')
    ohlv = json_obv[ticker]['prices']
    temp = pd.DataFrame(ohlv)[['formatted_date','adjclose']]
    temp.set_index('formatted_date', inplace=True)
    temp.dropna(inplace = True)
    close_prices[ticker] = temp.adjclose
    
    