from utils.db import get_connection
from utils.security import hash_password
from utils.validation import is_password_strong
from utils.email_utils import send_email

# register prompts
def register_user():
    username = input("Enter username: ").strip()
    password = input("Enter password: ").strip()
    email = input("Enter your email: ").strip()

    validation_message = is_password_strong(password)
    if validation_message:
        print(f"Error: {validation_message}")
        return
# password hashing
    hashed_password = hash_password(password)
# database for passwords and user and email
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (username, password, email) VALUES (?, ?,?)", 
                       (username, hashed_password, email))
        conn.commit()

        # Send welcome email
        subject = "Welcome to Our ESports Auth"
        content = f"Hello {username},\n\nThank you for registering! We're excited to have you onboard.\n\nBest regards,\nEsportsAuth Team"
        send_email(email, subject, content)

        print("Registration successful! A welcome email has been sent to your email address.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.close()
