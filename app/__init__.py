from flask import Flask # type: ignore
from .extentions import db, login_manager, bcrypt, mail
from .config import Config
from .blog import blog_bp
from .auth import auth_bp



def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    db.init_app(app)
    bcrypt.init_app(app)
    mail.init_app(app)
    app.register_blueprint(blog_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'info'
    
    from .models import load_user
    
   
    


    return app