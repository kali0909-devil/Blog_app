from flask import Flask # type: ignore
from flask_login import LoginManager # type: ignore
from flask_sqlalchemy import SQLAlchemy # type: ignore
from flask_bcrypt import Bcrypt # type: ignore

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'ajinkya123'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'blog.login'
    

    from .routes import blog
    
    app.register_blueprint(blog)

    


    return app