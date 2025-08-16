from flask_wtf import FlaskForm # type: ignore
from wtforms import StringField,PasswordField,SubmitField,BooleanField # type: ignore
from wtforms.validators import DataRequired,length,EqualTo,ValidationError,email # type: ignore
from ..models import User
from itsdangerous import URLSafeTimedSerializer # type: ignore
from flask import current_app # type: ignore

def generate_reset_token(email):
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    return serializer.dumps(email, salt='password-reset-salt')

def verify_reset_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    try:
        email = serializer.loads(token, salt='password-reset-salt', max_age=expiration)
    except Exception:
        return None
    return email



class RegisterForm(FlaskForm):
    username = StringField('username',validators=[DataRequired(),length(min=3)])
    email = StringField('email',validators=[DataRequired(),length(min=6),email(message='Invalid email address')])
    password = PasswordField('password',validators=[DataRequired(),length(min=4,message='password must contain atleast 4 characters')])
    confirm_password = PasswordField('Confirm Password',validators=[DataRequired(),EqualTo('password',message='password dose not match')])
    submit = SubmitField('Register')
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is already taken. Please choose another one.')
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is already registered. Please choose another one.')

class LoginForm(FlaskForm):
    username = StringField('username',validators=[DataRequired()])
    password = PasswordField('password',validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class ForgotPasswordForm(FlaskForm):
    email = StringField('email',validators=[DataRequired(),length(min=6),email(message='Invalid email address')])
    submit = SubmitField('Reset Password')
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if not user:
            raise ValidationError('There is no account with that email. You must register first.')
        
class ResetPasswordForm(FlaskForm):
    password = PasswordField('password',validators=[DataRequired(),length(min=4,message='password must contain atleast 4 characters')])
    confirm_password = PasswordField('Confirm Password',validators=[DataRequired(),EqualTo('password',message='password dose not match')])
    submit = SubmitField('Reset Password')
    
    def validate_password(self, password):
        if len(password.data) < 4:
            raise ValidationError('Password must be at least 4 characters long.')
