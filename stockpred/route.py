from flask import Flask, request, render_template, url_for, flash, session, redirect, make_response
from stockpred import app
import pandas as pd
import json
import stockpred.scripts.dashboard as dash
import stockpred.scripts.dashboardDeploy as dashdep
import plotly
import plotly.express as px
from stockpred.forms.dashform import DashFormNewModel, DashFormNewLongModel, generalInputs, cancelForm, longpredForm, DownloadForm, StopDeploy
from stockpred.forms.user import RegisterForm, LoginForm
from stockpred.models.register import User, Userdata
from tensorflow.keras.optimizers.legacy import Adam, SGD, RMSprop
from flask_login import login_user, logout_user, login_required, current_user
from stockpred import db
import uuid
import time
import io
from apscheduler.schedulers.background import BackgroundScheduler


@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')



@app.before_first_request
def clear_session():
    session.clear()
    session['code'] = ''
    
@app.route('/dashboard', methods=['GET','POST'])
def dashboard_page():
    global code, changeModel, longPredInput,\
        changelongPredMod, cancelModel, cancelLong, newLookback, newEpoch, newNeuron, newLoss, newOptimizer,\
        newLongLookback, newLongEpoch, newLongNeuron, newLongLoss, newLongOptimizer, numDays, fig, globalerror, modelerror, newerror, final

    changeModel=False
    changelongPredMod=False
    longPredInput=False
    cancelModel=False
    cancelLong=False 
    session['form1_clicked']=False
    session['form2_clicked']=False
    session['form4_clicked']=False
    newLookback, newEpoch, newNeuron, newLoss, newOptimizer,\
                    newLongLookback, newLongEpoch, newLongNeuron, newLongLoss, newLongOptimizer, numDays = 0,0,0,0,0,0,0,0,0,0,0

    form0 = generalInputs()
    form1 = DashFormNewModel()
    form2 = DashFormNewLongModel()
    form3=cancelForm()
    form4 = longpredForm()
    form5 = DownloadForm()
    
    if form0.validate_on_submit():
        session['code'] = form0.code.data
        code=form0.code.data
    elif 'code' in session:
        form0.code.data = session['code']
        code=session['code']

    if request.method == 'POST':
        if request.form.get('form1button1'):
            session['form1_clicked'] = True
        if request.form.get('form2button1'):
            session['form2_clicked'] = True
        if request.form.get('form4button1'):
            session['form4_clicked'] = True

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
        if form1.submitmodel.data and len(code) == 0 :
            flash("Please enter the code first and run the prediction model!", category='danger') 


  
    form1errors=[]
    for err_msg in form1.errors.values():
        form1errors.append(err_msg)


    if form4.validate_on_submit():
        if form4.longprediction.data:
            numDays = form4.numdays.data
            longPredInput = True
        if form4.longprediction.data and len(code) == 0 :
            flash("Please enter the code first and run the prediction model!", category='danger') 

    form4errors=[]
    for err_msg in form4.errors.values():
        form4errors.append(err_msg)


    if form2.validate_on_submit():
        if form2.submitmodel2.data:
            changelongPredMod =True
            newLongLookback = form2.newLookback2.data
            newLongEpoch = form2.newEpoch2.data
            newLongNeuron = form2.newNeuron2.data
            newLongLoss = form2.newLoss2.data
            newLongOptimizer = form2.newOptimizer2.data
            if newLongOptimizer == 'Adam':
                newLongOptimizer = Adam()
            if newLongOptimizer == 'SGD':
                newLongOptimizer = SGD()
            if newLongOptimizer == 'RMSprop':
                newLongOptimizer = RMSprop()
        if form2.submitmodel2.data and len(code) == 0 :
            flash("Please enter the code first and run the prediction model!", category='danger') 
    form2errors=[]
    for err_msg in form2.errors.values():
        form2errors.append(err_msg)


    if form3.validate_on_submit():
        if form3.cancelmodel.data:
            if session['code']:
                cancelModel = True
            else:
                flash("Please enter the code first and run the prediction model!", category='danger')

        if form3.cancellongmodel.data:
            if session['code']:
                cancelLong=True
            else:
                flash("Please enter the code first and run the prediction model!", category='danger')


    if code:
        try:
            fig, globalerror, modelerror, newerror, final = dash.updates(code, changeModel, longPredInput,\
                        changelongPredMod, cancelModel, cancelLong, newLookback, newEpoch, newNeuron, newLoss, newOptimizer,\
                            newLongLookback, newLongEpoch, newLongNeuron, newLongLoss, newLongOptimizer, numDays)
            #Create graphJSON
            graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
            errorsDict = {'globalerror': globalerror, 'modelerror': modelerror, 'newerror': newerror, 'final': final}
          
            if form5.validate_on_submit():
                if form5.download.data:
                    response = make_response(final.to_csv(index=False))
                    response.headers.set('Content-Disposition', 'attachment', filename='final.csv')
                    response.headers.set('Content-Type', 'text/csv')
                    return response
        
            return render_template('dashboard.html',  form0=form0, form1=form1,form1errors=form1errors, form2=form2,\
                                   form2errors=form2errors, form3 = form3, form4 = form4,\
                                     form4errors=form4errors, form5=form5, graphJSON=graphJSON, errorsDict = errorsDict, code=code)
        except:
            flash('You have entered the wrong code! Please look at the meta data guide in the settings.', category='danger')
            return redirect(url_for('dashboard_page'))
        
    else:
        errorsDict = {'globalerror': 0, 'modelerror': 0, 'newerror': 0, 'final': pd.DataFrame()}
        if form5.validate_on_submit():
            if form5.download.data:
               flash('You have not entered the code! No data at the moment.', category='danger') 

    #else:
    #    fig = px.line(template='plotly_dark')
    #    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    #    flash(f"Please enter the code", category='danger')
    return render_template('dashboard.html',  form0=form0, form1=form1, form1errors=form1errors,\
                            form2=form2,form2errors=form2errors,form3 = form3, form4 = form4,form4errors=form4errors, form5=form5, errorsDict = errorsDict)




@app.route('/register', methods=['GET','POST'])
def register_page():
    form0 = RegisterForm()
    if form0.validate_on_submit():
        user_to_create = User(username = form0.username.data,
                              email_address = form0.email_address.data,
                              password = form0.password1.data)
        
        db.session.add(user_to_create)
        db.session.commit()
        login_user(user_to_create)
        flash(f"Account created successfully! You are now logged in as {user_to_create.username} and use the dashboard.", category='success')
        return redirect(url_for('dashboard_page'))
    if form0.errors != {}:
        for err_msg in form0.errors.values():
            flash(f"There was an error with creating a user: {err_msg}", category = 'danger')
    return render_template('register.html', form0 = form0)

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(email_address = form.email_address.data).first()
        if attempted_user and attempted_user.check_password(attempted_password = form.password.data):
            login_user(attempted_user)
            flash(f'Success! You are logged in as: {attempted_user.username}', category='success')
            return redirect(url_for('dashboard_page'))
        else:
            flash('Username and password are not match! Please try again', category='danger')
    return render_template('login.html', form=form)

@app.route('/logout')
def logout_page():
    logout_user()
    flash("You have been logged out!", category = 'info')
    return redirect(url_for('home_page'))

count=0
dcode, dchangeModel, dlongPredInput,\
        dchangelongPredMod, dcancelModel, dcancelLong, dnewLookback, dnewEpoch, dnewNeuron, dnewLoss, dnewOptimizer,\
        dnewLongLookback, dnewLongEpoch, dnewLongNeuron, dnewLongLoss, dnewLongOptimizer, dnumDays = None, None,None,None,\
        None,None,None,None,None,None,None,None,None,None,None,None,None
def my_function():
    global count,dcode, dchangeModel, dlongPredInput,\
        dchangelongPredMod, dcancelModel, dcancelLong, dnewLookback, dnewEpoch, dnewNeuron, dnewLoss, dnewOptimizer,\
        dnewLongLookback, dnewLongEpoch, dnewLongNeuron, dnewLongLoss, dnewLongOptimizer, dnumDays
    if count==0:
        dcode, dchangeModel, dlongPredInput,\
        dchangelongPredMod, dcancelModel, dcancelLong, dnewLookback, dnewEpoch, dnewNeuron, dnewLoss, dnewOptimizer,\
        dnewLongLookback, dnewLongEpoch, dnewLongNeuron, dnewLongLoss, dnewLongOptimizer, dnumDays = code, changeModel, longPredInput,\
        changelongPredMod, cancelModel, cancelLong, newLookback, newEpoch, newNeuron, newLoss, newOptimizer,\
        newLongLookback, newLongEpoch, newLongNeuron, newLongLoss, newLongOptimizer, numDays

        dfig, dglobalerror, dmodelerror, dnewerror, dfinal = fig, globalerror, modelerror, newerror, final
    
    if count>0:
        dfig, dglobalerror, dmodelerror, dnewerror, dfinal = dashdep.updates(dcode, dchangeModel, dlongPredInput,\
            dchangelongPredMod, dcancelModel, dcancelLong, dnewLookback, dnewEpoch, dnewNeuron, dnewLoss, dnewOptimizer,\
            dnewLongLookback, dnewLongEpoch, dnewLongNeuron, dnewLongLoss, dnewLongOptimizer, dnumDays)
        
        dchangeModel=False
        dchangelongPredMod=False
        dlongPredInput=False
        dcancelModel=False
        dcancelLong=False 
        
    #Create graphJSON
    graphJSON = json.dumps(dfig, cls=plotly.utils.PlotlyJSONEncoder)
    errorsDict = {'globalerror': dglobalerror, 'modelerror': dmodelerror, 'newerror': dnewerror, 'final': dfinal}
    count+=1

    return graphJSON, errorsDict

scheduler = BackgroundScheduler()
scheduler.start()
@app.route('/deployment',methods=['GET','POST'])
@login_required
def deploy_page():
    form = StopDeploy()
    graphJSON = None
    errorsDict = {'globalerror': 0, 'modelerror': 0, 'newerror': 0, 'final': pd.DataFrame()}
    job = Userdata.query.filter_by(owner = current_user.id).first()
    if job:
        job_id = job.job_id
        scheduler.resume_job(job_id)
    else:
        job_id = str(uuid.uuid4()) + '_model'
        job = Userdata(job_id = job_id, owner = current_user.id)
        db.session.add(job)
        db.session.commit()
        jobres =  scheduler.add_job(func = my_function, trigger='interval', seconds=60, id=job_id)
        graphJSON, errorsDict = jobres.run()
    session['job_id'] = job_id

    if request.method == 'POST':
        if form.validate_on_submit():
            if form.stop.data:
                job_id = session.get('job_id')
                try:
                    scheduler.remove_job(job_id)
                except:
                    pass
                job = Userdata.query.filter_by(job_id=job_id).first()
                db.session.delete(job)
                db.session.commit()
                count=0
                print("stopped!")
    
    return render_template('deployment.html', form=form, graphJSON=graphJSON, errorsDict = errorsDict)
