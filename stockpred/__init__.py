from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
import os
from dotenv import load_dotenv
load_dotenv()
db_password = os.getenv('DB_PASSWORD')

app=Flask(__name__)
DATABASE_URL = f"postgresql://postgres.xadfhwcdjdeqdkxquphp:{db_password}@aws-0-eu-central-1.pooler.supabase.com:6543/postgres"
print(DATABASE_URL)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = '2b8c674fd1815cb4c61fb207'
app.add_url_rule('/source/<filename>', endpoint='source', view_func=app.send_static_file)
db=SQLAlchemy(app)
bcrypt=Bcrypt(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login_page"
login_manager.login_message_category = "info"
from stockpred import route
