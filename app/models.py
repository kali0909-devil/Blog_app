from flask_login import UserMixin
from . import db

class User(db.Model,UserMixin):
    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(150),unique = True, nullable = False)
    password = db.Column(db.String(100),nullable = False)

class Post(db.Model):
     post_id = db.Column(db.Integer,primary_key = True)
     title = db.Column(db.String(150), nullable = False)
     content = db.Column(db.String(100),nullable = False)