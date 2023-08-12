from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from .routes import main
from .celery import make_celery
from flask_cors import CORS

# Initialize Extensions
db = SQLAlchemy()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ticket_booking.db'
    app.config['JWT_SECRET_KEY'] ='6c7bf36236b2d12c3341541cd4b89da870ff1f8684f75dd1ca19f960dce5c9bd'

    db.init_app(app)
    jwt.init_app(app)
    CORS(app)
    app.config.update(
        CELERY_BROKER_URL='redis://localhost:6379',
        CELERY_RESULT_BACKEND='redis://localhost:6379',
    )
    celery = make_celery(app)

    with app.app_context():
        from . import routes
        from . import models

    app.register_blueprint(main)

    return app

# If this file is executed directly, start the Flask development server
if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
