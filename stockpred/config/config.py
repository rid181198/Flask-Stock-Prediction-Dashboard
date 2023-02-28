#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 15 21:11:48 2023

@author: rid
"""

from tensorflow.keras.optimizers.legacy import Adam

lookback=2
code='AAPL'
epochs=3
neurons=4
loss='mean_squared_error'
optimizer=Adam()



