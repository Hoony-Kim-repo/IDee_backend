import os
import random
import smtplib
from datetime import datetime, timedelta, timezone
from email.mime.text import MIMEText

from dotenv import load_dotenv

load_dotenv()

SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
SMTP_PORT = os.getenv("SMTP_PORT")
FROM_EMAIL = os.getenv("FROM_EMAIL")
FROM_NAME = os.getenv("FROM_NAME")

# In memory store for verification codes (for demonstration purposes)
# Key: email, Value: {"code": str, "expires_at": datetime}
EMAIL_VERIFICATION_STORE = {}


def generate_verification_code():
    """Generate a 4-digit verification code"""
    return str(random.randint(1000, 9999))


def generate_email(code):
    """Generate email subject and body for verification code"""

    title = "(No Reply) Your Email Verification Code by IDee"
    body = f"""
    Hi there,
    
    Thank you for signning up!
    Your verification code is:
    🔐 Verification Code: {code}
    
    Please enter this code within 5 minutes to complete your registration.
    If you did not request this, please ignore this email.
    
    Best regards,
    IDee
    """
    return title, body


def send_verification_email(target_email: str):
    """
    Create 4-digit code and send it to the target email.
    """
    code = generate_verification_code()

    expires_at = datetime.now(timezone.utc) + timedelta(minutes=5)
    EMAIL_VERIFICATION_STORE[target_email] = {"code": code, "expires_at": expires_at}

    email_subject, email_body = generate_email(code)

    msg = MIMEText(email_body, "plain")
    msg["Subject"] = email_subject
    msg["From"] = FROM_EMAIL
    msg["To"] = target_email

    with smtplib.SMTP(SMTP_SERVER, int(SMTP_PORT)) as server:
        server.starttls()
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.sendmail(FROM_EMAIL, target_email, msg.as_string())

    return code


def verify_email_code(target_email: str, code: str) -> bool:
    """
    Compare user input code with stored code.
    Returns True if correct and not expired, else False.
    """

    record = EMAIL_VERIFICATION_STORE.get(target_email)
    if not record:
        return False

    # Check expiration
    if datetime.now(datetime.timezone.utc) > record["expires_at"]:
        del EMAIL_VERIFICATION_STORE[target_email]  # Clean up expired code
        return False

    # Compare codes
    if record["code"] == code:
        del EMAIL_VERIFICATION_STORE[target_email]  # Clean up used code
        return True

    return False
