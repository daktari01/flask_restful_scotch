from flask import Blueprint

# An instance of Blueprint that represents authentication blueprint
auth_blueprint = Blueprint('auth', __name__)

from . import views