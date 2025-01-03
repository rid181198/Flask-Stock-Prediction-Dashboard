from flask import Flask, request, render_template, url_for, flash, session, redirect, make_response
from stockpred import app
from sqlalchemy.orm import Session
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
import json
import stockpred.scripts.dashboard as dash
import stockpred.scripts.dashboardDeploy as dashdep
import plotly
import plotly.express as px
from stockpred.forms.dashform import DashFormNewModel, DashFormNewLongModel, generalInputs, cancelForm, longpredForm, DownloadForm, StopDeploy, DeployForm
from stockpred.forms.user import RegisterForm, LoginForm
from stockpred.models.register import User, Userdata
from tensorflow.keras.optimizers.legacy import Adam, SGD, RMSprop
from flask_login import login_user, logout_user, login_required, current_user
from stockpred import db
import uuid
import json
from datetime import datetime
import time
from io import StringIO
import io
import traceback
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
        newLongLookback, newLongEpoch, newLongNeuron, newLongLoss, newLongOptimizer, numDays, fig, globalerror, modelerror, newerror, final, graphJSON

   
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
    form6 = DeployForm()

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
        if request.form.get('deploy'):
            if current_user.is_authenticated & ('graphJSON' in globals()) :
                userdata = User.query.filter_by(id = current_user.id).first()
                userdata.deploy_status = True
                db.session.add(userdata)
                db.session.commit()
                return redirect(url_for('deploy_page'))
            else:
                flash(f'Either you are not logged in or you have not run the model first.', category='danger')
                return redirect(url_for('dashboard_page'))
            

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
          
            print("#################################################")
            print(changeModel, newEpoch)
            print("#################################################")

            code, changeModel, longPredInput,\
            changelongPredMod, cancelModel, cancelLong, newLookback, newEpoch, newNeuron, newLoss, newOptimizer,\
            newLongLookback, newLongEpoch, newLongNeuron, newLongLoss, newLongOptimizer, numDays, fig, globalerror, modelerror, newerror, final, graphJSON = \
            code, changeModel, longPredInput,\
            changelongPredMod, cancelModel, cancelLong, newLookback, newEpoch, newNeuron, newLoss, newOptimizer,\
            newLongLookback, newLongEpoch, newLongNeuron, newLongLoss, newLongOptimizer, numDays, fig, globalerror, modelerror, newerror, final, graphJSON



            if form5.validate_on_submit():
                if form5.download.data:
                    response = make_response(final.to_csv(index=False))
                    response.headers.set('Content-Disposition', 'attachment', filename='final.csv')
                    response.headers.set('Content-Type', 'text/csv')
                    return response
        
            return render_template('dashboard.html',  form0=form0, form1=form1,form1errors=form1errors, form2=form2,\
                                   form2errors=form2errors, form3 = form3, form4 = form4,\
                                     form4errors=form4errors, form5=form5, form6 = form6,  graphJSON=graphJSON, errorsDict = errorsDict, code=code)
        except Exception as e:
            # Print detailed traceback
            print("An exception occurred:")
            traceback.print_exc()
            # You can also log the error message or use it programmatically
            error_message = traceback.format_exc()
            print(f"Formatted traceback: {error_message}")
            flash(f'You have entered the wrong code! Please look at the meta data guide in the settings.', category='danger')
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
                            form2=form2,form2errors=form2errors,form3 = form3, form4 = form4,form4errors=form4errors, form5=form5, form6 = form6, errorsDict = errorsDict)




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

#count,dcode, dchangeModel, dlongPredInput,\
#        dchangelongPredMod, dcancelModel, dcancelLong, dnewLookback, dnewEpoch, dnewNeuron, dnewLoss, dnewOptimizer,\
#        dnewLongLookback, dnewLongEpoch, dnewLongNeuron, dnewLongLoss, dnewLongOptimizer, dnumDays


#job.variables['count'],\
#        job.variables['code'],job.variables['changeModel'],job.variables['longPredInput'],job.variables['changelongPredMod'],\
#        job.variables['cancelModel'],job.variables['cancelLong'],job.variables['newLookback'],job.variables['newEpoch'],job.variables['newNeuron'],\
#        job.variables['newLoss'],job.variables['newOptimizer'],job.variables['newLongLookback'],job.variables['newLongEpoch'],job.variables['newLongNeuron'],\
#        job.variables['newLongLoss'],job.variables['newLongOptimizer'],job.variables['numDays']

class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        elif isinstance(obj, pd.Timestamp):
            return obj.isoformat()
        elif isinstance(obj, np.ndarray):
            return obj.tolist() 
        elif isinstance(obj, np.float32):
            return float(obj)
        elif isinstance(obj, MinMaxScaler):
            return {'scale_min': obj.data_min_.tolist(), 'scale_max': obj.data_max_.tolist()}
        elif isinstance(obj, pd.DataFrame):
            return obj.to_csv(index=False)
        elif isinstance(obj, Sequential):
            return obj.to_json()
        else:
            return super().default(obj)
        
class CustomDecoder(json.JSONDecoder):
    def __init__(self, *args, **kwargs):
        super().__init__(object_hook=self.object_hook, *args, **kwargs)
        
    def object_hook(self, obj_dict):
        if '__class__' in obj_dict:
            class_name = obj_dict['__class__']
            if class_name == 'DataFrame':
                print('yes it is dataframe')
                df = pd.read_json(obj_dict['__value__'])
                if 'Date' in df.columns:
                    df['Date'] = pd.to_datetime(df['Date'])
                return df
            elif class_name == 'Sequential':
                print('yes it is sequential')
                return Sequential.from_config(json.loads(obj_dict['__value__']))
        elif 'scale_min' in obj_dict and 'scale_max' in obj_dict:
            return MinMaxScaler(feature_range=(0, 1), copy=False).fit([obj_dict['scale_min'], obj_dict['scale_max']])
        elif 'dtype' in obj_dict:
            return np.array(obj_dict['data'], dtype=obj_dict['dtype'])
        elif 'datetime' in obj_dict:
            return datetime.datetime.strptime(obj_dict, '%Y-%m-%d')
        elif 'timestamp' in obj_dict:
            return pd.Timestamp(obj_dict['timestamp'])
        else:
            return obj_dict
      

def my_function():
    with app.app_context():
        jobs = db.session.query(Userdata).all()
        for job in jobs:
            variables = json.loads(job.variables,cls=CustomDecoder)
            variables['count'] += 1
            if variables['count']>0:
                #print(variables['historyDate'])
                dfig, newVariable = dashdep.updates(variables['globalPred'], variables['globalReal'], variables['prevCode'], pd.read_csv(StringIO(variables['dataset'])), variables['history'], variables['historyDate'], variables['train'], variables['target'], variables['realTarget'],\
                variables['predTarget'], variables['model'], variables['scaler'], variables['lookback'], variables['lookbackData'], variables['epochs'],variables['dates'], variables['longpredTarget'],\
                variables['longmodel'],variables['longscaler'],variables['trainv2'],variables['targetv2'],variables['realTargetv2'],variables['predTargetv2'],\
            variables['modelv2'],variables['scalerv2'],variables['lookbackDatav2'],variables['lookbackv2'], variables['epochsv2'], variables['longpredTargetFin'],\
                variables['code'], variables['changeModel'], variables['longPredInput'],\
                        variables['changelongPredMod'], variables['cancelModel'], variables['cancelLong'], variables['newLookback'], variables['newEpoch'], variables['newNeuron'], variables['newLoss'], variables['newOptimizer'],\
                            variables['newLongLookback'], variables['newLongEpoch'], variables['newLongNeuron'], variables['newLongLoss'], variables['newLongOptimizer'], variables['numDays'])
                
                #variables['fig'] = newVariable['fig']
                variables['rmseGlobal'] = newVariable['rmseGlobal']
                variables['rmseModel'] = newVariable['rmseModel']
                variables['rmseNew'] = newVariable['rmseNew']
                variables['prevCode'] = newVariable['prevCode']
                variables['dataset'] = newVariable['dataset']
                variables['history'] = newVariable['history']
                variables['historyDate'] = newVariable['historyDate']
                variables['train'] = newVariable['train']
                variables['target'] = newVariable['target']
                variables['realTarget'] = newVariable['realTarget']
                variables['predTarget'] = newVariable['predTarget']
                variables['model'] = newVariable['model']
                variables['scaler'] = newVariable['scaler']
                variables['lookback'] = newVariable['lookback']
                variables['lookbackData'] = newVariable['lookbackData']
                variables['epochs'] = newVariable['epochs']
                variables['dates'] = newVariable['dates']
                variables['longpredTarget'] = newVariable['longpredTarget']
                variables['longmodel'] = newVariable['longmodel']
                variables['longscaler'] = newVariable['longscaler']
                variables['trainv2'] = newVariable['trainv2']
                variables['targetv2'] = newVariable['targetv2']
                variables['realTargetv2'] = newVariable['realTargetv2']
                variables['predTargetv2'] = newVariable['predTargetv2']
                variables['modelv2'] = newVariable['modelv2']
                variables['scalerv2'] = newVariable['scalerv2']
                variables['lookbackv2'] = newVariable['lookbackv2']
                variables['lookbackDatav2'] = newVariable['lookbackDatav2']
                variables['epochsv2'] = newVariable['epochsv2']
                variables['globalPred'] = newVariable['globalPred']
                variables['globalReal'] = newVariable['globalReal']
                variables['longpredTargetFin'] = newVariable['longpredTargetFin']
                variables['final'] = newVariable['final']
                print(variables["changeModel"], variables["newEpoch"], variables['modelv2'])
                #Create graphJSON
                dgraphJSON = json.dumps(dfig, cls=plotly.utils.PlotlyJSONEncoder)
                derrorsDict = {'globalerror': variables['rmseGlobal'], 'modelerror': variables['rmseModel'], 'newerror': variables['rmseNew'], 'final': variables['final']}
                

                variables = json.dumps(variables, cls=CustomEncoder)
                job.variables = variables
                job.json_data = dgraphJSON

                
                db.session.commit()


scheduler = BackgroundScheduler()
scheduler.start()
@app.route('/deployment',methods=['GET','POST'])
@login_required
def deploy_page():

    userdata = User.query.filter_by(id = current_user.id).first()
    if userdata.deploy_status:

        form = StopDeploy()
        form5 = DownloadForm()
        job = Userdata.query.filter_by(owner = current_user.id).first()
        if job:
            job_id = job.job_id
            json_data = job.json_data
            variables = job.variables
            scheduler.resume_job(job_id)
        else:
            job_id = str(uuid.uuid4()) + '_model'
            variables = {'rmseGlobal': globalerror,
            'rmseModel': modelerror,
            'rmseNew': newerror,
            'prevCode': '',
            'dataset': pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]}).to_csv(index=False),
            'history': None,
            'historyDate': [datetime.strptime('2000-01-01','%Y-%m-%d'),datetime.strptime('2000-01-02','%Y-%m-%d')],
            'train': None,
            'target': None,
            'realTarget': [0],
            'predTarget': [0],
            'model': None,
            'scaler': None,
            'lookback':None,
            'lookbackData': None,
            'epochs': None,
            'dates': [datetime.strptime('2000-01-01','%Y-%m-%d'),datetime.strptime('2000-01-02','%Y-%m-%d')],
            'longpredTarget': None,
            'longmodel': None,
            'longscaler': None,
            'trainv2':None,
            'targetv2': None,
            'realTargetv2': None,
            'predTargetv2': None,
            'modelv2': None,
            'scalerv2': None,
            'lookbackDatav2': None,
            'lookbackv2': None,
            'epochsv2': None,
            'globalPred': [0],
            'globalReal': [0],
            'longpredTargetFin': None,
            'final': final,
            "code": code,
                "changeModel": changeModel,
                "longPredInput": longPredInput,
                "changelongPredMod": changelongPredMod,
                "cancelModel": cancelModel,
                "cancelLong": cancelLong,
                "newLookback": newLookback,
                "newEpoch": newEpoch,
                "newNeuron": newNeuron,
                "newLoss": newLoss,
                "newOptimizer": newOptimizer,
                "newLongLookback": newLongLookback,
                "newLongEpoch": newLongEpoch,
                "newLongNeuron": newLongNeuron,
                "newLongLoss": newLongLoss,
                "newLongOptimizer": newLongOptimizer,
                "numDays": numDays,
                "count":0}
            print("#################################################")
            print(changeModel, newEpoch)
            print("#################################################")
            variables = json.dumps(variables, cls=CustomEncoder)
            json_data = graphJSON
            job = Userdata(job_id = job_id, variables = variables, json_data=json_data, owner = current_user.id)
            
            db.session.add(job)
            db.session.commit()

            scheduler.add_job(func = my_function, trigger='interval', seconds=30, id=job_id)
            return redirect(url_for('deploy_page'))
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
                    userdata = User.query.filter_by(id = current_user.id).first()
                    userdata.deploy_status = False

                    db.session.add(userdata)
                    db.session.delete(job)
                    db.session.commit()
                    print("stopped!")

            if form5.validate_on_submit():
                if form5.download.data:
                    job_id = session.get('job_id')
                    job = Userdata.query.filter_by(job_id=job_id).first()
                    variables = json.loads(job.variables,cls=CustomDecoder)
                    finaldep = variables['final']
            
                    csv_data = io.StringIO()
                    csv_data.write(finaldep)
                    
                    response = make_response(csv_data.getvalue())
                    response.headers.set('Content-Disposition', 'attachment', filename='final.csv')
                    response.headers.set('Content-Type', 'text/csv')
                    return response
        
        return render_template('deployment.html', form=form, form5 = form5, dgraphJSON=job.json_data, derrorsDict = {'globalerror': 0, 'modelerror': 0, 'newerror': 0, 'final': pd.DataFrame()})

    else:
        flash(f'No deployed models! Please click on the Deploy model button', category='danger')
        return redirect(url_for('dashboard_page'))
