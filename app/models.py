from app import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    is_admin = db.Column(db.Boolean, default=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Theatre(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    place = db.Column(db.String(128))
    capacity = db.Column(db.Integer)
    shows = db.relationship('Show', backref='theatre', lazy='dynamic')

# Create a helper table 'showtags' for many-to-many relationship between Show and Tag
showtags = db.Table('showtags',
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True),
    db.Column('show_id', db.Integer, db.ForeignKey('show.id'), primary_key=True)
)

class Show(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    rating = db.Column(db.Float)
    tags = db.Column(db.String(128))
    ticket_price = db.Column(db.Float)
    theatre_id = db.Column(db.Integer, db.ForeignKey('theatre.id'))
    tags = db.relationship('Tag', secondary=showtags, lazy='subquery',
        backref=db.backref('shows', lazy=True))
    
class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, index=True)

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    show_id = db.Column(db.Integer, db.ForeignKey('show.id'))
    number_of_tickets = db.Column(db.Integer)
