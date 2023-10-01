'''
    Routes related to authentication
'''
from flask import Blueprint, request, jsonify, current_app, g, abort
from werkzeug.security import generate_password_hash, check_password_hash
from models.user import User
import jwt
from functools import wraps
from flask_login import login_required, LoginManager

'''blueprint for auth'''
auth_bp = Blueprint('auth', __name__)

'''
    API: http://localhost:5000/register
    API to register any user
    method: POST
    {
        "name": "admin3",
        "email": "admin3@gmail.com",
        "password": "1234",
        "role": "admin"     // if role not given -> default is 'regular'
    }
'''
@auth_bp.route('/register', methods=['POST'])
def register():
    name = str(request.json.get('name'))
    email = str(request.json.get('email'))
    password = str(request.json.get('password'))
    role = str(request.json.get('role')) or 'regular'

    if role != 'regular' and role != 'manager' and role != 'admin':
        return jsonify({'message': 'Invalid role'}), 400

    # Validate input
    if not name or not email or not password:
        return jsonify({'message': 'Invalid input'}), 400

    # Check if the user already exists
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({'message': 'User already exists'}), 409

    # Create a new user
    hashed_password = generate_password_hash(password)
    new_user = User(name=name, email=email, password_hash=hashed_password, role=role)
    new_user.save()

    return jsonify({'message': 'registered successfully'}), 201

'''
    API: http://localhost:5000/login
    API to login
    method: POST
    {
        "email": "admin3@gmail.com",
        "password": "1234",
    }
'''
@auth_bp.route('/login', methods=['POST'])
def login():
    email = str(request.json.get('email'))
    password = str(request.json.get('password'))

    if not email or not password:
        return jsonify({'message': 'Invalid input'}), 400
    
    user = User.query.filter_by(email=email).first()

    if not user:
        return jsonify({'message': 'User does not exist'}), 404
    
    if not check_password_hash(user.password_hash, password):
        return jsonify({'message': 'Invalid credentials'}), 401
    
    print(f'{user.email} Login successful!')

    access_token = generate_access_token(user)

    return jsonify({'access_token': access_token}), 200

def generate_access_token(user):
    '''generate access token'''
    payload = {
        'user_id': user.id,
        'name': user.name,
        'email': user.email,
        'role': user.role
    }
    secret_key = current_app.config['SECRET_KEY']
    access_token = jwt.encode(payload, secret_key, algorithm='HS256')
    return access_token


# Decorator to check if the request is from an authenticated user
def login_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        # Get the access token from the request headers or cookies
        access_token = request.headers.get('Authorization')

        if not access_token:
            return jsonify({'message': 'Missing access token'}), 401

        try:
            # Verify and decode the access token
            secret_key = current_app.config['SECRET_KEY']
            payload = jwt.decode(access_token, secret_key, algorithms=['HS256'])
            user_id = payload.get('user_id')

            # Set the current user based on the user ID
            current_user = User.query.get(user_id)
            if not current_user:
                return jsonify({"message": "Invalid user"}), 401

            # Store the current user in the Flask global object (g)
            g.current_user = current_user

        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Expired access token'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Invalid access token'}), 401

        return func(*args, **kwargs)

    return decorated_function

def admin_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        # Check if the user is logged in and is an admin
        if not g.current_user or not g.current_user == 'admin':
            abort(403)  # Return 403 Forbidden if not an admin

        return func(*args, **kwargs)
    return decorated_function

def manager_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        # Check if the user is logged in and is a manager
        if not g.current_user or not g.current_user.role == 'manager':
            abort(403)

        return func(*args, **kwargs)
    return decorated_function