from flask_sqlalchemy import SQLAlchemy # type: ignore
from flask_bcrypt import Bcrypt # type: ignore
from flask_login import LoginManager # type: ignore
from flask_mail import Mail # type: ignore
from flask_wtf import CSRFProtect # type: ignore
from flask_dance.contrib.google import make_google_blueprint# type: ignore
from .config import Config


db = SQLAlchemy()
login_manager = LoginManager()
bcrypt = Bcrypt()
mail = Mail()
csrf = CSRFProtect()

google_bp = make_google_blueprint(
    client_id=Config.GOOGLE_CLIENT_ID, # Loaded from config later
    client_secret=Config.GOOGLE_CLIENT_SECRET,  # Loaded from config later
    scope=["profile", "email"],
    redirect_to="auth.google_login"  # The endpoint to redirect to after login
)