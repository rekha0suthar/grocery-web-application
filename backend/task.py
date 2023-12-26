from celery import Celery
from celery.schedules import crontab
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import sqlite3
from checkout import calculate_total_expenditure
from datetime import datetime
from celery_config import celery
import smtplib
import os
from io import StringIO
import csv

def calculate_total_orders(user_id, role):
    conn1 = sqlite3.connect('storedata.db')
    cursor1 = conn1.cursor()

    cursor1.execute('SELECT * FROM orders WHERE user_id = ? AND role = ?', (user_id, role))
    orders = cursor1.fetchall()

    total_orders = 0
    for order in orders:
        total_orders += 1
    

    total_expenditure = calculate_total_expenditure(user_id, role)
    return total_orders, total_expenditure

@celery.task
def export_product_detail_as_csv(manager_id):
    conn1 = sqlite3.connect('storedata.db')
    cursor1 = conn1.cursor()

    cursor1.execute('SELECT * FROM products WHERE user_id = ? AND role = ? ORDER BY created_at DESC', (manager_id, 'manager'))
    products = cursor1.fetchall()

    cursor1.execute('SELECT * FROM category')
    categories = cursor1.fetchall()

    cursor1.execute('SELECT * FROM orders')
    orders = cursor1.fetchall()

    csv_data = StringIO()
    csv_writer = csv.writer(csv_data)
    csv_writer.writerow(['Name', 'Price', 'Expiry Date', 'Unit', 'Quantity', 'Sold Quantity', 'Category' ])
    
    sold_quantities = {}
    for order in orders:
        sold_quantities.setdefault(order[3], 0)
        sold_quantities[order[3]] += order[8]

    for product in products:
        category_name = ''
        for category in categories:
            if category[0] == product[7]:
                category_name = category[1]

        sold_quantity = sold_quantities.get(product[0], 0)

        csv_writer.writerow([
            product[1],
            product[2],
            product[4],
            product[3],
            product[6],
            sold_quantity,
            category_name
        ])
    base_dir = os.path.abspath(os.path.dirname(__file__))
    csv_file_path = os.path.join(base_dir, 'csv', 'product_report.csv')
    with open(csv_file_path, 'w') as csv_file:
        csv_file.write(csv_data.getvalue())
    return csv_file_path



@celery.task
def generate_monthly_report():
    current_month = datetime.now().strftime('%B')
    current_year = datetime.now().year

    conn1 = sqlite3.connect('storedata.db')
    cursor1 = conn1.cursor()

    cursor1.execute('SELECT * FROM users WHERE role = ?', ('user',))
    users = cursor1.fetchall()

    for user in users:
        total_orders, total_expenditure = calculate_total_orders(user[0], 'user')

        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
           <title>Monthly Activity Report</title>
        </head>
        <body>
            <H1>Monthly Activity Report - {current_month} {current_year} </h1>
            <p>Hello {user[1]} {user[2]}, </p>
            <p> Here's your activity summary for month of {current_month} {current_year}:</p>
            <ul>
                <li>Total orders: {total_orders}</li>
                <li>Total Expenditure: {total_expenditure}</li>
            </ul>
            <p>Thank you for using our serivce!</p>
            <p>Best regards</p>
            <p>Grocery Team</p>
        </body>
        </html>
        """
        send_email(html_content, user[6])

def send_email(html_content, to_email):
    from_email = "rekha0suthar@gmail.com" ##sender email id
    subject = 'Monthly Activity Report'

    to_email =  to_email ## receiver's email id

    msg = MIMEMultipart('alternate')
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject

    part1 = MIMEText(html_content, 'html')
    msg.attach(part1)

    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    smtp_username = 'rekha0suthar@gmail.com' ## sender email id
    smtp_password = 'wfzpohtcuxsmfjqs'

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_username, smtp_password)
            server.sendmail(from_email, to_email, msg.as_string())
            print(f"Email sent successfully to {to_email}")

    except Exception as e:
        print(f"Error sending email to {to_email}: {e}")