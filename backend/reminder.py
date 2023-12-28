import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime, timedelta
from flask import Flask
import time
import sqlite3

app = Flask(__name__)

sender_email = "rekha0suthar@gmail.com"

smtp_server = 'smtp.gmail.com'
smtp_port = 587
smtp_username = 'rekha0suthar@gmail.com'
smtp_password = 'wfzpohtcuxsmfjqs'

reminder_time = datetime.now().replace(
    hour=20, minute=13, second=0, microsecond=0)

def send_reminder(user):
    subject = "Daily Reminder"
    message = f"Hello {user[1]} {user[2]}! It seems like you haven't visited or bought anything today. Please consider checking out our products on GrocerStore."
    receiver_email = user[6]
    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg["Subject"] = subject
    msg.attach(MIMEText(message, "plain"))

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_username, smtp_password)
            server.sendmail(sender_email, receiver_email, msg.as_string())
        print(f"Reminder email sent to {receiver_email} successfully!")
    except Exception as e:
        print(f"Failed to send reminder email to {receiver_email}: {e}")


def check_user_activity(user):

    conn1 = sqlite3.connect('storedata.db')
    cursor1 = conn1.cursor()

    today = datetime.today().date()
    cursor1.execute('SELECT * FROM orders WHERE created_at >= "{today}"')
    users_todays_order = cursor1.fetchall()
    

    return not users_todays_order


if __name__ == '__main__':
    while True:

        current_time = datetime.now()
        time_until_reminder = reminder_time - current_time

        if time_until_reminder.total_seconds() < 0:
            time_until_reminder += timedelta(days=1)

        print(
            f"Waiting for {time_until_reminder.seconds} seconds until the reminder time...")
        time.sleep(time_until_reminder.seconds)

        conn1 = sqlite3.connect('storedata.db')
        cursor1 = conn1.cursor()

        cursor1.execute('SELECT * FROM users')
        users = cursor1.fetchall()
       
        for user in users:
            if check_user_activity(user):
                send_reminder(user)
            else:
                print(
                    f"{user[1]} {user[2]} has visited or bought something today. No reminder needed.")