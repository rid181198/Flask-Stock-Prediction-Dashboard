from flask import Flask, render_template, url_for, flash
from stockpred import app
import pandas as pd
import json
import stockpred.scripts.dashboard as dash
import plotly

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

 
@app.route('/dashboard')
def dashboard_page():
    #fig, globalerror, modelerror, newerror = dash.updates('AAPL', False, False,False,False,False)
    # Create graphJSON
    #graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
     
    #return render_template('dashboard.html', graphJSON=graphJSON)
    return render_template('dashboard.html')
