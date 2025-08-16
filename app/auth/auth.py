from flask import render_template, redirect, url_for, flash # type: ignore
from flask_login import login_user, login_required, logout_user, current_user # type: ignore
from . import auth_bp as auth
from ..extentions import bcrypt, db, mail
from ..models import load_user
from ..models import User
from .forms import RegisterForm, LoginForm, ForgotPasswordForm, ResetPasswordForm, generate_reset_token, verify_reset_token
from flask_mail import Message # type: ignore


@auth.route('/register',methods = ['GET','POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        email = form.email.data
        username = form.username.data
        password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username = username , password = password , email = email)
        db.session.add(user)
        db.session.commit()
        flash('Account Registred Successfully, Confirmation Email sent!','success')
        msg = Message('Account Created', recipients=[email])
        msg.body = f'Welcome {user.username}, your account has been created successfully!'
        mail.send(msg)
        return redirect(url_for('auth.login'))
    
    return render_template('register.html',form=form)

@auth.route('/login',methods = ['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password,password):
            login_user(user,remember=form.remember.data)
            flash('Welcome!')
            return redirect(url_for('blog.home'))
        else:
            flash('Invalid username or password','danger')
            return redirect(url_for('auth.login'))
    return render_template('login.html',form=form)

@auth.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    form = ForgotPasswordForm()
    if form.validate_on_submit():
        email = form.email.data
        user = User.query.filter_by(email=email).first()
        if user:
            token = generate_reset_token(email)
            reset_url = url_for('auth.reset_password', token=token, _external=True)
            flash('A password reset link has been sent to your email.', 'info')
            # Here you would typically send an email with a reset link
            msg = Message('Password Reset Request',[email])
            msg.body = f'Click the link to reset your password: {reset_url}'
            msg.html = render_template('reset_password_email.html', reset_url=reset_url)
            mail.send(msg)
            # Note: In a real application, you would send the email here
            return redirect(url_for('auth.login'))
        else:
            flash('No account found with that email.', 'danger')
    return render_template('forgot_password.html', form=form)

@auth.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    email = verify_reset_token(token)
    if not email:
        flash('Invalid or expired token.', 'danger')
        return redirect(url_for('auth.login'))
    # If the token is valid, find the user by email
    user = User.query.filter_by(email=email).first()   # find user by email from token
    if not user:
        flash('User not found.', 'danger')
        return redirect(url_for('auth.login'))
    
    form = ResetPasswordForm()
    if form.validate_on_submit():
        password = form.password.data
        user.password = bcrypt.generate_password_hash(password).decode('utf-8')
        db.session.commit()
        flash('Your password has been updated!', 'success')
        return redirect(url_for('auth.login'))
    return render_template('reset_password.html', form=form)
    

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('logout successfully','info')
    return redirect(url_for('auth.login'))
