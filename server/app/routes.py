from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from functools import wraps
from datetime import datetime, timedelta
from sqlalchemy import or_

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

def overlapping_shows(theatre_id, start_time, end_time, excluding_show_id=None):
    """ 
    Return overlapping shows for given theatre_id, start_time and end_time. 
    excluding_show_id can be provided to exclude a show (useful for the edit case).
    """
    from .models import Show
    
    # Fetch all shows for the theatre
    all_shows = Show.query.filter(Show.theatre_id == theatre_id).all()

    # Filter shows that overlap with the given time frame
    overlapping = [
        show for show in all_shows
        if (show.start_time < end_time and show.end_time > start_time) and show.id != excluding_show_id
    ]
    
    return overlapping


@main.route('/show', methods=['POST'])
@jwt_required()
@admin_required
def add_show():
    '''
    Route to create a new show
    User must be authenticated as an admin
    '''

    from .models import Show, Tag, Theatre
    from . import db

    try:
        data = request.get_json()
        start_time = datetime.strptime(data['startTime'], '%Y-%m-%dT%H:%M')
        duration = datetime.strptime(data['duration'], '%H:%M').time() # convert the string to time

        end_time = start_time + timedelta(hours=duration.hour, minutes=duration.minute)
        if overlapping_shows(data['theatreId'], start_time, end_time):
            return jsonify({'message': 'Another show is scheduled during this time at the given theatre.'}), 400

        new_show = Show(name=data['name'], ticket_price=data['ticketPrice'], theatre_id=data['theatreId'], start_time=start_time, duration=duration)

        # getting capacity
        theatre = Theatre.query.get(data['theatreId'])
        if not theatre:
            return jsonify({'message': 'Theatre not found.'}), 404
        
        new_show.capacity = theatre.capacity
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
        print(data)
        show = Show.query.get_or_404(show_id)
        show.name = data.get('name', show.name)
        show.ticket_price = data.get('ticketPrice', show.ticket_price)
        show.theatre_id = data.get('theatreId', show.theatre_id)

        if 'startTime' in data:
            print(data['startTime'])
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

        end_time = show.start_time + timedelta(hours=show.duration.hour, minutes=show.duration.minute)
        if overlapping_shows(show.theatre_id, show.start_time, end_time, excluding_show_id=show_id):
            return jsonify({'message': 'Another show is scheduled during this time at the given theatre.'}), 400

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

    # Check if the booking is made at least 30 minutes before the show start time
    if datetime.utcnow() + timedelta(minutes=30) >= show.start_time:
        return jsonify({'message': 'You can only book at least 30 minutes before the show start time.'}), 400

    # Check if there are enough seats available for the specific show
    if show.capacity < num_tickets:
        return jsonify({'message': 'Not enough seats available.'}), 400

    user_id = get_jwt_identity()
    booking = Booking(user_id=user_id, show_id=show_id, number_of_tickets=num_tickets)
    db.session.add(booking)
    show.capacity -= num_tickets  
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
            'show_timing': show.start_time.strftime('%Y-%m-%d %H:%M:%S') if show.start_time else None,
            'show_duration': show.duration.strftime('%H:%M') if show.duration else None ,
            'theatre_name': theatre.name,
            'theare_place': theatre.place,
            'number_of_tickets': booking.number_of_tickets
        })

    return jsonify(result)

@main.route('/shows/<int:show_id>/review', methods=['POST'])
@jwt_required()
def add_review(show_id):
    from .models import Review, Show, Booking
    from . import db

    # Get the user's ID from the JWT token
    user_id = get_jwt_identity()

    # Check if the show exists
    show = Show.query.get(show_id)
    if not show:
        return jsonify({'message': 'Show not found'}), 404

    # Validate user has booked the show
    user_booking = Booking.query.filter_by(user_id=user_id, show_id=show_id).first()
    if not user_booking:
        return jsonify({'message': 'You must book and watch the show before reviewing'}), 403

    # Check if the current time is past the show's end time
    if datetime.utcnow() < show.end_time:
        return jsonify({'message': 'You can only review after the show has ended'}), 403

    # Parse request data
    data = request.get_json()

    # Validate data
    if not data:
        return jsonify({'message': 'No input data provided'}), 400
    if 'rating' not in data:
        return jsonify({'message': 'Rating is required'}), 400
    if not (1 <= data['rating'] <= 5):  # Assuming a rating from 1 to 5
        return jsonify({'message': 'Rating must be between 1 and 5'}), 400

    # Check if the user has already reviewed this show
    existing_review = Review.query.filter_by(user_id=user_id, show_id=show_id).first()
    if existing_review:
        return jsonify({'message': 'You have already reviewed this show'}), 400

    # Create a new review
    review = Review(
        rating=data['rating'],
        text=data.get('text', ''),  # It's okay if the text is empty or not provided
        user_id=user_id,
        show_id=show_id
    )

    # Add to database
    db.session.add(review)
    db.session.commit()

    return jsonify({'message': 'Review added successfully', 'review': review.to_dict()}), 201

@main.route('/booking/<int:booking_id>', methods=['GET'])
@jwt_required()
def get_booking_details(booking_id):
    from .models import Booking, Show

    try:
        booking = Booking.query.get(booking_id)
        
        # Check if booking exists
        if not booking:
            return jsonify({"message": "Booking not found."}), 404

        # Assuming you have a to_dict() method in your Booking model
        booking_details = booking.to_dict()

        # Fetch show details
        show = Show.query.get(booking.show_id)
        if show:
            booking_details['show'] = show.to_dict()

        return jsonify(booking_details), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500
    

@main.route('/show/<int:show_id>/reviews', methods=['GET'])
@jwt_required()
def get_show_reviews(show_id):
    from .models import Review, Show

    try:
        reviews = Review.query.filter_by(show_id=show_id).all()

        show = Show.query.get(show_id)
        if not show:
            return jsonify({"message": "Show not found"}), 404
        show_name = show.name
        
        # Transforming the reviews into a list of dictionaries for jsonify to handle
        reviews_list = [review.to_dict() for review in reviews]
        
        return jsonify({"show_name": show_name, "reviews": reviews_list}), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500

@main.route('/summary', methods=['GET'])
@jwt_required()
@admin_required
def get_summary():
    from .models import User, Show, Theatre, Booking, Review
    from . import db

    try:
        total_users = User.query.count()
        total_theatres = Theatre.query.count()
        total_shows = Show.query.count()
        total_bookings = Booking.query.count()
        total_reviews = Review.query.count()
        
        # Calculate the average rating from all reviews
        avg_rating = db.session.query(db.func.avg(Review.rating)).scalar()

        # Get the top 3 shows based on the number of bookings
        top_shows = db.session.query(Show.name, db.func.sum(Booking.number_of_tickets).label('total_tickets')).\
                    join(Booking, Booking.show_id == Show.id).\
                    group_by(Show.name).\
                    order_by(db.desc('total_tickets')).\
                    limit(3).\
                    all()

        # Get the top 3 users who have written the most reviews
        top_reviewers = db.session.query(User.username, db.func.count(Review.id).label('total_reviews')).\
                        join(Review, Review.user_id == User.id).\
                        group_by(User.username).\
                        order_by(db.desc('total_reviews')).\
                        limit(3).\
                        all()

        return jsonify({
            'total_users': total_users,
            'total_theatres': total_theatres,
            'total_shows': total_shows,
            'total_bookings': total_bookings,
            'total_reviews': total_reviews,
            'average_rating': float(avg_rating) if avg_rating else None,
            'top_shows': [{'show_name': s[0], 'tickets_booked': s[1]} for s in top_shows],
            'top_reviewers': [{'user_name': u[0], 'reviews_written': u[1]} for u in top_reviewers]
        }), 200

    except Exception as e:
        return jsonify({"message": str(e)}), 500
