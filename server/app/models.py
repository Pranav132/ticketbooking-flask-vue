from app import db
from datetime import datetime, timedelta
from sqlalchemy import DateTime
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    email = db.Column(db.String(120), index=True, unique=True)  
    is_admin = db.Column(db.Boolean, default=False)
    reviews = db.relationship('Review', back_populates='user')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password, method='sha256')

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Theatre(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    place = db.Column(db.String(128))
    capacity = db.Column(db.Integer)
    shows = db.relationship('Show', backref='theatre', lazy='dynamic')


    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'place': self.place,
            'capacity':self.capacity,
            'shows': [show.to_dict() for show in self.shows[:3]] 
        }

# Create a helper table 'showtags' for many-to-many relationship between Show and Tag
showtags = db.Table('showtags',
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True),
    db.Column('show_id', db.Integer, db.ForeignKey('show.id'), primary_key=True)
)

class Show(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    # tags = db.Column(db.String(128))
    ticket_price = db.Column(db.Float)
    theatre_id = db.Column(db.Integer, db.ForeignKey('theatre.id'))
    start_time = db.Column(db.DateTime)
    duration = db.Column(db.Time) # duration in hours and minutes
    tags = db.relationship('Tag', secondary=showtags, lazy='subquery',
        backref=db.backref('shows', lazy=True))
    reviews = db.relationship('Review', back_populates='show')
    capacity = db.Column(db.Integer)

    @property
    def end_time(self):
        return self.start_time + timedelta(hours=self.duration.hour, minutes=self.duration.minute)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'ticket_price': self.ticket_price,
            'theatre_id': self.theatre_id,
            'start_time': self.start_time.strftime('%Y-%m-%d %H:%M:%S'),  # converting datetime object to string
            'duration': str(self.duration),  # converting time object to string
            'end_time': self.end_time.strftime('%Y-%m-%d %H:%M:%S'),  # using the end_time property and converting datetime object to string
            'tags': [tag.to_dict() for tag in self.tags], 
            'reviews': [review.to_dict() for review in self.reviews],
            'capacity': self.capacity
        }
        
    
class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, index=True)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
        }

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    show_id = db.Column(db.Integer, db.ForeignKey('show.id'))
    number_of_tickets = db.Column(db.Integer)

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'show_id': self.show_id,
            'number_of_tickets': self.number_of_tickets
        }

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False)
    text = db.Column(db.Text, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    show_id = db.Column(db.Integer, db.ForeignKey('show.id'), nullable=False)

    user = db.relationship('User', back_populates='reviews')
    show = db.relationship('Show', back_populates='reviews')

    def to_dict(self):
        return {
            'id': self.id,
            'rating': self.rating,
            'text': self.text,
            'user_id': self.user_id,
            'show_id': self.show_id,
        }