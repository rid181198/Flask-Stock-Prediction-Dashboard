from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///stocks.db'
app.config['SECRET_KEY'] = '2b8c674fd1815cb4c61fb207'
app.add_url_rule('/source/<filename>', endpoint='source', view_func=app.send_static_file)
db=SQLAlchemy(app)
bcrypt=Bcrypt(app)
login_manager = LoginManager(app)
login_manager.init_app(app)
login_manager.login_view = "login_page"
login_manager.login_message_category = "info"
from stockpred import route