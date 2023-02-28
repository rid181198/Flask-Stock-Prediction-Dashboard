

import stockpred.scripts.modelPred as mp
import stockpred.scripts.dashboard as dashapp
from datetime import timedelta

from datetime import date


    
    
    
    
    
globalPred = []
globalReal = []
prevCode=''
dataset, history, historyDate, train, target, realTarget, predTarget,\
    model, scaler, lookback, lookbackData, epochs, dates, longpredTarget,\
        longmodel,longscaler = 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
        
trainv2,targetv2,realTargetv2,predTargetv2,\
            modelv2,scalerv2,\
                lookbackDatav2,lookbackv2, epochsv2 = 0,0,0,0,0,0,0,0,0
longpredTargetFin=0

 


def updates(code, changeModel, longPredInput,\
                changelongPredMod, cancelModel, cancelLong):
    
    
    
    fig, rmseGlobal, rmseModel, rmseNew, newCode, \
    dataset, history, historyDate, train, target, realTarget, predTarget,\
    model, scaler, lookback, lookbackData, epochs, dates, longpredTarget,\
    longmodel,longscaler,trainv2,targetv2,realTargetv2,predTargetv2,\
    modelv2,scalerv2,lookbackDatav2,lookbackv2, epochsv2,globalPred, globalReal, longpredTargetFin=\
    mp.realTimePred(dashapp.globalPred, dashapp.globalReal, code, changeModel, longPredInput,\
    changelongPredMod, cancelModel, cancelLong, dashapp.prevCode, \
    dashapp.dataset, dashapp.history, dashapp.historyDate, dashapp.train, dashapp.target, dashapp.realTarget, dashapp.predTarget,\
    dashapp.model, dashapp.scaler, dashapp.lookback, dashapp.lookbackData, dashapp.epochs, dashapp.dates, dashapp.longpredTarget,\
    dashapp.longmodel,dashapp.longscaler,
    dashapp.trainv2,dashapp.targetv2,dashapp.realTargetv2,dashapp.predTargetv2,\
    dashapp.modelv2,dashapp.scalerv2,\
    dashapp.lookbackDatav2,dashapp.lookbackv2, dashapp.epochsv2, dashapp.longpredTargetFin)
        
  
    
    
    dashapp.prevCode = newCode
    dashapp.dataset, dashapp.history, dashapp.historyDate, dashapp.train, dashapp.target, dashapp.realTarget, dashapp.predTarget,\
    dashapp.model, dashapp.scaler, dashapp.lookback, dashapp.lookbackData, dashapp.epochs, dashapp.dates, dashapp.longpredTarget,\
    dashapp.longmodel,dashapp.longscaler = dataset, history, historyDate, train, target, realTarget, predTarget,\
    model, scaler, lookback, lookbackData, epochs, dates, longpredTarget,longmodel,longscaler
                    
    dashapp.trainv2,dashapp.targetv2,dashapp.realTargetv2,dashapp.predTargetv2,\
    dashapp.modelv2,dashapp.scalerv2,dashapp.lookbackDatav2,dashapp.lookbackv2, dashapp.epochsv2=\
    trainv2,targetv2,realTargetv2,predTargetv2,modelv2,scalerv2,lookbackDatav2,lookbackv2, epochsv2
    
    dashapp.globalPred, dashapp.globalReal, dashapp.longpredTargetFin= globalPred, globalReal, longpredTargetFin
  
    return fig, 'Global RMSE: {}'.format(rmseGlobal),\
        'Inbuilt model RMSE: {}'.format(rmseModel),\
            'New model RMSE: {}'.format(rmseNew)






