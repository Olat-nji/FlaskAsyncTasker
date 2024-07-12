from celery import Celery
from dotenv import load_dotenv
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Load environment variables from .env file
load_dotenv()

# Celery configuration
app = Celery('tasks', broker=os.getenv('CELERY_BROKER_URL'))

# Email configuration
MAIL_HOST = os.getenv('MAIL_HOST')
MAIL_PORT = int(os.getenv('MAIL_PORT'))
MAIL_USERNAME = os.getenv('MAIL_USERNAME')
MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
MAIL_ENCRYPTION = os.getenv('MAIL_ENCRYPTION')
MAIL_FROM_ADDRESS = os.getenv('MAIL_FROM_ADDRESS')
MAIL_FROM_NAME = os.getenv('MAIL_FROM_NAME')

@app.task
def send_email(to_email, subject, body):
    """
    Celery task to send an email using SMTP.

    Args:
    - to_email (str): Email address of the recipient.
    - subject (str): Subject line of the email.
    - body (str): Body content of the email.

    Returns:
    - str: Confirmation message indicating success or failure of email sending.
    """
    # Create a multipart message and set headers
    msg = MIMEMultipart()
    msg['From'] = MAIL_FROM_ADDRESS
    msg['To'] = to_email
    msg['Subject'] = subject

    # Add body to email
    msg.attach(MIMEText(body, 'plain'))

    # Connect to the server
    with smtplib.SMTP(MAIL_HOST, MAIL_PORT) as server:
        # If MAIL_USERNAME and MAIL_PASSWORD are set, login to the server
        if MAIL_USERNAME and MAIL_PASSWORD:
            server.login(MAIL_USERNAME, MAIL_PASSWORD)
        
        # Send the email
        server.sendmail(MAIL_FROM_ADDRESS, to_email, msg.as_string())

    return f'Email sent to {to_email}'
