
from flask import Blueprint, render_template, request, redirect, url_for, flash # type: ignore
from flask_login import login_required, current_user # type: ignore
from ..models import Post, User
from .. import db
from . import blog_bp as blog

@blog.route('/')
@login_required
def home():
    posts = Post.query.all()
    return render_template('blog.html',posts=posts)

@blog.route('/dashboard')
@login_required
def dashboard():
   user = current_user
   username = user.username
   email = user.email
   post_count = Post.query.filter_by(user_id=current_user.id).count()
   user_posts = Post.query.filter_by(user_id=current_user.id).all()
   return render_template('dashboard.html', posts=user_posts,username=username, email=email, post_count=post_count)
        
@blog.route('/new', methods=['GET', 'POST'])
@login_required
def new_post():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        image_url = request.form.get('image_url')  # image field from form
        reference_url = request.form.get('reference_url')  # reference field from form

        # Create a new post instance
        new_post = Post(
            title=title,
            content=content,
            user_id=current_user.id,
            image=image_url if image_url else None,
            reference=reference_url if reference_url else None
        )
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for('blog.home'))
    return render_template('new_post.html')

@blog.route("/post/<int:post_id>")
def post_detail(post_id):
    post = Post.query.get_or_404(post_id)
    author = User.query.get_or_404(post.user_id)
    return render_template("post.html", post=post,author=author.username)

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
        post.image = request.form.get('image_url')  # image field from form
        post.reference = request.form.get('reference_url')  # reference field from form
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


