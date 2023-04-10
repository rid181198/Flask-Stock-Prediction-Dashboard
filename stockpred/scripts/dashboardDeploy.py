

import stockpred.scripts.modelPred as mp
import stockpred.scripts.dashboardDeploy as dashappdep
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
                changelongPredMod, cancelModel, cancelLong, newLookback, newEpoch, newNeuron, newLoss, newOptimizer,\
                    newLongLookback, newLongEpoch, newLongNeuron, newLongLoss, newLongOptimizer, numDays):
    
    
    
    fig, rmseGlobal, rmseModel, rmseNew, newCode, \
    dataset, history, historyDate, train, target, realTarget, predTarget,\
    model, scaler, lookback, lookbackData, epochs, dates, longpredTarget,\
    longmodel,longscaler,trainv2,targetv2,realTargetv2,predTargetv2,\
    modelv2,scalerv2,lookbackDatav2,lookbackv2, epochsv2,globalPred, globalReal, longpredTargetFin, final=\
    mp.realTimePred(dashappdep.globalPred, dashappdep.globalReal, code, changeModel, longPredInput,\
    changelongPredMod, cancelModel, cancelLong, dashappdep.prevCode, \
    dashappdep.dataset, dashappdep.history, dashappdep.historyDate, dashappdep.train, dashappdep.target, dashappdep.realTarget, dashappdep.predTarget,\
    dashappdep.model, dashappdep.scaler, dashappdep.lookback, dashappdep.lookbackData, dashappdep.epochs, dashappdep.dates, dashappdep.longpredTarget,\
    dashappdep.longmodel,dashappdep.longscaler,
    dashappdep.trainv2,dashappdep.targetv2,dashappdep.realTargetv2,dashappdep.predTargetv2,\
    dashappdep.modelv2,dashappdep.scalerv2,\
    dashappdep.lookbackDatav2,dashappdep.lookbackv2, dashappdep.epochsv2, dashappdep.longpredTargetFin,\
        newLookback, newEpoch, newNeuron, newLoss, newOptimizer,\
            newLongLookback, newLongEpoch, newLongNeuron, newLongLoss, newLongOptimizer, numDays)
        
  
    
    
    dashappdep.prevCode = newCode
    dashappdep.dataset, dashappdep.history, dashappdep.historyDate, dashappdep.train, dashappdep.target, dashappdep.realTarget, dashappdep.predTarget,\
    dashappdep.model, dashappdep.scaler, dashappdep.lookback, dashappdep.lookbackData, dashappdep.epochs, dashappdep.dates, dashappdep.longpredTarget,\
    dashappdep.longmodel,dashappdep.longscaler = dataset, history, historyDate, train, target, realTarget, predTarget,\
    model, scaler, lookback, lookbackData, epochs, dates, longpredTarget,longmodel,longscaler
                    
    dashappdep.trainv2,dashappdep.targetv2,dashappdep.realTargetv2,dashappdep.predTargetv2,\
    dashappdep.modelv2,dashappdep.scalerv2,dashappdep.lookbackDatav2,dashappdep.lookbackv2, dashappdep.epochsv2=\
    trainv2,targetv2,realTargetv2,predTargetv2,modelv2,scalerv2,lookbackDatav2,lookbackv2, epochsv2
    
    dashappdep.globalPred, dashappdep.globalReal, dashappdep.longpredTargetFin= globalPred, globalReal, longpredTargetFin
  
    return fig, rmseGlobal,\
        rmseModel,\
           rmseNew, final






