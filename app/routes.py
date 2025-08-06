
from flask import render_template,request,redirect,url_for,Blueprint,flash # type: ignore
from flask_login import login_user,login_required,logout_user,current_user # type: ignore
from . import bcrypt,db,login_manager
from .models import User,Post


blog = Blueprint('blog',__name__)



@blog.route('/')
@login_required
def home():
    posts = Post.query.all()
    return render_template('blog.html',posts=posts)


@blog.route('/new',methods = ['GET','POST'])
@login_required
def new_post():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        user_id = current_user.id
        
        posts = Post(title=title,content=content,user_id=user_id,user=current_user)
        db.session.add(posts)
        db.session.commit()
        return redirect(url_for('blog.home'))
    return render_template('new_post.html')

@blog.route('/delete/<int:post_id>', methods=['POST', 'GET'])
@login_required
def delete(post_id):
    posts = Post.query.filter_by(post_id=post_id).first()
    if posts.user_id != current_user.id:
        author = User.query.get_or_404(posts.user_id)
        flash(f"This post belongs to {author.username}, You cannot delete this.", "danger")
        return redirect(url_for('blog.home'))

    db.session.delete(posts)
    db.session.commit()
    flash("Post deleted successfully!", "success")
    return redirect(url_for('blog.home'))

@blog.route('/edit/<int:post_id>', methods=['GET', 'POST'])
def edit(post_id):
    post = Post.query.get_or_404(post_id)
    if post.user_id != current_user.id:
       author = User.query.get_or_404(post.user_id)
       flash(f"This post belongs to {author.username}, You cannot edit this.", "danger")
       return redirect(url_for('blog.home'))
     
    if request.method == 'POST':
        post.title = request.form.get('title')
        post.content = request.form.get('content')
        db.session.commit()
        return redirect(url_for('blog.home'))
    return render_template('edit.html', post=post)


@blog.route('/projects')
@login_required
def projects():
    projects = [
        {'name':'Blog','status':'Completed'},
        {'name':'Status','status':'In Progress'},
        {'name':'Chatbot','status':'Planned'}
        ]
    return render_template('projects.html',projects=projects)

@blog.route('/contact',methods=['GET','POST'])
@login_required
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        message = request.form.get('message')
        return render_template('thanks.html',name=name,message=message)
    return render_template('contact.html')

@blog.route('/register',methods = ['GET','POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = bcrypt.generate_password_hash(request.form.get('password')).decode('utf-8')
        user = User(username = username , password = password)
        db.session.add(user)
        db.session.commit()
        flash('Account Registred Successfully, Confirmation Email sent!','success')
        return redirect(url_for('blog.login'))
    
    return render_template('register.html')

@blog.route('/login',methods = ['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password,password):
            login_user(user)
            flash('Welcome!')
            return redirect(url_for('blog.home'))
        else:
            flash('Invalid username or password','danger')
            return redirect(url_for('blog.login'))
    return render_template('login.html')
    

@blog.route('/logout')
@login_required
def logout():
    logout_user()
    flash('logout successfully','info')
    return redirect(url_for('blog.login'))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))