from datetime import datetime
from enum import unique
from flask import Flask, flash, redirect,render_template,url_for
from flask_sqlalchemy import SQLAlchemy
import appForms

app = Flask(__name__) 
app.config['SECRET_KEY']="532e9fcb0e8a603aaba6da044566f412"
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///site.db'#//// used for absolute path; ///used for relative path with respect to the project folder

db=SQLAlchemy(app)
class User(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(50),unique=True,nullable=False)
    email=db.Column(db.String(128),unique=True,nullable=False)
    # The profile pic may not be unique eg the default starting picture 
    profilePic=db.Column(db.String(20),nullable=False,default="default.jpg")
    password=db.Column(db.String(60),nullable=False)

    # A relationship is not a column , but actually it runs a query in the on the post table
    # backref = 
    # lazy = 
    posts=db.relationship('Post',backref='author',lazy=True)

    def ___repr__(self):
        return f"User('{self.username}','{self.email}','{self.password}')"
    
class Post(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(100),nullable=False)
    datePosted=db.Column(db.DateTime,nullable=False,default=datetime.utcnow)
    content=db.Column(db.Text,nullable=False)
    userId=db.Column(db.Integer, db.ForeignKey('user.id'),nullable=True)
    # The argument of ForeignKey is small letter user since it represents the table user
    # For every class, the corresponding table is small lettered by default

    def ___repr__(self):
        return f"User('{self.title}','{self.datePosted}')"

    

    

blogPosts=[
    {
        'author':'Me',
        'title':'Post 1',
        'content':'Hi !',
        'date':'June 5,2020'
    },
    {
        'author':'Friend',
        'title':'New post',
        'content':'Hello',
        'date':'May 18,2020'
    },
    {
        'author':'Friend',
        'title':'New post',
        'content':'Hello',
        'date':'May 18,2020'
    },
    {
        'author':'Friend',
        'title':'New post',
        'content':'Hello',
        'date':'May 18,2020'
    },
    {
        'author':'Friend',
        'title':'New post',
        'content':'Hello',
        'date':'May 18,2020'
    },
    {
        'author':'Friend',
        'title':'New post',
        'content':'Hello',
        'date':'May 18,2020'
    },
    {
        'author':'Friend',
        'title':'New post',
        'content':'Hello',
        'date':'May 18,2020'
    },

    {
        'author':'Friend',
        'title':'New post',
        'content':'Hello',
        'date':'May 18,2020'
    },
    {
        'author':'Friend',
        'title':'New post',
        'content':'Hello',
        'date':'May 18,2020'
    },
    {
        'author':'Friend',
        'title':'New post',
        'content':'Hello',
        'date':'May 18,2020'
    },
    {
        'author':'Friend',
        'title':'New post',
        'content':'Hello',
        'date':'May 18,2020'
    },
    {
        'author':'Friend',
        'title':'New post',
        'content':'Hello',
        'date':'May 18,2020'
    },
    {
        'author':'Friend',
        'title':'New post',
        'content':'Hello',
        'date':'May 18,2020'
    },
    {
        'author':'Friend',
        'title':'New post',
        'content':'Hello',
        'date':'May 18,2020'
    },
    {
        'author':'Friend',
        'title':'New post',
        'content':'Hello',
        'date':'May 18,2020'
    },
]

@app.route('/') 
@app.route('/home')
def home(): 
    return render_template('home.html',posts=blogPosts)

@app.route('/about') 
def about(): 
    return render_template('about.html',newTitle='About')

@app.route('/signup',methods=['POST','GET']) 
def signup(): 
    form=appForms.SignUpForm()
    if form.validate_on_submit():
        flash(f"Account created for {form.username.data}","success")
        return redirect(url_for('home'))
    return render_template('signup.html',newTitle='Sign Up',form=form)

@app.route('/login',methods=['POST','GET']) 
def login(): 
    form=appForms.LoginForm()
    if form.validate_on_submit():
        if form.email.data=='admin@blog.com' and form.password.data=="password":
            flash(f"Logged in as {form.email.data}","success")
            return redirect(url_for('home'))
        else:
            flash(f"Login unsuccessful, please check email and password","danger")
    return render_template('login.html',newTitle='Log In',form=form)

if __name__=="__main__": 
    app.run(debug=True) 