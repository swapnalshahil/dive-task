from flask import Blueprint

auth_bp = Blueprint('auth', __name__)
entry_bp = Blueprint('entry_bp', __name__)
users_bp = Blueprint('users', __name__, url_prefix='/users')

from .auth import *
from .entry import *
from .user import *
