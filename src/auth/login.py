from datetime import datetime, timedelta
from utils.db import get_connection
from utils.security import verify_password, hash_ip
from utils.geolocation import get_ip_address, get_timezone_from_ip
from utils.email_utils import send_email
from utils.otp import generate_otp
from utils.validation import is_password_strong

MAX_FAILED_ATTEMPTS = 5
LOCKOUT_DURATION = 1  # Lockout duration in minutes

# account status check if locked out or not
def check_lockout_status(username):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT failed_attempts, lockout_until FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()

    if user:
        failed_attempts, lockout_until = user
        if lockout_until:
            lockout_until = datetime.strptime(lockout_until, "%Y-%m-%d %H:%M:%S")
            if datetime.now() < lockout_until:
                return True, lockout_until
    return False, None

# for failed attempts
def update_failed_attempts(username):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT failed_attempts FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()

    if user:
        failed_attempts = user[0] + 1

        if failed_attempts >= MAX_FAILED_ATTEMPTS:
            lockout_until = datetime.now() + timedelta(minutes=LOCKOUT_DURATION)
            cursor.execute("UPDATE users SET failed_attempts = ?, lockout_until = ? WHERE username = ?",
                           (failed_attempts, lockout_until.strftime("%Y-%m-%d %H:%M:%S"), username))
            print(f"Account locked due to multiple failed attempts. Try again after {LOCKOUT_DURATION} minutes.")
        else:
            cursor.execute("UPDATE users SET failed_attempts = ? WHERE username = ?", (failed_attempts, username))
            print(f"Invalid password. {MAX_FAILED_ATTEMPTS - failed_attempts} attempts remaining.")
        conn.commit()
    conn.close()


def reset_failed_attempts(username):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("UPDATE users SET failed_attempts = 0, lockout_until = NULL WHERE username = ?", (username,))
    conn.commit()
    conn.close()

#log login attempts
def log_login_attempt(username, ip_address, timezone):
    conn = get_connection()
    cursor = conn.cursor()

    hashed_ip = hash_ip(ip_address)
    cursor.execute("INSERT INTO login_logs (username, hashed_ip, timezone) VALUES (?, ?, ?)",
                   (username, hashed_ip, timezone))
    conn.commit()
    conn.close()

#this is some captcha type thing
def human_verification():
    import random

    num1, num2 = random.randint(1, 9), random.randint(1, 9)
    correct_answer = num1 + num2

    try:
        user_answer = int(input(f"Solve this: {num1} + {num2} = "))
        if user_answer == correct_answer:
            print("Verification successful!")
            return True
        else:
            print("Incorrect answer. Verification failed.")
            return False
    except ValueError:
        print("Invalid input. Verification failed.")
        return False


def login_user():
    username = input("Enter username: ").strip()
    password = input("Enter password: ").strip()

    conn = get_connection()
    cursor = conn.cursor()

    # Check if the user exists
    cursor.execute("SELECT password, email FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()

    if not user:
        print("Username not found. Please register first.")
        return

    hashed_password, email = user

    # Check lockout status
    is_locked_out, lockout_until = check_lockout_status(username)
    if is_locked_out:
        print(f"Account is locked until {lockout_until}. Please try again later.")
        return

    # Verify password
    if not verify_password(password, hashed_password):
        update_failed_attempts(username)
        return

    # Password is correct; reset failed attempts
    reset_failed_attempts(username)

    # Log IP and timezone
    ip_address = get_ip_address()
    timezone = get_timezone_from_ip(ip_address)
    print(f"Login detected from IP: {ip_address}, Timezone: {timezone}")

    # Perform additional verification if the IP or timezone is unusual
    cursor.execute("SELECT hashed_ip, timezone FROM login_logs WHERE username = ? ORDER BY timestamp DESC LIMIT 1", (username,))
    last_login = cursor.fetchone()

    if last_login:
        last_hashed_ip, last_timezone = last_login

        if not verify_password(ip_address, last_hashed_ip) or timezone != last_timezone:
            print("Unusual activity detected. Additional verification required.")
            if not human_verification():
                print("Verification failed. Login denied.")
                return

    # Generate and send OTP for 2FA
    otp = generate_otp()
    send_email(email, "Your Login OTP", f"Your OTP is: {otp}")

    # Ask for OTP verification
    user_otp = input("Enter the OTP sent to your email: ").strip()
    if user_otp != otp:
        print("Invalid OTP. Login denied.")
        return

    # Log successful login
    log_login_attempt(username, ip_address, timezone)

    print("Login successful! Welcome back!")
