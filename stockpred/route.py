from flask import Flask, request, render_template, url_for, flash, session
from stockpred import app
import pandas as pd
import json
import stockpred.scripts.dashboard as dash
import plotly
import plotly.express as px
from stockpred.forms.dashform import DashFormNewModel, DashFormNewLongModel, generalInputs, cancelForm, longpredForm
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


@app.before_first_request
def clear_session():
    session.clear()
    session['code'] = ''
@app.route('/dashboard', methods=['GET','POST'])
def dashboard_page():
    changeModel=False
    changelongPredMod=False
    longPredInput=False
    cancelModel=False
    cancelLong=False 
    newLookback, newEpoch, newNeuron, newLoss, newOptimizer,\
                    newLongLookback, newLongEpoch, newLongNeuron, newLongLoss, newLongOptimizer, numDays = 0,0,0,0,0,0,0,0,0,0,0

    form0 = generalInputs()
    form1 = DashFormNewModel()
    form2 = DashFormNewLongModel()
    form3=cancelForm()
    form4 = longpredForm()
    
    if form0.validate_on_submit():
        session['code'] = form0.code.data
        code=form0.code.data
    elif 'code' in session:
        form0.code.data = session['code']
        code=session['code']

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

    if form4.validate_on_submit():
        numDays = form4.numdays.data
        longPredInput = True

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

    if form3.validate_on_submit():
        if form3.cancelmodel.data:
            cancelModel = True
        if form3.cancellongmodel.data:
            cancelLong=True


    if code:
        fig, globalerror, modelerror, newerror = dash.updates(code, changeModel, longPredInput,\
                    changelongPredMod, cancelModel, cancelLong, newLookback, newEpoch, newNeuron, newLoss, newOptimizer,\
                        newLongLookback, newLongEpoch, newLongNeuron, newLongLoss, newLongOptimizer, numDays)
        #Create graphJSON
        graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        return render_template('dashboard.html',  form0=form0, form1=form1, form2=form2, form3 = form3, form4 = form4, graphJSON=graphJSON)

    #else:
    #    fig = px.line(template='plotly_dark')
    #    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    #    flash(f"Please enter the code", category='danger')
    return render_template('dashboard.html',  form0=form0, form1=form1, form2=form2, form3 = form3, form4 = form4)
