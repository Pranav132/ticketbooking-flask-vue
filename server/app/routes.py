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

@main.route('/')
def index():
    from . import db
    return jsonify(message="Hello, World!")

@main.route('/admin-login', methods=['POST'])
def admin_login():
    '''
    Admin user login route
    '''
    from .models import User
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()

    if not user:
        return jsonify({'message': 'User not found.'}), 401

    if not user.check_password(data['password']):
        return jsonify({'message': 'Incorrect password.'}), 401
    
    if not user.is_admin:
        return jsonify({'message': 'User is not an admin.'}), 401

    access_token = create_access_token(identity=user.id)
    return jsonify(access_token=access_token), 200


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
    
    if user.is_admin:
        return jsonify({'message': 'Admin user - please login through admin form!'}), 401

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
    capacity = data['capacity']
    place = data['place']
    name = data['name']

    if isinstance(capacity, int):
        capacity_value = capacity
    elif isinstance(capacity, str) and capacity.isdigit():
        capacity_value = int(capacity)
    else:
        capacity_value = 0

    if not name or not place or not capacity:
        return jsonify({'message': 'Invalid data provided. Please try again'}), 400

    # Check for duplicate theatre based on name and place
    existing_theatre = Theatre.query.filter_by(name=name, place=place).first()
    if existing_theatre:
        return jsonify({'message': 'Theatre with the same name and place already exists'}), 400

    new_theatre = Theatre(name=name, place=place, capacity=capacity_value)
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


@main.route('/search/theatre', methods=['GET'])
@jwt_required()
def search_theatre():
    from .models import Theatre
    location = request.args.get('location', '')
    capacity = request.args.get('capacity', '')
    if isinstance(capacity, int):
        capacity_value = capacity
    elif isinstance(capacity, str) and capacity.isdigit():
        capacity_value = int(capacity)
    else:
        capacity_value = 0
    theatres = Theatre.query.filter(Theatre.place.contains(location)).filter(Theatre.capacity >= capacity_value).all()
    return jsonify([theatre.to_dict() for theatre in theatres]), 200


@main.route('/search/show', methods=['GET'])
@jwt_required()
def search_show():
    from .models import Show

    tag = request.args.get('tag', '')
    rating = request.args.get('rating', None)
    
    query = Show.query
    if tag:
        query = query.filter(Show.tags.any(name=tag))
    if rating:
        query = query.filter(Show.rating >= float(rating))

    shows = query.all()
    return jsonify([show.to_dict() for show in shows]), 200

@main.route('/theatre/<int:theatre_id>', methods=['GET'])
@jwt_required()
def get_theatre(theatre_id):
    from .models import Theatre
    theatre = Theatre.query.get(theatre_id)
    if theatre is None:
        return jsonify({'message': 'Theatre not found.'}), 404
    return jsonify(theatre.to_dict()), 200


@main.route('/book', methods=['POST'])
@jwt_required()
def book_show():
    from .models import Show, Booking
    from . import db
    data = request.get_json()
    show_id = data.get('show_id')
    num_tickets = data.get('num_tickets')
    show = Show.query.get(show_id)
    if show is None:
        return jsonify({'message': 'Show not found.'}), 404
    
    theatre = show.theatre
    if theatre.capacity < num_tickets:
        return jsonify({'message': 'Not enough seats available.'}), 400

    user_id = get_jwt_identity()
    booking = Booking(user_id=user_id, show_id=show_id, number_of_tickets=num_tickets)
    db.session.add(booking)
    theatre.capacity -= num_tickets
    db.session.commit()
    return jsonify({'message': 'Booking successful.'}), 200
