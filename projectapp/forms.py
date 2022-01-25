from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField ,SubmitField
# from wtforms.fields.simple import TextAreaField
from wtforms.validators import DataRequired,Email,Length,InputRequired

class LoginForm(FlaskForm):
    username = StringField('username: ', validators=[InputRequired(), Length(min=5, max=30)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=200)])

class RegisterForm(FlaskForm):
    username = StringField('username: ', validators=[InputRequired(), Length(min=5, max=30)])
    email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'),])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=200)])