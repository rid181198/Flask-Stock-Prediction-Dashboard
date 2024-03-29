

import stockpred.scripts.modelPred as mp
import pandas as pd
from datetime import timedelta
from datetime import date
import json

def updates(globalPred, globalReal, prevCode, dataset, history, historyDate, train, target, realTarget,\
        predTarget, model, scaler, lookback, lookbackData, epochs, dates, longpredTarget,\
        longmodel,longscaler,\
    trainv2,targetv2,realTargetv2,predTargetv2,\
    modelv2,scalerv2,lookbackDatav2,lookbackv2, epochsv2, longpredTargetFin,\
        code, changeModel, longPredInput,\
                changelongPredMod, cancelModel, cancelLong, newLookback, newEpoch, newNeuron, newLoss, newOptimizer,\
                    newLongLookback, newLongEpoch, newLongNeuron, newLongLoss, newLongOptimizer, numDays):
    
    
    
    fig, rmseGlobal, rmseModel, rmseNew, newCode, \
    dataset, history, historyDate, train, target, realTarget, predTarget,\
    model, scaler, lookback, lookbackData, epochs, dates, longpredTarget,\
    longmodel,longscaler,trainv2,targetv2,realTargetv2,predTargetv2,\
    modelv2,scalerv2,lookbackDatav2,lookbackv2, epochsv2,globalPred, globalReal, longpredTargetFin, final=\
    mp.realTimePred(globalPred, globalReal, code, changeModel, longPredInput,\
    changelongPredMod, cancelModel, cancelLong, prevCode, \
    dataset, history, historyDate, train, target, realTarget, predTarget,\
    model, scaler, lookback, lookbackData, epochs, dates, longpredTarget,\
    longmodel,longscaler,trainv2,targetv2,realTargetv2,predTargetv2,\
    modelv2,scalerv2,lookbackDatav2,lookbackv2, epochsv2,longpredTargetFin,\
        newLookback, newEpoch, newNeuron, newLoss, newOptimizer,\
            newLongLookback, newLongEpoch, newLongNeuron, newLongLoss, newLongOptimizer, numDays)
        
#[date.strftime('%Y-%m-%d') for date in historyDate]  
    
    variables = {'rmseGlobal': rmseGlobal,
           'rmseModel': rmseModel,
           'rmseNew': rmseNew,
           'prevCode': newCode,
           'dataset': dataset,
           'history': history,
           'historyDate': historyDate,
           'train': train,
           'target': target,
           'realTarget': realTarget,
           'predTarget': predTarget,
           'model': model,
           'scaler': scaler,
           'lookback': lookback,
           'lookbackData': lookbackData,
           'epochs': epochs,
           'dates': dates,
           'longpredTarget': longpredTarget,
           'longmodel': longmodel,
           'longscaler': longscaler,
           'trainv2': trainv2,
           'targetv2': targetv2,
           'realTargetv2': realTargetv2,
           'predTargetv2': predTargetv2,
           'modelv2': modelv2,
           'scalerv2': scalerv2,
           'lookbackDatav2': lookbackDatav2,
           'lookbackv2': lookbackv2,
           'epochsv2': epochsv2,
           'globalPred': globalPred,
           'globalReal': globalReal,
           'longpredTargetFin': longpredTargetFin,
           'final': final}

    

    return fig, variables




