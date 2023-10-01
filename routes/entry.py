'''
    Routes related to entries
'''
from flask import Blueprint, request, jsonify, g
from models.entry import Entry
from models.user import User
from .auth import auth_bp, login_required, admin_required, manager_required
import requests
from datetime import date, datetime

# Create a blueprint for entry routes
entry_bp = Blueprint("entry_bp", __name__)

'''
    API: http://localhost:5000/entries
    API to get all entries if admin access else their own records only
    arguments can be used to filter like
    Example - http://localhost:5000/entries?per_page=2&user_name=manager1&page=2
    method: GET
'''
@entry_bp.route("/entries", methods=["GET"])
@login_required
def get_entries():
    """Get all entries."""
    current_user = g.current_user
    page = request.args.get("page", default=1, type=int)
    per_page = request.args.get("per_page", default=10, type=int)
    user_name = request.args.get("username")
    food = request.args.get("food")

    query = Entry.query

    if current_user.role == "admin":
        if user_name:
            query = query.join(User).filter(User.name.ilike(f"%{user_name}%"))
        if food:
            query = query.filter(Entry.text.ilike(f"%{food}%"))
        entries = query.paginate(page=page, per_page=per_page)
    else:
        query = query.filter_by(user_id=current_user.id)
        if user_name:
            query = query.join(User).filter(User.name.ilike(f"%{user_name}%"))
        if food:
            query = query.filter(Entry.text.ilike(f"%{food}%"))
        entries = query.paginate(page=page, per_page=per_page)

    result = [entry.serialize() for entry in entries.items]
    return jsonify({
        "entries": result,
        "total_entries": entries.total,
        "current_page": entries.page,
        "per_page": entries.per_page,
        "has_next": entries.has_next,
        "has_prev": entries.has_prev
    })

'''
    API: http://localhost:5000/entries/<entry_id>
    API to get a particular entry 
    Admin can Read any entry, others can only Read their own entry
    method: GET
'''
@entry_bp.route("/entries/<entry_id>", methods=["GET"])
@login_required
def get_entry(entry_id):
    """Get a specific entry."""
    current_user = g.current_user

    if current_user.role == 'regular' or current_user.role == 'manager':
        entry = Entry.query.filter_by(user_id=current_user.id).filter_by(id=entry_id).first()
        if not entry:
            return jsonify({"message": "Entry not found"}), 404
        return jsonify(entry.serialize())

    entry = Entry.query.get(entry_id)
    if not entry:
        return jsonify({"message": "Entry not found"}), 404

    return jsonify(entry.serialize())

'''
    API: http://localhost:5000/entries
    API to create a new entry
    method: POST
    {
        "text": "4 bowls chicken",
        "calories": 1000,       //optional
        "date": "2023-06-18",   //optional
        "time": "18:34"         //optional
    }
'''
@entry_bp.route("/entries", methods=["POST"])
@login_required
def create_entry():
    """Create a new entry."""
    data = request.json
    current_user = g.current_user
    user_id = None
    if current_user:
        user_id = current_user.id
    else:
        user_id = data.get("user_id")

    if not user_id:
        return jsonify({"message": "User not found"}), 404

    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404
    
    _date = data.get('date')
    _time = data.get('time')

    if _date is None:
        _date = date.today()
    if _time is None:
        _time = datetime.now().time()

    entry = Entry(
        date=_date,
        time=_time,
        text=data.get("text"),
        calories=data.get("calories"),
        user_id=user_id
    )  
    entry.save()
    return jsonify(entry.serialize()), 201

'''
    API: http://localhost:5000/entries/<entry_id>
    API to Update existing entry
    All entry Update Access to admin, for other roles only update to their records
    method: PUT
    {
        "text": "4 bowls chicken",
        "calories": 1000,       //optional
        "date": "2023-06-18",   //optional
        "time": "18:34"         //optional
    }
'''
@entry_bp.route("/entries/<entry_id>", methods=["PUT"])
@login_required
def update_entry(entry_id):
    """Update a specific entry."""
    current_user = g.current_user

    if current_user.role == 'regular' or current_user.role == 'manager':
        entry = Entry.query.filter_by(user_id=current_user.id).filter_by(id=entry_id).first()
    elif current_user.role == 'admin':
        entry = Entry.query.get(entry_id)

    if not entry:
        return jsonify({"message": "Entry not found"}), 404

    data = request.json

    # Validate and convert the date input to Python's date format
    date_str = data.get("date", entry.date)
    if date_str is None:
        date_str = date.today()

    # Validate and convert the time input to Python's time format
    time_str = data.get("time", entry.time)
    if time_str is None:
        time_str =  datetime.now().time()

    # Update the entry with the validated date and time
    entry.date = date_str
    entry.time = time_str
    entry.text = data.get("text", entry.text)
    entry.calories = data.get("calories")
    entry.save()

    return jsonify(entry.serialize())

'''
    API: http://localhost:5000/entries/<entry_id>
    API to Delete existing entry
    Delete Access for any entry given to admin, for other roles only delete to their records
    method: DELETE
'''
@entry_bp.route("/entries/<entry_id>", methods=["DELETE"])
@login_required
def delete_entry(entry_id):
    """Delete a specific entry."""
    current_user = g.current_user
    if current_user.role == 'regular' or current_user.role == 'manager':
        entry = Entry.query.filter_by(user_id=current_user.id).filter_by(id=entry_id).first()
    elif current_user.role == 'admin':
        entry = Entry.query.get(entry_id)

    if not entry:
        return jsonify({"message": "Entry not found"}), 404

    entry.delete()
    return jsonify({"message": "Entry deleted"}), 200
