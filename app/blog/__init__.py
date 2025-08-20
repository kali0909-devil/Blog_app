from flask import Blueprint # type: ignore

blog_bp = Blueprint('blog', __name__, template_folder='templates', static_folder='static', static_url_path='/static')

from . import routes