from flask import Blueprint

main = Blueprint('main', __name__)
error_bp = Blueprint('error', __name__)

from . import views, errors

