'''
    Routes related to users
'''
from flask import Blueprint, request, jsonify, g, abort
from werkzeug.security import generate_password_hash
from models.user import User
import requests
from .auth import auth_bp, login_required, admin_required, manager_required


# Create blueprint for users routes
users_bp = Blueprint('users', __name__, url_prefix='/users')

'''
    API: http://localhost:5000/users/create
    API to create a new user by admin and manager
    method: POST
    {
        "name": "user6",
        "email": "user6@gmail.com",
        "password": "1234",
        "role": "regular"       // if role not given -> default is 'regular'
    }
'''
@users_bp.route('/create', methods=['POST'])
@login_required
def create_user():
    """Create a new user."""
    current_user = g.current_user
    if current_user.role == 'regular':
        return jsonify({'message': 'Unauthorized'}), 401
    
    data = request.json
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    role = data.get('role') or 'regular'

    if role not in ('regular', 'admin', 'manager'):
        return jsonify({'message': 'Invalid role'}), 400

    if not name or not email or not password:
        return jsonify({'message': 'Invalid input'}), 400

    # Check if the user already exists
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({'message': 'User already exists'}), 409

    hashed_password = generate_password_hash(password)

    new_user = User(name=name, email=email, password_hash=hashed_password, role=role)
    new_user.save()
    print(f'{new_user.name} created!')
    return jsonify(new_user.serialize()), 201

'''
    API: http://localhost:5000/users/<user_id>
    API to get user by user_id can be accessed by admin and manager only
    method: GET
'''
@users_bp.route('/<user_id>', methods=['GET'])
@login_required
def get_user(user_id):
    """Get a specific user."""
    current_user = g.current_user
    if current_user.role == 'admin' or current_user.role == 'manager':
        user = User.query.get(user_id)
        if not user:
            return jsonify({'message': 'User not found'}), 404

        return jsonify(user.serialize())

    return jsonify({'message': 'Unauthorized'}), 401

'''
    API: http://localhost:5000/users/list
    API to get a list of all users, access to manager and admin
    arguments can be used to filter with role,username,email
    Example - http://localhost:5000/users/list?role=regular&username=user4
    method: GET
'''
@users_bp.route('/list', methods=['GET'])
@login_required
def get_users():
    """Get a list of users."""
    current_user = g.current_user
    if current_user.role == 'regular':
        return jsonify({'message': 'Unauthorized'}), 401

    page = request.args.get('page', default=1, type=int)
    per_page = request.args.get('per_page', default=10, type=int)
    username = request.args.get('username')
    email = request.args.get('email')
    user_role = request.args.get('role')
    query = User.query

    if username:
        query = query.filter(User.name.ilike(f'%{username}%'))

    if email:
        query = query.filter(User.email.ilike(f'%{email}%'))

    if user_role:
        query = query.filter(User.role.ilike(f'%{user_role}%'))

    users = query.paginate(page=page, per_page=per_page)

    serialized_users = [users.serialize() for users in users.items]
    return jsonify({
        'users': serialized_users,
        'total_users': users.total,
        'current_page': users.page,
        'per_page': users.per_page,
        'total_pages': users.pages,
        'has_next': users.has_next,
        'has_prev': users.has_prev
    })


'''
    API: http://localhost:5000/users/<user_id>
    API to Update existing user, access to manager and admin
    method: PUT
    {
        "name": "user6",
        "email": "user6@gmail.com",
        "role": "regular"
    }
'''
@users_bp.route('/<user_id>', methods=['PUT'])
@login_required
def update_user(user_id):
    """Update a specific user."""
    current_user = g.current_user

    if current_user.role == 'regular':
        return jsonify({'message': 'Unauthorized'}), 401
    
    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': 'User not found'}), 404

    data = request.json
    user.name = data.get('name', user.name)
    user.email = data.get('email', user.email)
    user.role = data.get('role', user.role)
    user.save()

    return jsonify(user.serialize())

'''
    API: http://localhost:5000/users/<user_id>
    API to Delete existing user
    Admin can Delete any user,manager and admin
    Manager can Delete any user, but cannot delete any admin and manager
    User is Unauthorized to Delete any user
    method: DELETE
'''
@users_bp.route('/<user_id>', methods=['DELETE'])
@login_required
def delete_user(user_id):
 
    current_user = g.current_user

    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': 'User not found'}), 404

    if current_user.role == 'admin':
        user.delete()
        return jsonify({'message': 'User deleted'})

    if current_user.role == 'manager' and user.role == 'regular':
        user.delete()
        return jsonify({'message': 'User deleted'})
   
    return jsonify({'message': 'Unauthorized'}), 401

'''
    API: http://localhost:5000/users/expected-calories
    API to Update Daily Expected Calories for all users
    By Default it is 2000 while creating/registering user
    method: PUT
    {
        "expected_daily_calories" : 2500
    }
'''
@users_bp.route('/expected-calories', methods=['PUT'])
@login_required
def set_expected_calories():
    """Set the expected number of calories per day for a user."""
    current_user = g.current_user
    # print(current_user)
    user = User.query.get(current_user.id)
    if not user:
        return jsonify({'message': 'User not found'}), 404

    data = request.json
    expected_calories = data.get('expected_daily_calories')

    user.expected_daily_calories = expected_calories
    user.save()

    return jsonify({'message': 'Expected calories per day updated'})
