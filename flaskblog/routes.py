from flask import flash, redirect,render_template,url_for
from flaskblog import appForms
from flaskblog import app, db, bcrypt
from flaskblog.models import User,Post
from flask_login import login_user, current_user, logout_user

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
    if current_user.is_authenticated:
        return redirect(url_for('home')) 
    form=appForms.SignUpForm()
    if form.validate_on_submit():
        hashed_password=bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user1= User(username=form.username.data,email=form.email.data,password=hashed_password)
        db.session.add(user1)
        db.session.commit()
        flash(f"Your account has been created! You can now log in.","success")
        return redirect(url_for('login'))
    return render_template('signup.html',newTitle='Sign Up',form=form)

@app.route('/login',methods=['POST','GET']) 
def login(): 
    if current_user.is_authenticated:
        return redirect(url_for('home')) 
    form=appForms.LoginForm()
    if form.validate_on_submit():
        user=User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password,form.password.data):
            login_user(user,remember=form.remember.data)
            return redirect(url_for('home')) 
        else:
            flash(f"Login unsuccessful, please check email and password","danger")
    return render_template('login.html',newTitle='Log In',form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home')) 
