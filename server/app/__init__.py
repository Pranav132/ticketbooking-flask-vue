from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from .routes import main

# Initialize Extensions
db = SQLAlchemy()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ticket_booking.db'
    app.config['JWT_SECRET_KEY'] = 'your-secret-key'  # Replace with your secret key

    db.init_app(app)
    jwt.init_app(app)

    with app.app_context():
        from . import routes

    app.register_blueprint(main)

    return app

# If this file is executed directly, start the Flask development server
if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
