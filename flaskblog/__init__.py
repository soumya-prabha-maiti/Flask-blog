from datetime import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__) 
app.config['SECRET_KEY']="532e9fcb0e8a603aaba6da044566f412"
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///site.db'#//// used for absolute path; ///used for relative path with respect to the project folder

db=SQLAlchemy(app)
bcrypt=Bcrypt(app)
login_manager=LoginManager(app)
login_manager.login_view='login'#function name for login, this is called when we try to access a page restricted behind login
login_manager.login_message_category='info'# bootstrap class for flash messages to be displyed when trying to access restricted pages 

from flaskblog import routes