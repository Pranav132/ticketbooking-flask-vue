To run

First start redis
Next

1. You are in server directory
2. source venv/bin/activate

In three separate terminals^

python run.py
celery -A app.tasks.celery beat --loglevel=info  
celery -A app.tasks.celery worker --loglevel=info
