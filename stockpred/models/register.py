from stockpred import db, login_manager
from stockpred import bcrypt
from flask_login import UserMixin

@login_manager.user_loader
def user_loader(user):
    return User.query.get(int(user))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=30), nullable=False, unique=True)
    email_address = db.Column(db.String(length=50), nullable=False, unique=True)
    password_hash = db.Column(db.String(length=60), nullable=False)
    userdata = db.relationship('Userdata', backref='owned_user', lazy=True)

    @property
    def password(self):
        return self.password
    
    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

    def check_password(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)

class Userdata(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    job_id = db.Column(db.String(length=50))
    json_data = db.Column(db.String(), default='')
    owner = db.Column(db.Integer(), db.ForeignKey('user.id'))
    variables = db.Column(db.String(), default='')
    #def __init__(self, df):
    #    self.json_data = df.to_json()

    
