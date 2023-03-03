from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, IntegerField, HiddenField
from wtforms.validators import Length, DataRequired, NumberRange



class generalInputs(FlaskForm):
    code = StringField(label='Enter the code', validators=[Length(min=1,max=15)])
    cancelmodel = SubmitField(label='Cancel your model')
    #cancellongmodel = SubmitField(label='Cancel long prediction')
    #numdays = IntegerField(label='Enter the days you want to predict', validators=[NumberRange(min=1,max=300)])
    #longprediction = SubmitField(label='Long prediction')

class DashFormNewModel(FlaskForm):
    newNeuron = IntegerField(label='Neurons', validators=[NumberRange(min=1, max=100)])
    newEpoch = IntegerField(label='Epochs', validators=[NumberRange(min=1,max=100)])
    newLookback = IntegerField(label='Lookback window', validators=[NumberRange(min=1,max=30)])
    newLoss = SelectField(label ='Loss function', choices=[('mean_squared_error','MSE'),('mean_absolute_error','MAE'),\
                                                     ('mean_absolute_percentage_error','MAPE'),\
                                                        ('mean_squared_logarithmic_error','MSLE')])
    newOptimizer=SelectField(label = 'Optimizer', choices=[('Adam','Adam'),('SGD','SGD'),\
                                                    ('RMSprop','RMSprop')])
    submitmodel = SubmitField(label='Change the model')
    submitsave = SubmitField(label='Save the model')

class DashFormNewLongModel(FlaskForm):

    newNeuron = IntegerField(label='Neurons', validators=[NumberRange(min=1, max=100)])
    newEpoch = IntegerField(label='Epochs', validators=[NumberRange(min=1,max=100)])
    newLookback = IntegerField(label='Lookback window', validators=[NumberRange(min=1,max=30)])
    newLoss = SelectField(label ='Loss function', choices=[('mean_squared_error','MSE'),('mean_absolute_error','MAE'),\
                                                     ('mean_absolute_percentage_error','MAPE'),\
                                                        ('mean_squared_logarithmic_error','MSLE')])
    newOptimizer=SelectField(label = 'Optimizer', choices=[('Adam','Adam'),('SGD','SGD'),\
                                                    ('RMSprop','RMSprop')])
    submitmodel = SubmitField(label='Change the model')
    submitsave = SubmitField(label='Save the model')
