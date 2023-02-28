#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 13 20:36:53 2023

@author: rid
"""
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from datetime import datetime

class preProcessing():
    
    def __init__(self, dataset, lookback):
        self.dataset = dataset
        self.lookback = lookback
        
      
    #loading the data
    def dataLoading(self, startDate='2023-02-16'):
        #filtering the target variable
        
    
        
        booleanCond=[]
        for i in self.dataset['Date']:
            i=datetime.date(i)
            if i<=datetime.date(datetime.strptime(startDate, '%Y-%m-%d')):
                booleanCond.append(True)
            else:
                booleanCond.append(False)
       
        self.dateTarget = self.dataset[booleanCond].Date
        
        self.closeTarget = self.dataset[booleanCond]['Close'].values
        
        self.closeTarget = self.closeTarget.reshape(len(self.closeTarget),1)
        
     
        return  self.closeTarget,  self.dateTarget
        
     #scaling the data   
    def dataScaling(self):
        #scaling the data
        self.closeScaling = self.dataLoading()[0]
        scaler = MinMaxScaler(feature_range=(0,1))
        self.closeScaling  = scaler.fit_transform(self.closeScaling)
        self.closeScaling = self.closeScaling.reshape(len(self.closeScaling))
        
        return scaler, self.closeScaling

    #windowing the data
    def windowGenerator(self):
        
        self.closeScaled= self.dataScaling()[1]
        trainFeature=[]
        trainTarget=[]
        
        for i in range(len(self.closeScaled)-self.lookback):
            val1 = self.closeScaled[i:(i+self.lookback)] 
            val2 = self.closeScaled[i+self.lookback] 
            trainFeature.append(val1)
            trainTarget.append(val2)
        trainFeature=np.array(trainFeature)
        trainFeature=trainFeature.reshape(trainFeature.shape[0],trainFeature.shape[1],1)
        trainTarget = np.array(trainTarget)
        
        
        return trainFeature, trainTarget
        

class updateScaler():
    
    def __init__(self, target, lookback):
        self.target = target
        self.lookback = lookback
     
    def dataScaling(self):
       
        self.target = self.target.reshape(len(self.target),1)
        
        scaler = MinMaxScaler(feature_range=(0,1))
        self.target  = scaler.fit_transform(self.target)
        self.target = self.target.reshape(len(self.target))
        
        
        return scaler, self.target
    
    def windowGenerator(self):
        
        self.target= self.dataScaling()[1]
        
        trainFeature=[]
        trainTarget=[]
        
      
        
        for i in range(len(self.target)-self.lookback):
            val1 = self.target[i:(i+self.lookback)] 
            val2 = self.target[i+self.lookback] 
            trainFeature.append(val1)
            trainTarget.append(val2)
        trainFeature=np.array(trainFeature)
        trainFeature=trainFeature.reshape(trainFeature.shape[0],trainFeature.shape[1],1)
        trainTarget = np.array(trainTarget)
        
        
        return trainFeature, trainTarget
    
    