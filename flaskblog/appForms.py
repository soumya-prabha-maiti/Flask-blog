import email
from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,BooleanField
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
