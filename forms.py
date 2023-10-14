from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, InputRequired

class SignupForm(FlaskForm):
    first_name = StringField('First name', validators=[DataRequired(message='Please enter your first name')])
    last_name = StringField('Last name', validators=[DataRequired(message='Please enter your last name')])
    email = StringField('Email', validators=[DataRequired(message='Please enter your email'), Email(message='Please enter a valid email')])
    password = PasswordField('Password', validators=[InputRequired(message='Please enter your password'), EqualTo('confirm_password', message='Password must match')])
    confirm_password = PasswordField('Confirm password', validators=[DataRequired(message='Please enter your confirm password')])
    submit = SubmitField('Sign up')

class SignInForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(message='Please enter your email'), Email(message='Please enter a valid email')])
    password = PasswordField('Password', validators=[InputRequired(message='Please enter your password')])
    submit = SubmitField('Sign in')

class TaskForm(FlaskForm):
    description = StringField('Description', validators=[DataRequired(message='Please enter a description')])
    priority = SelectField('Priority', coerce=int)
    submit = SubmitField('Submit')