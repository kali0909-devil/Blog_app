from flask_login import UserMixin,current_user
from . import db

class User(db.Model,UserMixin):
    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(150),unique = True, nullable = False)
    password = db.Column(db.String(100),nullable = False)
    posts = db.relationship('Post', backref='user', lazy=True)

class Post(db.Model,UserMixin):
     post_id = db.Column(db.Integer,primary_key = True)
     title = db.Column(db.String(150), nullable = False)
     content = db.Column(db.String(100),nullable = False)
     user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    