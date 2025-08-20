from flask import Flask  # type: ignore
from .extentions import db, login_manager, bcrypt, mail, csrf, google_bp
from .config import Config
from .blog import blog_bp
from .auth import auth_bp
from flask_migrate import Migrate

migrate = Migrate()   # ✅ create migrate instance


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    bcrypt.init_app(app)
    mail.init_app(app)
    csrf.init_app(app)

    # Register blueprints
    app.register_blueprint(blog_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(google_bp, url_prefix='/auth/google_login')

    # Login manager
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'info'

    # Flask-Migrate
    migrate.init_app(app, db)   # ✅ better way

    from .models import load_user  # to register user loader

    return app
