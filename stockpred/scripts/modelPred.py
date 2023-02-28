#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 16 21:50:12 2023

@author: rid
"""

from stockpred.scripts.LSTMmodel import LSTMmodelPipe
from datetime import timedelta
from stockpred.scripts.preprocessingPipe import preProcessing, updateScaler
from stockpred.scripts.dataLoader import dataFrame
import holidays
import datetime
from datetime import date
import numpy as np
from sklearn.metrics import mean_absolute_error, mean_squared_error
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px

import stockpred.config.config as conf
import plotly.io as pio
pio.renderers.default='browser'
import stockpred.scripts.modelFitting as mf

def date_by_adding_business_days(from_date, add_days):
    business_days_to_add = add_days
    current_date = from_date
    addDate=[]
    while business_days_to_add > 0:
        current_date += datetime.timedelta(days=1)
        weekday = current_date.weekday()
        if weekday >= 5: # sunday = 6
            continue
        addDate.append(current_date)
        business_days_to_add -= 1
    return addDate

def currentDate(from_date, add_days):
    business_days_to_add = add_days
    current_date = from_date
    while business_days_to_add > 0:
        current_date += datetime.timedelta(days=1)
        weekday = current_date.weekday()
        if weekday >= 5: # sunday = 6
            continue
        business_days_to_add -= 1
    return current_date



def changeModelFunc(newNeuron, newOptim, newLoss, newEpoch, newLook, target, history, scaler, lookbackData):  
    
    neuronsv2=newNeuron
    optimizerv2=newOptim
    lossv2=newLoss
    epochsv2=newEpoch
    lookbackv2=newLook
    lookbackDatav2 = np.array(history[:lookbackv2])
    
    modelv2  = LSTMmodelPipe(neuronsv2, optimizerv2, lossv2,(lookbackv2,1)).modelGenerator()
    predTargetv2=[]
    realTargetv2=[]
    
    
    targetv2=np.array(target).reshape(len(target),1)
    targetv2 = scaler.inverse_transform(targetv2).reshape(len(targetv2))
    targetv2=np.append(lookbackData, targetv2)
    scalerv2 = updateScaler(targetv2,lookbackv2).dataScaling()[0] 
    trainv2, targetv2 = updateScaler(targetv2,lookbackv2).windowGenerator()
    
 
    modelv2 = mf.fitter(trainv2,targetv2,modelv2, epochs=epochsv2)
    predTargetv2.append(mf.futurePred(trainv2,targetv2,modelv2,scalerv2,lookback=lookbackv2))
 
    return trainv2, targetv2, realTargetv2, predTargetv2, modelv2, scalerv2, lookbackDatav2, lookbackv2, epochsv2
    



def preloading(dataset,lookback = conf.lookback,code=conf.code, epochs=conf.epochs,\
               neurons=conf.neurons, loss=conf.loss, optimizer=conf.optimizer\
               ):
    
    
    
       
    lookback=lookback
    code=code
    epochs=epochs
    neurons=neurons
    loss=loss
    optimizer=optimizer
    
    
    
    preprocessor = preProcessing(dataset,lookback)
    history, historyDate = preprocessor.dataLoading()
    historyDate=list(historyDate)
    history = history[:,0]
    
    
    
    lookbackData = np.array(history[:lookback])
    scaler = preprocessor.dataScaling()[0]  
    train, target = preprocessor.windowGenerator()
    model  = LSTMmodelPipe(neurons, optimizer, loss,(train.shape[1],1)).modelGenerator()
    model.summary()
    
    mf.fitter(train,target,model)
    
    
    predTarget=[]
    realTarget=[]
    longpredTarget=[]
    longmodel=[]
    longscaler=[]
    
    predTarget.append(mf.futurePred(train,target,model,scaler,lookback=lookback))
  
    
    

    historyDeployed, historyDateDeployed = preprocessor.dataLoading(startDate=str(date.today()))
    historyDeployed = historyDeployed[:,0]
    realDataDeployed = historyDeployed[len(history):]
    dates = list(historyDateDeployed)[len(history):]
    
    for i in realDataDeployed:
        
        train, target, model, scaler =  \
        mf.dataReloaded(i,train,target,realTarget,predTarget,\
                        longpredTarget,model,longmodel,scaler,longscaler, lookbackData)
            
      
    history=historyDeployed
    historyDate=list(historyDateDeployed)
        
    
    return history, historyDate, train, target, realTarget, predTarget,\
        model, scaler, code, lookback, lookbackData, epochs, dates
    
    

    
    
    
def init(code, prevCode):
    if (code==prevCode) == False:
        dataset =  dataFrame(code)
        
        history, historyDate, train, target, realTarget, predTarget,\
            model, scaler, code, lookback, lookbackData, epochs, dates = preloading(dataset,code=code)
        
        longpredTarget=[]
        longmodel=[]
        longscaler=[]

    
        return dataset, history, historyDate, train, target, realTarget, predTarget,\
            model, scaler, lookback, lookbackData, epochs, dates, longpredTarget,\
                longmodel,longscaler
    
    
        
    
        


def realTimePred(globalPred, globalReal, code, changeModel, longPredInput, changelongPredMod, cancelModel, cancelLong, prevCode, \
                 dataset, history, historyDate, train, target, realTarget, predTarget,\
                     model, scaler, lookback, lookbackData, epochs, dates, longpredTarget,\
                         longmodel,longscaler,\
                    trainv2,targetv2,realTargetv2,predTargetv2,\
                                modelv2,scalerv2, lookbackDatav2,lookbackv2, epochsv2, longpredTargetFin ):
    
    try:
        dataset, history, historyDate, train, target, realTarget, predTarget,\
            model, scaler, lookback, lookbackData, epochs, dates, longpredTarget,\
                longmodel,longscaler = init(code, prevCode)
    except:
        pass
   
    
    
    if cancelModel==True:
        predTargetv2=[]
        trainv2,targetv2,realTargetv2,modelv2,scalerv2,lookbackDatav2,\
        lookbackv2, epochsv2 = 0,0,0,0,0,0,0,0
    if cancelLong==True:
        longpredTargetFin=[]
    
    else:
        
        preprocessor = preProcessing(dataset,lookback)
        historyUpdate, historyDateUpdate = preprocessor.dataLoading(startDate=str(date.today()))
        historyDateUpdate=list(historyDateUpdate)
        historyUpdate = historyUpdate[:,0]
        
        
        
        if len(history) == len(historyUpdate):
            updates='no'
            history=historyUpdate
            historyDate = historyDateUpdate
            
            
        else:
            updates='yes'
            history=historyUpdate
            historyDate = historyDateUpdate
            
           
    
        if changeModel==True:
            
            dead1, dead2, trainv2, targetv2, realTargetv2, predTargetv2,\
                modelv2, scalerv2, dead4, lookbackv2, lookbackDatav2, epochsv2, dead5 = preloading(dataset,code=code,lookback=4,epochs=3,neurons=4)
            
            changeModel=False
        
        
        
        if updates == 'yes':
            train, target, model, scaler =  \
            mf.dataReloaded(151,train,target,realTarget,predTarget,\
                            longpredTarget,model,longmodel,scaler,longscaler, lookbackData)
            dates.append(historyDateUpdate[-1])
            
            try:
                trainv2, targetv2, modelv2, scalerv2 =  \
                mf.dataReloaded(151,trainv2,targetv2,realTargetv2,predTargetv2,\
                                longpredTarget,modelv2,longmodel,scalerv2,longscaler, lookbackDatav2, lookback = lookbackv2, epochs=epochsv2)
            
            except:
                pass
            
            
        if longPredInput == True:
            longpredTarget=[]
            model = mf.fitter(train,target,model, epochs)
            longmodel=model
            longscaler=scaler
            longtrain, longtarget = train, target
            longPredInput=False
            
            if changelongPredMod == False:
               
                longpredTarget=[]
                model = mf.fitter(train,target,model, epochs)
                longmodel=model
                longscaler=scaler
                longtrain, longtarget = train, target
                longpredTarget.append(mf.futurePred(longtrain,longtarget,longmodel,longscaler,lookback=lookback))
    
                
                mf.longPred(3,longtrain,longtarget,realTarget,predTarget,\
                            longpredTarget,model,longmodel,scaler,longscaler,\
                                lookbackData)
                longpredTargetFin = longpredTarget 
            
            
            elif changelongPredMod == True:
                longtrainv3,longtargetv3, realTargetdead, longpredTarget,\
                    longmodelv3,longscalerv3,lookbackDatav3, lookbackv3, epochsv3 = \
                        changeModelFunc(8,conf.optimizer, conf.loss, 3, 4, target, history, scaler, lookbackData)
                
                mf.longPred(3,longtrainv3,longtargetv3,realTarget,predTarget,\
                            longpredTarget,model,longmodelv3,scaler,longscalerv3,\
                                lookbackDatav3, epochs=epochsv3, lookback=lookbackv3)
                
                longpredTargetFin = longpredTarget 
                changelongPredMod=False
        
           
        if updates == 'no':
              print('No updates yet!!')
        
    
    
   
    originalf1 = pd.DataFrame({'Class' : ['Previous (Before deployment)']*len(history),\
                             'Date' : list(historyDate),\
                             'Stock price' : history})
    originalf1['next_stock'] = originalf1['Stock price'].shift(periods=-1)
    originalf1['next_date'] = originalf1['Date'].shift(periods=-1)
    originalf1['difference'] = originalf1['next_stock'] - originalf1['Stock price'] 
    
         
        
    
    originalf2 = pd.DataFrame({'Class' : ['Current (After deployment)']*len(realTarget),\
                             'Date' : dates,\
                             'Stock price' : realTarget})
    originalf2['next_stock'] = 0
    originalf2['next_date'] = 0
    originalf2['difference'] = 0 
    
     
    
  
    preddf1 = pd.DataFrame({'Class' : ['Prediction (Deployed model)']*len(predTarget[:-1]),\
                             'Date' : dates,\
                             'Stock price' : predTarget[:-1]})
    preddf1['next_stock'] = preddf1['Stock price'].shift(periods=-1)
    preddf1['next_date'] = preddf1['Date'].shift(periods=-1)
    preddf1['difference'] =  preddf1['next_stock'] - preddf1['Stock price'] 
    
    
    try:
        preddf2 = pd.DataFrame({'Class' : ['Prediction (Your model)']*len(predTargetv2[:-1]),\
                                 'Date' : dates ,\
                                 'Stock price' : predTargetv2[:-1]})
        preddf2['next_date'] = 0
        preddf2['next_stock'] = 0
        preddf2['difference'] = 0
        
    except:
        predTargetv2=[]
        preddf2 = pd.DataFrame({'Class' : ['Prediction (Your model)']*len(predTargetv2[:-1]),\
                                 'Date' : [],\
                                 'Stock price' : predTargetv2[:-1]})
        preddf2['next_date'] = 0
        preddf2['next_stock'] = 0
        preddf2['difference'] = 0
            
        
    
    try:
        longpreddf = pd.DataFrame({'Class' : ['Long prediction']*len(longpredTargetFin),\
                                 'Date' : list(date_by_adding_business_days(dates[-1],  len(longpredTargetFin))),\
                                 'Stock price' : longpredTargetFin})
        longpreddf['next_date'] = longpreddf['Date'].shift(periods=-1)
        longpreddf['next_stock'] = longpreddf['Stock price'].shift(periods=-1)
        longpreddf['difference'] =  longpreddf['next_stock'] - longpreddf['Stock price']
    except:
        longpredTargetFin=[]
        longpreddf = pd.DataFrame({'Class' : ['Long prediction']*len(longpredTargetFin),\
                                 'Date' : list(date_by_adding_business_days(dates[-1],  len(longpredTargetFin))),\
                                 'Stock price' : longpredTargetFin})
        longpreddf['next_date'] = longpreddf['Date'].shift(periods=-1)
        longpreddf['next_stock'] = longpreddf['Stock price'].shift(periods=-1)
        longpreddf['difference'] =  longpreddf['next_stock'] - longpreddf['Stock price']
  
        
    
        
        
    
    final =  pd.concat([originalf1, originalf2, preddf1, preddf2, longpreddf])
    fig = px.line(final, x = 'Date', y = 'Stock price', color = 'Class',\
                  markers = True, \
                      title="Real time stock prediction of " + str(code),\
                          template='plotly_dark')
    
    
    posdiffBars = final[final['difference']>=0]
    negdiffBars = final[final['difference']<0]
    #fig2 = px.bar(final[final['difference']>=0], x="Date", y="difference" ,color_discrete_sequence =['green']*len(final[final['difference']>=0]),opacity=0.9,barmode='overlay',base='Stock price',width=[15]*len(final[final['difference']>=0]))
    #fig3 = px.bar(final[final['difference']<0], x="Date", y="difference",color_discrete_sequence =['red']*len(final[final['difference']<0]),opacity=0.9,barmode='overlay',base='Stock price',width=[15]*len(final[final['difference']<0]))
    
    fig2 = go.Bar( x=posdiffBars['Date'], y=posdiffBars["difference"] ,marker =dict(color='green'),opacity=0.25,base=posdiffBars['Stock price'])
    fig3 = go.Bar( x=negdiffBars['Date'], y=negdiffBars["difference"] ,marker =dict(color='red'),opacity=0.25,base=negdiffBars['Stock price'])
    
    fig.add_trace(fig2)
    fig.add_trace(fig3)    

    

    
    
    fig.update_layout(font_color='white',\
                          title_font_color='white',\
                    font=dict(family='Franklin Gothic', size=22))
    
     
        

    
    
    #fig.show()

    globalPred+=predTarget[:-1]
    globalReal+=realTarget

    #print("Total RMSE after deployment: ", mf.evaluationScore(globalReal, globalPred))
    #print("Inbuilt model's RMSE: ", mf.evaluationScore(np.array(realTarget), np.array(predTarget[:-1])))
    #print("Your model's RMSE: ", mf.evaluationScore(np.array(realTarget), np.array(predTargetv2[:-1])))
    
    rmseGlobal = mf.evaluationScore(globalReal, globalPred)
    rmseModel = mf.evaluationScore(np.array(realTarget), np.array(predTarget[:-1]))
 
    
    if predTargetv2[:-1]:
        rmseNew = mf.evaluationScore(np.array(realTarget), np.array(predTargetv2[:-1]))
    else:
        rmseNew=0
    
    prevCode=code
    
    
    
    
    return fig, rmseGlobal, rmseModel, rmseNew, prevCode, \
            dataset, history, historyDate, train, target, realTarget, predTarget,\
                model, scaler, lookback, lookbackData, epochs, dates, longpredTarget,\
                    longmodel,longscaler,\
                    trainv2,targetv2,realTargetv2,predTargetv2,\
                                modelv2,scalerv2, lookbackDatav2,lookbackv2, epochsv2,\
                                    globalPred, globalReal, longpredTargetFin
    
  
  







