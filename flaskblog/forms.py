import email
from flask_login import current_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileField,FileAllowed
from wtforms import StringField,PasswordField,SubmitField,BooleanField,TextAreaField
from wtforms.validators import DataRequired,length,Email,EqualTo,ValidationError
from flaskblog.models import User

class SignUpForm(FlaskForm):
    username = StringField('Username',validators=[DataRequired(),length(min=2,max=50)])
    email=StringField('Email',validators=[DataRequired(),Email()])
    password=PasswordField('Password',validators=[DataRequired()])
    confirmPassword=PasswordField('Confirm Password',validators=[DataRequired(),EqualTo('password',message="Passwords do not match")])
    submit=SubmitField(label="Sign Up")

    # Template of custom validator: 
    # def validate_field(self,field):
    #     if condition:
    #         raise ValidationError('Validation message')

    def validate_username(self,username):
        user=User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username is already taken. Please choose a different one')

    def validate_email(self,email):
        user=User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email is already taken. Please choose a different one')

class LoginForm(FlaskForm):
    email=StringField('Email',validators=[DataRequired(),Email()])#Login with email
    password=PasswordField('Password',validators=[DataRequired()])
    remember=BooleanField(label='Remember Me')#Stay logged in with a secure cookie
    submit=SubmitField(label='Log in')

class UpdateAccountForm(FlaskForm):
    username = StringField('Username',validators=[DataRequired(),length(min=2,max=50)])
    email=StringField('Email',validators=[DataRequired(),Email()])
    profile_pic=FileField(label='Update Profile Picture',validators=[FileAllowed(['jpg','png'])])
    submit=SubmitField(label="Update")
    

    def validate_username(self,username):
        if username.data!=current_user.username:
            user=User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('Username is already taken. Please choose a different one')

    def validate_email(self,email):
        if email.data!=current_user.email:
            user=User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('Email is already taken. Please choose a different one')


class BlogpostForm(FlaskForm):
    title = StringField('Title',validators=[DataRequired()])
    content=TextAreaField('Content')
    submit=SubmitField(label="Post")

class RequestResetForm(FlaskForm):
    email=StringField('Email',validators=[DataRequired(),Email()])
    submit=SubmitField(label="Request Reset")

    def validate_email(self,email):
        user=User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('No user found with given email. You must register first')

class ResetPasswordForm(FlaskForm):
    password=PasswordField('Password',validators=[DataRequired()])
    confirm_password=PasswordField('Confirm Password',validators=[DataRequired(),EqualTo('password',message="Passwords do not match")])
    submit=SubmitField(label="Reset Password")
