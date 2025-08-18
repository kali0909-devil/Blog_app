from flask_login import UserMixin # type: ignore
from .extentions import login_manager
from . import db
from .static import images

class User(db.Model,UserMixin):
    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(150),unique = True, nullable = False)
    email = db.Column(db.String(150),unique = True, index = True , nullable = False)
    password = db.Column(db.String(100),nullable = False)
    posts = db.relationship('Post', backref='user', lazy=True)

class Post(db.Model,UserMixin):
     post_id = db.Column(db.Integer,primary_key = True)
     title = db.Column(db.String(150), nullable = False)
     content = db.Column(db.String(100),nullable = False)
     image = db.Column(db.String(500),nullable = True)
     reference = db.Column(db.String(500),nullable = True)
     user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))