from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, IntegerField
from wtforms.validators import Length, DataRequired
from tensorflow.keras.optimizers.legacy import Adam, SGD, RMSprop


class generalInputs(FlaskForm):
    code = StringField(label='Enter the code',  default="AAPL", validators=[Length(min=1,max=15), DataRequired()])
    cancelmodel = SubmitField(label='Cancel your model')
    cancellongmodel = SubmitField(label='Cancel long prediction')
    numdays = IntegerField(label='Enter the days you want to predict', validators=[Length(min=1,max=3), DataRequired()])
    longprediction = SubmitField(label='Long prediction')

class DashFormNewModel(FlaskForm):
    newNeuron = IntegerField(label='Neurons', validators=[Length(min=1, max=3),DataRequired()])
    newEpoch = IntegerField(label='Epochs', validators=[Length(min=1,max=3), DataRequired()])
    newLookback = IntegerField(label='Lookback window', validators=[Length(min=1,max=3), DataRequired()])
    newLoss = SelectField(label ='Loss function', choices=[('mean_squared_error','MSE'),('mean_absolute_error','MAE'),\
                                                     ('mean_absolute_percentage_error','MAPE'),\
                                                        ('mean_squared_logarithmic_error','MSLE')], validators=[DataRequired()])
    newOptimizer=SelectField(label = 'Optimizer', choices=[(Adam(),'Adam'),(SGD(),'SGD'),\
                                                    (RMSprop(),'RMSprop')], validators=[DataRequired()])
    submitmodel = SubmitField(label='Change the model')
    submitsave = SubmitField(label='Save the model')

class DashFormNewLongModel(FlaskForm):
    newNeuron = IntegerField(label='Neurons', validators=[Length(min=1, max=3),DataRequired()])
    newEpoch = IntegerField(label='Epochs', validators=[Length(min=1,max=3), DataRequired()])
    newLookback = IntegerField(label='Lookback window', validators=[Length(min=1,max=3), DataRequired()])
    newLoss = SelectField(label ='Loss function', choices=[('mean_squared_error','MSE'),('mean_absolute_error','MAE'),\
                                                     ('mean_absolute_percentage_error','MAPE'),\
                                                        ('mean_squared_logarithmic_error','MSLE')], validators=[DataRequired()])
    newOptimizer=SelectField(label = 'Optimizer', choices=[(Adam(),'Adam'),(SGD(),'SGD'),\
                                                    (RMSprop(),'RMSprop')], validators=[DataRequired()])
    submitmodel = SubmitField(label='Change the model')
    submitsave = SubmitField(label='Save the model')
    
