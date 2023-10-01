'''User model definition and methods'''

from . import db
from flask import current_app
from werkzeug.security import generate_password_hash, check_password_hash
from .entry import Entry

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(50), nullable=False)
    expected_daily_calories = db.Column(db.Integer, nullable=False, default=2000)

    '''Setting up one to many relationship between User and Entry model'''
    entries = db.relationship('Entry', back_populates='user', cascade='all, delete-orphan')

    def __init__(self, name, email, password_hash, role='regular', expected_daily_calories=None):
        self.name = name
        self.email = email
        self.password_hash = password_hash
        self.role = role
        self.expected_daily_calories = expected_daily_calories

    '''
        password method is defined to raise an AttributeError 
        to prevent accessing the password attribute directly
    '''
    @property
    def password(self):
        raise AttributeError('Password is write-only.')

    @password.setter
    def password(self, password):
        # Hash the password and store the hash
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        # Verify the provided password with the stored hash
        return check_password_hash(self.password_hash, password)

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'role': self.role,
            'expected_daily_calories': self.expected_daily_calories
        }

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def save(self):
        db.session.add(self)
        db.session.commit()

'''
    SQLAlchemy event listener that is triggered after a User object is deleted from the database. 
    It performs a cascading delete operation on the associated Entry objects.
'''
@db.event.listens_for(User, 'after_delete')
def delete_user_entries(mapper, connection, target):
    connection.execute(
        Entry.__table__.delete().where(Entry.user_id == target.id)
    )
