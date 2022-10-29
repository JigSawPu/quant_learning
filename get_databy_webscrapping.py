#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 27 19:32:33 2021

@author: aryakumar
"""

import requests
from bs4 import BeautifulSoup

url = 'https://finance.yahoo.com/quote/MSFT/balance-sheet?p=MSFT'
page = requests.get(url)

page_content = page.content
soup = BeautifulSoup(page_content, 'html.parser')

table = soup.find_all()