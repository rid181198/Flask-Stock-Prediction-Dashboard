#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 12 21:28:03 2023

@author: rid
"""


import numpy as np
import pandas as pd
from pandas_datareader import data
import matplotlib.pyplot as plt
import yfinance as yf
from datetime import date
import tensorflow as tf
from tensorflow.keras.optimizers.legacy import Adam
import yfinance as yf
today = str(date.today())


# download dataframe and stock data
def dataFrame(code):
    tickerData = yf.download(tickers = code,  # list of tickers
                period = "max",         # time period
                interval = "1d",       # trading interval
                ignore_tz = True,      # ignore timezone when aligning data from different exchanges?
                prepost = False) 
    tickerData = tickerData.reset_index()
    tickerData['Date'] = pd.to_datetime(tickerData['Date'])
    
    return tickerData








