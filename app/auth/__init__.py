from flask import Blueprint # type: ignore

auth_bp = Blueprint('auth', __name__, template_folder='templates')

from . import auth
