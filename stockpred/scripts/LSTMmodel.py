#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 13 20:57:36 2023

@author: rid
"""

#from preprocessingPipe import preProcessing
#from dataLoader import dataFrame
from keras.models import Sequential
from keras.layers import Dense, LSTM, Input
#from tensorflow.keras.optimizers.legacy import Adam



class LSTMmodelPipe():
    
    def __init__(self, neurons, optimizer, loss, input_shape):
        self.neurons = neurons
        self.optimizer = optimizer
        self.loss = loss
        self.input_shape = input_shape
        
    def modelGenerator(self):
        self.model = Sequential()
        self.model.add(Input(shape=self.input_shape))  # Replace time_steps and features with your values
        self.model.add(LSTM(self.neurons, return_sequences=True))
        self.model.add(LSTM(self.neurons, return_sequences=False))
        self.model.add(Dense(int(self.neurons / 2)))
        self.model.add(Dense(1))
        
        self.model.compile(optimizer= self.optimizer, loss=self.loss)
        print("wowww")
        print(self.model)
        return self.model
