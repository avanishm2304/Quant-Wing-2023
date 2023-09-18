# -*- coding: utf-8 -*-
"""
Created on Sat Sep  9 05:10:41 2023

@author: Avanish Mohgaonkar
"""

import yfinance as yf
import pandas as pd
import numpy as np
import copy
import matplotlib.pyplot as plt
ticker = "TATASTEEL.NS"
stock_data = pd.DataFrame()
stock_data = yf.download(ticker,period="2y",interval ="1d")
stock_data.dropna(how="any",inplace=True)
def MACD(DF, a=12 ,b=26, c=9):
    
    df = DF.copy()
    df["ma_fast"] = df["Adj Close"].ewm(span=a, min_periods=a).mean()
    df["ma_slow"] = df["Adj Close"].ewm(span=b, min_periods=b).mean()
    df["macd"] = df["ma_fast"] - df["ma_slow"]
    df["signal"] = df["macd"].ewm(span=c, min_periods=c).mean()
    return df.loc[:,["macd","signal"]]

def ATR(DF, n=14):
    df = DF.copy()
    df["H-L"] = df["High"] - df["Low"]
    df["H-PC"] = abs(df["High"] - df["Adj Close"].shift(1))
    df["L-PC"] = abs(df["Low"] - df["Adj Close"].shift(1))
    df["TR"] = df[["H-L","H-PC","L-PC"]].max(axis=1, skipna=False)
    df["ATR"] = df["TR"].ewm(com=n, min_periods=n).mean()
    return df["ATR"]

def ADX(DF, n=14):
    df = DF.copy()
    df["ATR"] = ATR(DF, n)
    df["upmove"] = df["High"] - df["High"].shift(1)
    df["downmove"] = df["Low"].shift(1) - df["Low"]
    df["+dm"] = np.where((df["upmove"]>df["downmove"]) & (df["upmove"] >0), df["upmove"], 0)
    df["-dm"] = np.where((df["downmove"]>df["upmove"]) & (df["downmove"] >0), df["downmove"], 0)
    df["+di"] = 100 * (df["+dm"]/df["ATR"]).ewm(alpha=1/n, min_periods=n).mean()
    df["-di"] = 100 * (df["-dm"]/df["ATR"]).ewm(alpha=1/n, min_periods=n).mean()
    df["ADX"] = 100* abs((df["+di"] - df["-di"])/(df["+di"] + df["-di"])).ewm(alpha=1/n, min_periods=n).mean()
    return df.loc[:,["+di","-di","ADX"]]
def CAGR(DF):
    df = DF.copy()
    df["cum_return"] = (1 + df["returns"]).cumprod()
    n = len(df)/(252)
    CAGR = (df["cum_return"].tolist()[-1])**(1/n) - 1
    return CAGR

signal=""
strat_df= copy.deepcopy(stock_data)
return_val=[0]
strat_df[["macd","signal"]]= MACD(strat_df)
strat_df[["+di","-di","ADX"]]=ADX(strat_df)
strat_df.dropna(how="any",inplace=True)
print("calculating returns for ",ticker)
for i in range(1,len(strat_df)):
    if signal=="":
        return_val.append(0)
        if ((strat_df["macd"][i]-strat_df["signal"][i]>0) and (strat_df["+di"][i]>strat_df["-di"][i]) and (strat_df["ADX"][i]>25)):
            signal="buy"
        elif ((strat_df["macd"][i]-strat_df["signal"][i]<0) and (strat_df["+di"][i]<strat_df["-di"][i]) and (strat_df["ADX"][i]>25)):
            signal="sell"
    elif signal=="buy":
        if ((strat_df["Low"][i]<strat_df["Low"][i-1]) and (strat_df["ADX"][i]<25)):
            return_val.append((strat_df["Low"][i-1])/(strat_df["Adj Close"][i-1])-1)
            signal=""
        elif ((strat_df["macd"][i]-strat_df["signal"][i]<0) and (strat_df["+di"][i]<strat_df["-di"][i]) and (strat_df["ADX"][i]>25)):
            return_val.append((strat_df["Adj Close"][i])/(strat_df["Adj Close"][i-1])-1)
            signal ="sell"
        else:
            return_val.append((strat_df["Adj Close"][i])/(strat_df["Adj Close"][i-1])-1)
    elif signal =="sell":
        if ((strat_df["High"][i]>strat_df["High"][i-1]) and (strat_df["ADX"][i]<25)):
            return_val.append((strat_df["Adj Close"][i-1])/(strat_df["High"][i-1])-1)
            signal=""
        elif ((strat_df["macd"][i]-strat_df["signal"][i]>0) and (strat_df["+di"][i]>strat_df["-di"][i]) and (strat_df["ADX"][i]>25)):
            return_val.append((strat_df["Adj Close"][i-1])/(strat_df["Adj Close"][i])-1)
            signal="buy"
        else:
            return_val.append((strat_df["Adj Close"][i-1])/(strat_df["Adj Close"][i])-1)
strat_df["returns"]= np.array(return_val)
strat_df.reset_index(inplace=True)
fig = plt.figure(figsize=(10,4))
ax = fig.add_axes([0,0,0.8,0.8])
ax.plot(strat_df["Date"],(1+strat_df["returns"]),'r')
ax.set_xlabel("date")
ax.set_ylabel("returns")
ax.set_title("returns")
plt.show()
print("total returns at the end of 2 years: {}%".format((((1+strat_df["returns"]).cumprod().iloc[-1])-1)*100))
print("Compounded annual growth rate(or return):{}%".format(CAGR(strat_df)*100))       

            