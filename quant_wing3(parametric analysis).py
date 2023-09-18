# -*- coding: utf-8 -*-
"""
Created on Thu Sep 14 14:51:09 2023

@author: Avanish Mohgaonkar
"""

import yfinance as yf
import numpy as np
from scipy.stats import norm
tickers =["NFLX","MSFT","AAPL"]
daily_data={}
data_for_CAGR={}
exp_annual_returns={}
std_dev={}
pflio=100000
weight = 1/len(tickers)
weights={}
for ticker in tickers:
    weights[ticker]= weight
for ticker in tickers:
    daily_data[ticker]= yf.download(ticker,period= "1y",interval="1d")
    daily_data[ticker]["daily_returns"]= daily_data[ticker]["Adj Close"].pct_change()
    daily_data[ticker].dropna(inplace=True)
for ticker in tickers:
    data_for_CAGR[ticker]= yf.download(ticker,period= "5y",interval="1d")
    data_for_CAGR[ticker].dropna(inplace=True)
  
def CAGR(DF):
    df = DF.copy()
    df["cum_return"] = (1 + df["Adj Close"].pct_change()).cumprod()
    n = len(df)/(252)
    CAGR = (df["cum_return"].tolist()[-1])**(1/n) - 1
    return CAGR
for ticker in tickers:
    exp_annual_returns[ticker]=CAGR(data_for_CAGR[ticker])
    std_dev[ticker]= daily_data[ticker]["daily_returns"].std()*(np.sqrt(252))
cov_NM= (np.cov(daily_data["NFLX"]["daily_returns"],daily_data["MSFT"]["daily_returns"])[0,1])*252
cov_NA= (np.cov(daily_data["NFLX"]["daily_returns"],daily_data["AAPL"]["daily_returns"])[0,1])*252
cov_AM= (np.cov(daily_data["AAPL"]["daily_returns"],daily_data["MSFT"]["daily_returns"])[0,1])*252
calculation_1=0
for ticker in tickers:
    calculation_1+=(std_dev[ticker]**2)*(weights[ticker]**2)
calculation_2= 2*weights["NFLX"]*weights["MSFT"]*cov_NM + 2*weights["AAPL"]*weights["MSFT"]*cov_AM + 2*weights["NFLX"]*weights["AAPL"]*cov_NA
pflio_std = np.sqrt(calculation_1 + calculation_2)
time_interval_days = 20
confidence_interval =0.95
pflio_exp_return= 0
for ticker in tickers:
    pflio_exp_return += exp_annual_returns[ticker]* weights[ticker]
z_score = norm.ppf(confidence_interval)
VAR = pflio_std*z_score*(np.sqrt(time_interval_days/252))
loss = pflio* VAR
print("expected return of portfolio= {}%".format(pflio_exp_return*100))
print("VAR of portfolio= {}".format(VAR))
print("maximum loss incurred in next {} days with {}% certainity = {}".format(time_interval_days,confidence_interval*100,loss))
