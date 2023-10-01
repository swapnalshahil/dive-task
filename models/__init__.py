from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .user import User
from .entry import Entry
