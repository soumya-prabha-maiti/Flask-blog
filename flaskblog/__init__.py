from datetime import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__) 
app.config['SECRET_KEY']="532e9fcb0e8a603aaba6da044566f412"
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///site.db'#//// used for absolute path; ///used for relative path with respect to the project folder

db=SQLAlchemy(app)

from flaskblog import routes