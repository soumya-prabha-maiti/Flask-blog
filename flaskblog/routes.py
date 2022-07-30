import os
import secrets
from PIL import Image
from flask import flash, redirect,render_template,url_for, request
from flaskblog import appForms
from flaskblog import app, db, bcrypt
from flaskblog.models import User,Post
from flask_login import login_user, current_user, logout_user,login_required

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
            next_page = request.args.get('next') # use get('next') instead of ['next'] since 'next' may not exist
            return redirect(next_page) if next_page else redirect(url_for('home')) 
        else:
            flash(f"Login unsuccessful, please check email and password","danger")
    return render_template('login.html',newTitle='Log In',form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home')) 

def save_profile_pic(form_profile_pic):
    random_hex=secrets.token_hex(8)
    _,f_ext=os.path.splitext(form_profile_pic.filename)
    profile_pic_filename=random_hex+f_ext
    picture_path=os.path.join(app.root_path,'static/profile_pictures',profile_pic_filename)
    
    output_size=(256,256)
    i=Image.open(form_profile_pic)
    i.thumbnail(output_size)
    i.save(picture_path)
    return profile_pic_filename

@app.route('/account',methods=['POST','GET'])
@login_required
def account():
    form=appForms.UpdateAccountForm()
    if form.validate_on_submit():
        current_user.username=form.username.data
        current_user.email=form.email.data
        if form.profile_pic.data:
            profile_pic_filename=save_profile_pic(form.profile_pic.data)
            current_user.profilePic=profile_pic_filename
        db.session.commit()
        flash('Your account has been updated!','success')
        return redirect(url_for('account'))#redirect to avoid "Confirm form resubmission"
    elif request.method=='GET':
        # Display the current details already filled up in the form
        form.username.data=current_user.username
        form.email.data=current_user.email
    profile_pic=url_for('static',filename=f'profile_pictures/{current_user.profilePic}')
    return render_template('account.html',newTitle='Account',profile_pic=profile_pic,form=form)