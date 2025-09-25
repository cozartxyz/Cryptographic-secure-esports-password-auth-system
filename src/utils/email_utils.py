import smtplib
import os
from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv() 

def send_email(to_email, subject, content):
    email_host = os.getenv("EMAIL_HOST")
    email_port = os.getenv("EMAIL_PORT")
    email_user = os.getenv("EMAIL_USER")
    email_pass = os.getenv("EMAIL_PASS")

    try:
        
        msg = EmailMessage()
        msg.set_content(content)
        msg["Subject"] = subject
        msg["From"] = email_user
        msg["To"] = to_email

        
        with smtplib.SMTP(email_host, email_port) as server:
            server.starttls()  
            server.login(email_user, email_pass)  
            server.send_message(msg)  
        print(f"Email sent to {to_email}")
    except Exception as e:
        print(f"Failed to send email: {e}")
