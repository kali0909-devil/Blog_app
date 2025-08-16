from flask import Blueprint # type: ignore

blog_bp = Blueprint('blog', __name__)

from . import routes