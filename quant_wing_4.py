# -*- coding: utf-8 -*-
"""
Created on Sun Nov  5 11:23:26 2023

@author: Avanish Mohgaonkar
"""

import yfinance as yf
import pandas as pd

tickers = ["APOLLOHOSP.NS","EICHERMOT.NS","ADANIPORTS.NS","TITAN.NS","LTIM.NS","ONGC.NS","JSWSTEEL.NS","TATAMOTORS.NS","ICICIBANK.NS","TECHM.NS","INFY.NS","HEROMOTOCO.NS","SBIN.NS","COALINDIA.NS","BAJAJ-AUTO.NS","HINDUNILVR.NS","SUNPHARMA.NS","ASIANPAINT.NS","BHARTIARTL.NS","UPL.NS"]
ohlcv={}
return_df = pd.DataFrame()
for ticker in tickers:
    ohlcv[ticker]= yf.download(ticker,period="5y",interval="1d")
    ohlcv[ticker].dropna(how="any",inplace = True)
    ohlcv[ticker]["returns"]= ohlcv[ticker]["Adj Close"].pct_change()
    ohlcv[ticker].dropna(how="any",inplace = True)
    return_df[ticker]= ohlcv[ticker]["returns"]
matrix = pd.DataFrame()
matrix = return_df.corr()
def get_key(val):
   
    for key, value in dict1.items():
        if val == value:
            return key
 
    return "key doesn't exist" 

"""matrix.loc["APOLLOHOSP.NS"].sort_values(ascending=False)[:2].index.values.tolist()[1]"""
'''for ticker in matrix:
    ticker_2 = matrix.loc[ticker].sort_values(ascending=False)[:2].index.values.tolist()[1]
    x1 = matrix[ticker].loc[ticker].mean()
    x2 = matrix[ticker].loc[ticker_2].mean()
    if(x1>x2):
        matrix.drop(ticker,inplace = True)
        matrix.drop(ticker,axis=1,inplace = True)
    if(x2>x1):
        matrix.drop(ticker_2,inplace = True)
        matrix.drop(ticker_2,axis=1,inplace = True)'''
"""dict={}
dict2={}
for ticker in matrix:
    
    dict2[ticker]= matrix.loc[ticker].mean()
        
list2= list(dict2.values())
list2.sort()
list3= list2[:5]
for i in range(5):
    name = get_key(list3[i])
    dict[name]= list3[i]
portfolio = list(dict.keys())
print("most uncorrelated stocks are:",portfolio)"""

dict1={}
for ticker in matrix:
    list1 = matrix.loc[ticker].sort_values(ascending = True)[:5].index.values.tolist()
    for i in range(5):
        dict1[(ticker,list1[i])]= matrix.loc[ticker].sort_values(ascending= True)[i]
       
list3= list(dict1.values())       
list3.sort()
list4 = list3[:10]
names=[]
for i in range(0,10,2):
    names.append(get_key(list4[i]))
ticker_list=[]
for i in names:
    n1,n2= i
    if n1 not in ticker_list:
        ticker_list.append(n1)
    if n2 not in ticker_list:
        ticker_list.append(n2)
print("final list of portfolio:",ticker_list)



    
    
    
    
    
    
    
    
        
        
    
    
        
        
    
        
    
    
