
import os
import secrets
from PIL import Image
from flask import flash, redirect,render_template,url_for, request,abort
from flask_mail import Message
from flaskblog.forms import SignUpForm,LoginForm,UpdateAccountForm,BlogpostForm,RequestResetForm,ResetPasswordForm
from flaskblog import app, db, bcrypt, mail
from flaskblog.models import User,Post
from flask_login import login_user, current_user, logout_user,login_required


@app.route('/') 
@app.route('/home')
def home(): 
    page=request.args.get('page',default=1,type=int)
    posts=Post.query.order_by(Post.datePosted.desc()).paginate(page=page,per_page=5)
    return render_template('home.html',posts=posts)

@app.route('/about') 
def about(): 
    return render_template('about.html',newTitle='About')

@app.route('/signup',methods=['POST','GET']) 
def signup(): 
    if current_user.is_authenticated:
        return redirect(url_for('home')) 
    form=SignUpForm()
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
    form=LoginForm()
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
    form=UpdateAccountForm()
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

@app.route('/post/new',methods=['POST','GET'])
@login_required
def create_post():
    form=BlogpostForm()
    if form.validate_on_submit():
        new_post=Post(title=form.title.data,content=form.content.data,author=current_user)
        db.session.add(new_post)
        db.session.commit()
        flash('Your post has been created!','success')
        return redirect(url_for('home')) 
    return render_template('create_update_post.html',newTitle='Create Post',form=form,legend='Create a new post')

@app.route('/post/<int:post_id>')
def post(post_id):
    post=Post.query.get_or_404(post_id)
    return render_template('post.html',newTitle=post.title,post=post)

@app.route('/post/<int:post_id>/update',methods=['POST','GET'])
@login_required
def update_post(post_id):
    post=Post.query.get_or_404(post_id)
    if post.author!=current_user:
        abort(403)
    form=BlogpostForm()

    if form.validate_on_submit():
        post.title=form.title.data
        post.content=form.content.data
        db.session.commit()
        flash('Your post has been updated!','success')
        return redirect(url_for('post',post_id=post.id))
    elif request.method=='GET':
        form.title.data=post.title
        form.content.data=post.content
        return render_template('create_update_post.html',newTitle='Update Post',form=form,legend='Update Post')

@app.route('/post/<int:post_id>/delete',methods=['POST'])
@login_required
def delete_post(post_id):
    post=Post.query.get_or_404(post_id)
    if post.author!=current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!','success')
    return redirect(url_for('home'))


@app.route('/user/<string:username>')
def user_profile(username): 
    page=request.args.get('page',default=1,type=int)
    user=User.query.filter_by(username=username).first_or_404()
    posts=Post.query.filter_by(author=user)\
        .order_by(Post.datePosted.desc())\
        .paginate(page=page,per_page=5)
    return render_template('user_profile.html',newTitle=f'User - {username}',posts=posts,user=user)

def send_reset_email(user):
    token=user.create_pw_reset_token()
    msg=Message('Password Reset Request',sender='noreply@demo.com',recipients=[user.email])
    msg.body=f'''To reset your password, visit the following link:
    
{url_for('reset_password',token=token,_external=True)}

If you did not make this request, you can safely ignore this email and no changes will be made to your accout.
    '''
    mail.send(msg)

@app.route("/request_password_reset",methods=['GET','POST'])
def request_reset():
    if current_user.is_authenticated:
        # TODO : logout user instead of redirect to home
        return redirect(url_for('home'))
    form=RequestResetForm()
    if form.validate_on_submit():
        user=User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash("An email has been sent with instructions to reset your password","info")
        return redirect(url_for("login"))
    return render_template('request_reset.html',newTitle='Request Password Reset',form=form)

@app.route("/reset_password/<token>",methods=['GET','POST'])
def reset_password(token):
    if current_user.is_authenticated:
        # TODO : logout user instead of redirect to home
        return redirect(url_for('home'))
    user = User.verify_pw_reset_token(token)
    if user is None:
        flash('Invalid or expired token','warning')
        return redirect(url_for('request_reset'))
    form=ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password=bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password=hashed_password
        db.session.commit()
        flash(f"Your Password has been updated! You can now log in.","success")
        return redirect(url_for('login'))
    return render_template('reset_password.html',newTitle='Reset Password',form=form)