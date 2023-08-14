from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from functools import wraps
from datetime import datetime, timedelta
from sqlalchemy import or_, Time

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

    from .models import Show, Tag
    from . import db

    try:
        data = request.get_json()
        start_time = datetime.strptime(data['startTime'], '%Y-%m-%dT%H:%M')
        duration = datetime.strptime(data['duration'], '%H:%M').time() # convert the string to time
        new_show = Show(name=data['name'], ticket_price=data['ticketPrice'], theatre_id=data['theatreId'], start_time=start_time, duration=duration)
        tags_data = data['tags']
        tags = []
        for tag_name in tags_data:
            tag_name = tag_name.strip()  # Removing any leading or trailing whitespaces
            tag = Tag.query.filter_by(name=tag_name).first()
            if not tag:  # If tag doesn't exist, create it
                tag = Tag(name=tag_name)
                db.session.add(tag)
            tags.append(tag)

        new_show.tags = tags  # Add tags to show

        db.session.add(new_show)
        db.session.commit()

        return jsonify({'message': 'New show created'}), 201
    
    except Exception as e:
        return jsonify({'message': str(e)})

@main.route('/show/<int:show_id>', methods=['PUT'])
@jwt_required()
@admin_required
def edit_show(show_id):
    '''
    Route to edit an existing show
    User must be authenticated as an admin
    '''

    from .models import Show, Tag
    from . import db

    try:
        data = request.get_json()
        show = Show.query.get_or_404(show_id)
        show.name = data.get('name', show.name)
        show.ticket_price = data.get('ticketPrice', show.ticket_price)
        show.theatre_id = data.get('theatreId', show.theatre_id)

        if 'startTime' in data:
            show.start_time = datetime.strptime(data['startTime'], '%Y-%m-%dT%H:%M')
        if 'duration' in data:
            show.duration = datetime.strptime(data['duration'], '%H:%M').time() # convert the string to time

        if 'tags' in data:
            tags_data = data['tags']
            tags = []
            for tag_name in tags_data:
                tag_name = tag_name.strip()  # Removing any leading or trailing whitespaces
                tag = Tag.query.filter_by(name=tag_name).first()
                if not tag:  # If tag doesn't exist, create it
                    tag = Tag(name=tag_name)
                    db.session.add(tag)
                tags.append(tag)

            show.tags = tags  # Update tags of show

        db.session.commit()

        return jsonify({'message': 'Show updated successfully'}), 200

    except Exception as e:
        return jsonify({'message': str(e)}), 401

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

    for tag in show.tags:
        if len(tag.shows) == 1:  # Check if this is the only show with this tag
            db.session.delete(tag)

    db.session.delete(show)
    db.session.commit()

    return jsonify({'message': 'Show deleted'}), 200


@main.route('/search/theatre', methods=['GET'])
@jwt_required()
def search_theatre():
    from .models import Theatre
    location = request.args.get('location', '')
    capacity = request.args.get('capacity', '')
    name = request.args.get('name', '')
    if isinstance(capacity, int):
        capacity_value = capacity
    elif isinstance(capacity, str) and capacity.isdigit():
        capacity_value = int(capacity)
    else:
        capacity_value = 0
    theatres = Theatre.query.filter(Theatre.name.contains(name)).filter(Theatre.place.contains(location)).filter(Theatre.capacity >= capacity_value).all()
    return jsonify([theatre.to_dict() for theatre in theatres]), 200

# helper to check if a value is a number
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

@main.route('/search/show', methods=['GET'])
@jwt_required()
def search_show():
    from .models import Show, Review, Tag
    from . import db

    rating = request.args.get('rating', None)
    name = request.args.get('name', None)
    max_price = request.args.get('max_price', None)
    theatre_id = request.args.get('theatre_id')

    if not theatre_id:
        return jsonify({"error": "Theatre ID is required"}), 400

    query = Show.query.filter_by(theatre_id=theatre_id)
    
    tags = request.args.get('tag', "").split(',')
    tags_list = [tag.strip() for tag in tags if tag.strip()]

    if tags and tags != ['']:
        conditions = [Show.tags.any((Tag.name != None) & (Tag.name.ilike(f"%{tag.strip()}%"))) for tag in tags_list if tag]
        query = query.filter(or_(*conditions))

    if name:
        query = query.filter(Show.name.ilike(f'%{name}%'))

    if max_price:
        query = query.filter(Show.ticket_price <= float(max_price))
        

    if rating and is_number(rating):
        # Filter shows by their average rating
        subquery = db.session.query(Review.show_id, db.func.avg(Review.rating).label('avg_rating')).group_by(Review.show_id).subquery()
        query = query.join(subquery, subquery.c.show_id == Show.id).filter(subquery.c.avg_rating >= float(rating))

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

@main.route('/show/<int:show_id>', methods=['GET'])
@jwt_required()
def get_show(show_id):
    from .models import Show
    show = Show.query.get(show_id)
    if show is None:
        return jsonify({'message': 'Show not found.'}), 404
    return jsonify(show.to_dict()), 200

@main.route('/get_theatre_shows/<int:theatre_id>', methods=['GET'])
@jwt_required()
def get_shows_by_theatre(theatre_id):
    from .models import Show

    shows = Show.query.filter_by(theatre_id=theatre_id).all()

    # Convert each show to its dictionary representation
    shows_list = [show.to_dict() for show in shows]

    return jsonify(shows_list), 200

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

@main.route('/user/bookings', methods=['GET'])
@jwt_required()
def get_user_bookings():
    from .models import Show, Booking, Theatre
    from . import db

    # Get the user's ID from the JWT token
    user_id = get_jwt_identity()
    
    # Query for the user's bookings
    bookings = Booking.query.filter_by(user_id=user_id).all()

    # For each booking, get the associated Show and Theatre info
    result = []
    for booking in bookings:
        show = Show.query.get(booking.show_id)
        
        # Retrieve theatre information using the theatre_id from the Show model
        theatre = Theatre.query.get(show.theatre_id)
        
        result.append({
            'booking_id': booking.id,
            'show_name': show.name,
            'show_timing': show.start_time,
            'show_duration': show.duration,
            'theatre_name': theatre.name,
            'theare_place': theatre.place,
            'number_of_tickets': booking.number_of_tickets
        })

    return jsonify(result)
