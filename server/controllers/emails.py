import os
import smtplib
from dotenv import load_dotenv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

load_dotenv()

SMTP_SERVER_HOST = os.environ.get('SMTP_SERVER_HOST')
SMTP_SERVER_PORT = os.environ.get('SMTP_SERVER_PORT')
SENDER_ADDRESS = os.environ.get('SENDER_ADDRESS')
SENDER_PASSWORD = os.environ.get('SENDER_PASSWORD')

def send_email(to, subject, body):
    msg = MIMEMultipart()
    msg['From'] = SENDER_ADDRESS
    msg['To'] = to
    msg['Subject'] = subject
    
    msg.attach(MIMEText(body, 'html'))
    
    smtp_server = smtplib.SMTP(SMTP_SERVER_HOST, SMTP_SERVER_PORT)
    smtp_server.login(SENDER_ADDRESS, SENDER_PASSWORD)
    smtp_server.send_message(msg)
    smtp_server.quit()
    
    return True