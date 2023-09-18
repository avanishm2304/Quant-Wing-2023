# -*- coding: utf-8 -*-
"""
Created on Tue Sep 12 12:36:46 2023

@author: Avanish Mohgaonkar
"""

import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt
from sklearn.linear_model import LinearRegression
import numpy as np
ticker_1= "^NSEI"
ticker_2 ="RELIANCE.NS"
start = dt.datetime.today()-dt.timedelta(365)
end = dt.datetime.today()-dt.timedelta(1)
df_nifty = yf.download(ticker_1,start,end,interval = "1d")
df_nifty.reset_index(inplace=True)
df_stock= yf.download(ticker_2,start,end,interval = "1d")
df_stock.reset_index(inplace=True)
fig,axes = plt.subplots(nrows=2,ncols=1,figsize=(10,5))
axes[0].plot(df_nifty["Date"],df_nifty["Adj Close"],"b",label=ticker_1)
axes[0].plot(df_stock["Date"],df_stock["Adj Close"],"r",label=ticker_2)
axes[0].set_title("comparison of close prices")
axes[0].set_xlabel("Date")
axes[0].set_ylabel("Close prices")
plt.legend()
df_nifty["daily_return"]= df_nifty["Adj Close"].pct_change()
df_stock["daily_return"]=df_stock["Adj Close"].pct_change()
df_nifty.dropna(how="any",inplace=True)
df_stock.dropna(how="any",inplace=True)
df_nifty["cum_returns"]=(1+df_nifty["daily_return"]).cumprod()
df_stock["cum_returns"]=(1+df_stock["daily_return"]).cumprod()
axes[1].plot(df_nifty["Date"],df_nifty["cum_returns"],"b",label=ticker_1)
axes[1].plot(df_stock["Date"],df_stock["cum_returns"],"r",label=ticker_2)
axes[1].set_title("comparison of cumulative daily returns")
axes[1].set_xlabel("Date")
axes[1].set_ylabel("cumulative daily returns")
plt.legend()
plt.tight_layout()
plt.show()
model = LinearRegression()
x = np.array(df_nifty["daily_return"]).reshape(-1,1)
y = np.array(df_stock["daily_return"])
model.fit(x,y)
r_square= model.score(x,y)
alpha = model.intercept_
beta = model.coef_[0]
print("Coefficient of determination is (R^2):",r_square)
print("value of alpha is:",alpha)
print("value of beta is:",beta)
rf_rate = 0.06
exp_ret_nifty = df_nifty["cum_returns"].iloc[-1]-1 # calculated the rate of return not the expected rate of return(can calculate rate of returns for nifty for a higher time period to get more accurate value)
mar_risk_prem = exp_ret_nifty - rf_rate
exp_ret_stock= rf_rate + beta*mar_risk_prem
print("expected return of stock using CAPM:{}%".format(exp_ret_stock*100))

