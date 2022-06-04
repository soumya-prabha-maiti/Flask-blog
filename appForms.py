import email
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,BooleanField
from wtforms.validators import DataRequired,length,Email,EqualTo

class SignUpForm(FlaskForm):
    username = StringField('Username',validators=[DataRequired(),length(min=2,max=50)])
    email=StringField('Email',validators=[DataRequired(),Email()])
    password=PasswordField('Password',validators=[DataRequired()])
    confirmPassword=PasswordField('Confirm Password',validators=[DataRequired(),EqualTo('password',message="Passwords do not match")])
    submit=SubmitField(label="Sign Up")

class LoginForm(FlaskForm):
    email=StringField('Email',validators=[DataRequired(),Email()])#Login with email
    password=PasswordField('Password',validators=[DataRequired()])
    remember=BooleanField(label='Remember Me')#Stay logged in with a secure cookie
    submit=SubmitField(label='Log in')
