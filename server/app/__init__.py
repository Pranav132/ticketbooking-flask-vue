from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from .routes import main
from flask_cors import CORS
from celery import Celery
from datetime import timedelta
from celery.schedules import crontab

# Initialize Extensions
db = SQLAlchemy()
jwt = JWTManager()
celery = Celery(__name__, broker='redis://localhost:6379', backend='redis://localhost:6379')

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ticket_booking.db'
    app.config['JWT_SECRET_KEY'] ='6c7bf36236b2d12c3341541cd4b89da870ff1f8684f75dd1ca19f960dce5c9bd'

    db.init_app(app)
    jwt.init_app(app)
    CORS(app)

    from .celery_config import celery as celery_task

    celery_task.conf.update(app.config)
        
    class ContextTask(celery_task.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)
                    
    celery_task.Task = ContextTask

    celery_task.conf.beat_schedule = {
        'send-reminders-every-evening': {
            'task': 'app.tasks.send_daily_reminders',
            'schedule': timedelta(days=1),
            'args': ()
        },
        'send-monthly-reports': {
            'task': 'app.tasks.send_monthly_reports',
            'schedule': crontab(day_of_month='1', hour='0', minute='0'),
            'args': ()
        },
        'test-celery':{
            'task': 'app.tasks.simple_task',
            'schedule': timedelta(seconds=1),
            'args': ()
        }
    }

    with app.app_context():
        from . import routes
        from . import models

    app.register_blueprint(main)

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
