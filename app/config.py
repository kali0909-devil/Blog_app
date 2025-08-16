import os
from datetime import timedelta
from dotenv import load_dotenv  # type: ignore

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") 
    SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI", "sqlite:///site.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    REMEMBER_COOKIE_DURATION = timedelta(days=7) 

    # Email config
    MAIL_SERVER = os.environ.get("MAIL_SERVER", "smtp.gmail.com")
    MAIL_PORT = int(os.environ.get("MAIL_PORT", 587))
    MAIL_USE_SSL = False
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")  # Gmail username
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")  # Gmail app password
    MAIL_DEFAULT_SENDER = os.environ.get("MAIL_DEFAULT_SENDER")  # Default sender email

    # Google OAuth Config
    GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID")
    GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET")
    OAUTHLIB_RELAX_TOKEN_SCOPE = True
    OAUTHLIB_INSECURE_TRANSPORT = True  # Disable in production!
