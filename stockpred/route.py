from flask import Flask, request, render_template, url_for, flash
from stockpred import app
import pandas as pd
import json
import stockpred.scripts.dashboard as dash
import plotly
from stockpred.forms.dashform import DashFormNewModel, DashFormNewLongModel, generalInputs
from tensorflow.keras.optimizers.legacy import Adam, SGD, RMSprop

@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')

@app.route('/register')
def register_page():
    return render_template('register.html')

@app.route('/login')
def login_page():
    return render_template('login.html')

 
@app.route('/dashboard', methods=['GET','POST'])
def dashboard_page():
    changeModel=False
    changelongPredMod=False
    longPredInput=False
    cancelModel=False
    cancelLong=False
    newLookback, newEpoch, newNeuron, newLoss, newOptimizer,\
                    newLongLookback, newLongEpoch, newLongNeuron, newLongLoss, newLongOptimizer, numDays = 0,0,0,0,0,0,0,0,0,0,0

    form1 = DashFormNewModel()
    form2 = DashFormNewLongModel()
    form0 = generalInputs()

    
        #code=form0.code.data

    if form0.validate_on_submit():
        if form0.cancelmodel.data:
            cancelModel = True
            cancelLong=True
            longPredInput=True
            numDays = form0.numdays.data

    if form1.validate_on_submit():
        if form1.submitmodel.data:
            changeModel=True
            newLookback = form1.newLookback.data
            newEpoch = form1.newEpoch.data
            newNeuron = form1.newNeuron.data
            newLoss = form1.newLoss.data
            newOptimizer = form1.newOptimizer.data
            if newOptimizer == 'Adam':
                newOptimizer = Adam()
            if newOptimizer == 'SGD':
                newOptimizer = SGD()
            if newOptimizer == 'RMSprop':
                newOptimizer = RMSprop()

    if form2.validate_on_submit():
        if form2.submitmodel.data:
            changelongPredMod =True
            newLongLookback = form2.newLookback.data
            newLongEpoch = form2.newEpoch.data
            newLongNeuron = form2.newNeuron.data
            newLongLoss = form2.newLoss.data
            newLongOptimizer = form2.newOptimizer.data
            if newLongOptimizer == 'Adam':
                newLongOptimizer = Adam()
            if newLongOptimizer == 'SGD':
                newLongOptimizer = SGD()
            if newLongOptimizer == 'RMSprop':
                newLongOptimizer = RMSprop()


    code='AAPL'
    fig, globalerror, modelerror, newerror = dash.updates(code, changeModel, longPredInput,\
                changelongPredMod, cancelModel, cancelLong, newLookback, newEpoch, newNeuron, newLoss, newOptimizer,\
                    newLongLookback, newLongEpoch, newLongNeuron, newLongLoss, newLongOptimizer, numDays)
    #Create graphJSON
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template('dashboard.html', form1=form1, form2=form2, form0=form0, graphJSON=graphJSON)
