#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 13 21:34:06 2023

@author: rid
"""

import stockpred.config.config as conf
import numpy as np
from sklearn.metrics import mean_absolute_error, mean_squared_error
from stockpred.scripts.preprocessingPipe import updateScaler

lookback=conf.lookback

epochs=conf.epochs

def fitter(train,target,model,epochs=epochs):
    model.fit(train,target,epochs=epochs)    
    return model


def futurePred(train,target,model,scaler,lookback=lookback):
    tempFeatures=[]
    tempFeatures.append(np.append(np.delete(train[-1], 0), target[-1]))
    tempFeatures=np.array(tempFeatures).reshape(1,lookback,1)
    temppred = model.predict(tempFeatures)
    temppred = scaler.inverse_transform(temppred)[0][0]
    return temppred


def updateData(train, target, realTarget, scaler, lookbackData,lookback=lookback):
    #realVal = np.array(realTarget[-1]).reshape(1,1)
    #realVal = scaler.transform(realVal)[0][0]
    
    target=np.array(target).reshape(len(target),1)
    target = scaler.inverse_transform(target).reshape(len(target))
    
    target=np.append(lookbackData, target)
    target = np.append(target,np.array(realTarget[-1]))

    #predFeatures=[]
    #predFeatures.append(np.append(np.delete(train[-1], 0), target[-1]))
    #predFeatures=np.array(predFeatures).reshape(1,lookback,1)
    #train = np.concatenate((train,predFeatures))
    scaler = updateScaler(target,lookback).dataScaling()[0] 
    train, target = updateScaler(target,lookback).windowGenerator()
    
    
    return train,target,scaler

def updatelongData(train, target, realTarget, longscaler, lookbackData,  lookback=lookback):
    target=np.array(target).reshape(len(target),1)
    target = longscaler.inverse_transform(target).reshape(len(target))
    target=np.append(lookbackData, target)
    target = np.append(target,np.array(realTarget[-1]))
    longscaler = updateScaler(target,lookback).dataScaling()[0] 
    train, target = updateScaler(target,lookback).windowGenerator()
    
    return train,target,longscaler
    


def dataReloaded(realVal,train,target,realTarget,predTarget,longpredTarget,model,longmodel,scaler,longscaler,lookbackData,lookback=lookback,epochs=epochs,longperiod=False):
    
    if realVal != None and longperiod==False:
        realTarget.append(realVal)
        
        train, target, newScaler = updateData(train,target,realTarget,scaler,  lookbackData, lookback=lookback)
        model = fitter(train,target,model,epochs=epochs)
        predTarget.append(futurePred(train,target,model,newScaler,lookback=lookback))
        
        return train, target, model, newScaler
    
    
    elif realVal == None and longperiod==True:
        
        
        longtrain, longtarget, longNewscaler = updatelongData(train,target,longpredTarget,longscaler, lookbackData, lookback=lookback)
        longmodel = fitter(longtrain,longtarget,longmodel,epochs=epochs)
        longpredTarget.append(futurePred(longtrain,longtarget,longmodel,longNewscaler,lookback=lookback))
        
        return longtrain, longtarget, longmodel, longNewscaler
    
    else:
        print('sorry no updates from the stock prices for today!')

def evaluationScore(trues,preds):
    mae = mean_absolute_error(trues,preds)
    rmse = np.sqrt(mean_squared_error(trues,preds))
    return mae, rmse


def longPred(period,longtrain,longtarget,realTarget,predTarget,longpredTarget,model,longmodel,scaler,longscaler, lookbackData, epochs=epochs, lookback=lookback):
    for i in range(period):
        longtrain, longtarget, longmodel, longscaler = dataReloaded(None,longtrain,longtarget,realTarget,predTarget,\
                        longpredTarget,model,longmodel,scaler,longscaler, lookbackData, lookback=lookback, epochs=epochs,longperiod=True)
        
 


