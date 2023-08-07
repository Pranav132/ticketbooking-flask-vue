from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from functools import wraps
from datetime import datetime

def admin_required(f):
    '''
    Decorator to ensure that a user accessing an admin route is authenticated as an admin
    '''
    @wraps(f)
    def decorated_function(*args, **kwargs):
        from .models import User
        current_user = User.query.get(get_jwt_identity())
        if not current_user.is_admin:
            return jsonify({'message': 'Only admins are allowed!'}), 403
        return f(*args, **kwargs)
    return decorated_function

main = Blueprint('main', __name__)

# DELETE LATER FOR REFERENCE
@main.route('/')
def index():
    from . import db
    return jsonify(message="Hello, World!")

@main.route('/admin-endpoint', methods=['GET'])
@jwt_required()
@admin_required
def protected_admin_route():
    return "Hi Admin!", 200

# END DELETE LATER

@main.route('/signup', methods=['POST'])
def signup():
    '''
    Signup Route
    '''
    # importing inside route to avoid circular imports
    from . import db
    from .models import User

    data = request.get_json()

    # Check if username or email already exists
    existing_user = User.query.filter((User.username==data['username']) | (User.email==data['email'])).first()
    if existing_user:
        return jsonify({'message': 'User already exists'}), 400

    new_user = User(username=data['username'], email=data['email'])
    new_user.set_password(data['password'])
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'Registered successfully'}), 201

@main.route('/login', methods=['POST'])
def login():
    '''
    Default user login route
    '''
    from .models import User
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()

    if not user:
        return jsonify({'message': 'User not found.'}), 401

    if not user.check_password(data['password']):
        return jsonify({'message': 'Incorrect password.'}), 401

    access_token = create_access_token(identity=user.id)
    return jsonify(access_token=access_token), 200

@main.route('/theatre', methods=['POST'])
@jwt_required()
@admin_required
def add_theatre():
    '''
    Route to add a theatre \n
    User must be authenticated as admin
    '''
    from .models import Theatre
    from . import db
    data = request.get_json()
    new_theatre = Theatre(name=data['name'], place=data['place'], capacity=data['capacity'])
    db.session.add(new_theatre)
    db.session.commit()
    return jsonify({'message': 'New theatre created'}), 201


@main.route('/theatre/<int:theatre_id>', methods=['PUT'])
@jwt_required()
@admin_required
def edit_theatre(theatre_id):
    '''
    Route to edit existing theatre \n
    User must be authenticated as an admin user
    '''

    from .models import Theatre
    from . import db

    data = request.get_json()
    theatre = Theatre.query.get_or_404(theatre_id)
    theatre.name = data.get('name', theatre.name)
    theatre.place = data.get('place', theatre.place)
    theatre.capacity = data.get('capacity', theatre.capacity)
    db.session.commit()
    return jsonify({'message': 'Theatre updated'}), 200


@main.route('/theatre/<int:theatre_id>', methods=['DELETE'])
@jwt_required()
@admin_required
def delete_theatre(theatre_id):
    '''
    Route to delete an existing theatre \n
    User must be authenticated as admin
    '''

    from .models import Theatre
    from . import db

    theatre = Theatre.query.get_or_404(theatre_id)
    db.session.delete(theatre)
    db.session.commit()

    return jsonify({'message': 'Theatre deleted'}), 200


@main.route('/show', methods=['POST'])
@jwt_required()
@admin_required
def add_show():
    '''
    Route to create a new show
    User must be authenticated as an admin
    '''

    from .models import Show
    from . import db

    data = request.get_json()
    start_time = datetime.strptime(data['start_time'], '%Y-%m-%d %H:%M:%S') # convert the string to datetime
    duration = datetime.strptime(data['duration'], '%H:%M').time() # convert the string to time
    new_show = Show(name=data['name'], rating=data['rating'], ticket_price=data['ticket_price'], theatre_id=data['theatre_id'], start_time=start_time, duration=duration)
    db.session.add(new_show)
    db.session.commit()

    return jsonify({'message': 'New show created'}), 201

@main.route('/show/<int:show_id>', methods=['PUT'])
@jwt_required()
@admin_required
def edit_show(show_id):
    '''
    Route to edit an existing show
    User must be authenticated as an admin
    '''

    from .models import Show
    from . import db

    data = request.get_json()
    show = Show.query.get_or_404(show_id)
    show.name = data.get('name', show.name)
    show.rating = data.get('rating', show.rating)
    show.ticket_price = data.get('ticket_price', show.ticket_price)
    show.theatre_id = data.get('theatre_id', show.theatre_id)
    if 'start_time' in data:
        show.start_time = datetime.strptime(data['start_time'], '%Y-%m-%d %H:%M:%S') # convert the string to datetime
    if 'duration' in data:
        show.duration = datetime.strptime(data['duration'], '%H:%M').time() # convert the string to time
    db.session.commit()
    return jsonify({'message': 'Show updated'}), 200


@main.route('/show/<int:show_id>', methods=['DELETE'])
@jwt_required()
@admin_required
def delete_show(show_id):
    '''
    Route to delete an existing show \n
    User must be authenticated as an admin
    '''

    from .models import Show
    from . import db

    show = Show.query.get_or_404(show_id)
    db.session.delete(show)
    db.session.commit()

    return jsonify({'message': 'Show deleted'}), 200

