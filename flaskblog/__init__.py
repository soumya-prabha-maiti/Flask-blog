from datetime import datetime
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail

app = Flask(__name__) 
app.config['SECRET_KEY']="532e9fcb0e8a603aaba6da044566f412"
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///site.db'#//// used for absolute path; ///used for relative path with respect to the project folder

db=SQLAlchemy(app)
bcrypt=Bcrypt(app)
login_manager=LoginManager(app)
login_manager.login_view='users.login'#function name for login, this is called when we try to access a page restricted behind login
login_manager.login_message_category='info'# bootstrap class for flash messages to be displyed when trying to access restricted pages 

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT']='587'
app.config['MAIL_USE_TLS']=True
app.config['MAIL_USERNAME']=os.environ.get('EMAIL_USERNAME')
app.config['MAIL_PASSWORD']=os.environ.get('EMAIL_PASSWORD')
mail=Mail(app)

from flaskblog.users.routes import users
from flaskblog.posts.routes import posts
from flaskblog.main.routes import main

app.register_blueprint(users)
app.register_blueprint(posts)
app.register_blueprint(main)
