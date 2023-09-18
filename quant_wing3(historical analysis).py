# -*- coding: utf-8 -*-
"""
Created on Mon Sep 18 13:39:30 2023

@author: Avanish Mohgaonkar
"""

import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
 
tickers =["MSFT","AAPL","TSLA","META"]
stock_data = pd.DataFrame()
daily_returns=pd.DataFrame()
for ticker in tickers:
    stock_data[ticker]=yf.download(ticker,period="10y",interval="1d")["Adj Close"]
    stock_data.dropna(inplace =True)
for ticker in tickers:
    daily_returns[ticker]= np.log(stock_data[ticker]/stock_data[ticker].shift(1))
    daily_returns.dropna(inplace =True)
pflio = 150000
weight = 1/len(tickers)
weights={}
for ticker in tickers:
    weights[ticker]= weight
pflio_returns=pd.DataFrame()
for ticker in tickers:
    pflio_returns[ticker]=daily_returns[ticker]* weights[ticker]
pflio_returns["returns"]= pflio_returns.sum(axis=1)
time_interval_days=10
confidence_interval= 0.95
pflio_returns["rolling_ret"]= pflio_returns["returns"].rolling(window=time_interval_days,min_periods=time_interval_days).sum()
pflio_returns.dropna(inplace=True)
VAR = -np.percentile(pflio_returns["rolling_ret"],(1-confidence_interval)*100)
max_loss = VAR * pflio
pflio_returns["rollling_ret_value"]=pflio_returns["rolling_ret"]*pflio
plt.hist(pflio_returns["rollling_ret_value"],bins=40,density=True)
plt.title("Returns distributution")
plt.xlabel("Portfolio returns")
plt.ylabel("frequency")
plt.axvline(x=-max_loss,color='r',lw=1.5,ls='--',label="VAR")
plt.legend()
plt.show()
print("VAR of portfolio= {}".format(VAR))
print("maximum loss incurred in next {} days with {}% certainity = {}".format(time_interval_days,confidence_interval*100,max_loss))


