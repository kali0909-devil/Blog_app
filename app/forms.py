from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField
from wtforms.validators import DataRequired,length,EqualTo,ValidationError
from .models import User

class RegisterForm(FlaskForm):
    username = StringField('username',validators=[DataRequired(),length(min=3)])
    password = PasswordField('password',validators=[DataRequired(),length(min=4,message='password must contain atleast 4 characters')])
    confirm_password = PasswordField('Confirm Password',validators=[DataRequired(),EqualTo('password',message='password dose not match')])
    submit = SubmitField('Register')
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is already taken. Please choose another one.')

class LoginForm(FlaskForm):
    username = StringField('username',validators=[DataRequired()])
    password = PasswordField('password',validators=[DataRequired()])
    submit = SubmitField('Login')
