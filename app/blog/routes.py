
from flask import Blueprint, render_template, request, redirect, url_for, flash,current_app# type: ignore
from flask_login import login_required, current_user # type: ignore
from ..models import Post, User, Comment, Like # type: ignore 
from .. import db
from . import blog_bp as blog
import os
from werkzeug.utils import secure_filename # type: ignore
# Define the upload folder
UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', 'app/static/uploads')


# Home route for the blog
@blog.route('/')
@login_required
def home():
    posts = Post.query.all()
    return render_template('blog.html',posts=posts)

# Dashboard route for the user
@blog.route('/dashboard')
@login_required
def dashboard():
   user = current_user
   username = user.username
   email = user.email
   post_count = Post.query.filter_by(user_id=current_user.id).count()
   user_posts = Post.query.filter_by(user_id=current_user.id).all()
   return render_template('dashboard.html', posts=user_posts,username=username, email=email, post_count=post_count)

# Route to create a new post    
@blog.route('/new', methods=['GET', 'POST'])
@login_required
def new_post():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        image_url = request.form.get('image_url')
        reference_url = request.form.get('reference_url')
        select_img = None

        # Handle file upload
        if 'select_img' in request.files and request.files['select_img'].filename != '':
            file = request.files['select_img']
            filename = secure_filename(file.filename)
            upload_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            file.save(upload_path)
            select_img = filename

        # Validate required fields
        if not title or not content:
            flash('Title and content are required!', 'danger')
            return redirect(url_for('blog.new_post'))

        # Create post
        post = Post(
            title=title,
            content=content,
            user_id=current_user.id,
            image=image_url if image_url else None,
            select_img=select_img if select_img else None,
            reference=reference_url if reference_url else None
        )

        db.session.add(post)
        db.session.commit()
        flash('Post created successfully!', 'success')
        return redirect(url_for('blog.home'))

    # GET request renders the form
    return render_template('new_post.html')

# Route to view a specific post
@blog.route("/post/<int:post_id>")
def post_detail(post_id):
    post = Post.query.get_or_404(post_id)
    author = User.query.get_or_404(post.user_id)
    comments = Comment.query.filter_by(post_id=post_id).all()
    likes_count = Like.query.filter_by(post_id=post_id).count()
    liked = False
    if current_user.is_authenticated:
        liked = Like.query.filter_by(post_id=post_id, user_id=current_user.id).first() is not None

    return render_template("post.html", post=post, author=author.username, comments=comments, likes_count=likes_count, liked=liked)

# Route to delete a post
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

# Route to edit a post
@blog.route('/edit/<int:post_id>', methods=['GET', 'POST'])
@login_required
def edit(post_id):
    post = Post.query.get_or_404(post_id)

    if post.user_id != current_user.id:
        author = User.query.get_or_404(post.user_id)
        flash(f"This post belongs to {author.username}. You cannot edit this.", "danger")
        return redirect(url_for('blog.home'))

    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        image_url = request.form.get('image_url')
        reference_url = request.form.get('reference_url')
        file = request.files.get('select_img')

        if not title or not content:
            flash("Title and content are required.", "danger")
            return redirect(url_for('blog.edit', post_id=post_id))

        post.title = title
        post.content = content
        post.reference = reference_url
        if image_url:
            post.image = image_url

        if file and file.filename != "":
            filename = secure_filename(file.filename)
            file.save(os.path.join(current_app.config["UPLOAD_FOLDER"], filename))
            post.select_img = filename

        db.session.commit()
        flash("Post updated successfully!", "success")
        return redirect(url_for('blog.post_detail', post_id=post_id))

    return render_template('edit.html', post=post)

# Route to like or unlike a post
@blog.route('/like/<int:post_id>', methods=['POST'])
@login_required
def like(post_id):
    post = Post.query.get_or_404(post_id)  # safer, 404 if not found

    existing_like = Like.query.filter_by(post_id=post_id, user_id=current_user.id).first()
    
    if existing_like:
        db.session.delete(existing_like)
        db.session.commit()
        flash('You unliked this post.', 'success')
    else:
        new_like = Like(post_id=post_id, user_id=current_user.id)
        db.session.add(new_like)
        db.session.commit()
        flash('You liked this post.', 'success')
    
    
    return redirect(url_for('blog.post_detail', post_id=post_id,new_like=True, post=post))


# Route to view comments on a post
@blog.route('/comments/<int:post_id>', methods=['POST'])
@login_required
def comments(post_id):
    post = Post.query.get_or_404(post_id)
    if request.method == 'POST':
        content = request.form.get('content')
        if not content:
            flash('Comment cannot be empty.', 'danger')
            return redirect(url_for('blog.post_detail', post_id=post_id))
        new_comment = Comment(
            content=content,
            post_id=post_id,
            user_id=current_user.id
        )
        db.session.add(new_comment)
        db.session.commit()
        flash('Comment added successfully!', 'success')
        return redirect(url_for('blog.post_detail', post_id=post_id))
    
    comments = Comment.query.filter_by(post_id=post_id).all()
    return render_template('post.html', post=post, comments=comments)

# Delete a comment
@blog.route('/comment/delete/<int:comment_id>', methods=['POST'])
@login_required
def delete_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)

    # Only the comment author can delete
    if comment.user_id != current_user.id:
        flash("You cannot delete this comment.", "danger")
        return redirect(url_for('blog.post_detail', post_id=comment.post_id))

    db.session.delete(comment)
    db.session.commit()
    flash("Comment deleted successfully.", "success")
    return redirect(url_for('blog.post_detail', post_id=comment.post_id))

# Route to view all projects
@blog.route('/projects')
@login_required
def projects():
    projects = [
        {'name':'Blog','status':'Completed'},
        {'name':'Status','status':'In Progress'},
        {'name':'Chatbot','status':'Planned'}
        ]
    return render_template('projects.html',projects=projects)

# Route to contact the admin
@blog.route('/contact',methods=['GET','POST'])
@login_required
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        message = request.form.get('message')
        return render_template('thanks.html',name=name,message=message)
    return render_template('contact.html')


