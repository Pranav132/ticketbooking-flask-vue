
from .celery_config import celery
from datetime import datetime, timedelta
import csv
from io import StringIO
import yagmail
import os
import time

USER = 'cnsendemails@gmail.com'
APP_PASSWORD = 'ktcfryrveizoqisb' # a token for gmail


def generate_csv_for_theatre(theatre):
    output = StringIO()
    writer = csv.writer(output)
    
    # Write header
    writer.writerow(['Show Name', 'Ticket Price', 'Start Time', 'Duration', 'End Time'])
    
    # Write data
    for show in theatre.shows:
        writer.writerow([show.name, show.ticket_price, show.start_time, show.duration, show.end_time])

    return output.getvalue()

def get_users_who_did_not_visit_or_book():
    from .models import Booking, User
    one_day_ago = datetime.utcnow() - timedelta(days=1)
    
    users_who_booked = Booking.query.filter(Booking.timestamp > one_day_ago).with_entities(Booking.user_id).all()
    booked_user_ids = [user[0] for user in users_who_booked]

    users_who_did_not_book = User.query.filter(User.id.notin_(booked_user_ids)).all()

    return users_who_did_not_book

def send_email(user, subject, message):
    with yagmail.SMTP(USER, APP_PASSWORD) as yag:
        yag.send(user.email, subject, message)
        print(f'Sent email to {user.email} successfully')

def generate_html_report_for_user(user):
    from .models import Booking
    one_month_ago = datetime.utcnow() - timedelta(days=30)

    user_bookings = Booking.query.filter_by(user_id=user.id).filter(Booking.timestamp > one_month_ago).all()
    
    # Convert this data to HTML (just a very basic version for illustration)
    html_data = f"<h1>Monthly Report for {user.username}</h1>"
    for booking in user_bookings:
        html_data += f"<p>Booked {booking.number_of_tickets} tickets for show {booking.show_id}.</p>"

    return html_data


@celery.task
def send_daily_reminders():
    users = get_users_who_did_not_visit_or_book() 
    html_data = "<h1>Hi, You have not visited today!</h1>" 
    for user in users:
       send_email(user, "Daily Reminder", html_data)

@celery.task
def send_monthly_reports():
    from .models import User
    users = User.query.all()
    for user in users:
        report = generate_html_report_for_user(user)  # Implement this
        send_email(user,"Monthly Report", report)

class User:
    def __init__(self, email):
        self.email = email


@celery.task
def export_theatre_as_csv(theatre_id):
    from .models import Theatre
    theatre = Theatre.query.get(theatre_id)
    csv_data = generate_csv_for_theatre(theatre)
    
    # Define directory and filename.
    dir_name = 'csv'
    file_name = f"theatre_{theatre_id}.csv"
    file_path = os.path.join(dir_name, file_name)  
    
    # Ensure the directory exists.
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)

    # Save the CSV data to the file.
    with open(file_path, 'w') as csv_file:
        csv_file.write(csv_data)

    user = User(email="cnsendemails@gmail.com")

    # Send an email.
    send_email(user, f"CSV for Theatre {theatre_id}", f"CSV generation complete. It's at this path in your file system: {file_path}")

# testing celery
@celery.task
def simple_task():
    print("Simple task is running!")
    time.sleep(5)
    print("Simple task finished!")

