from flask import Blueprint
from flask import render_template

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

from . import routes