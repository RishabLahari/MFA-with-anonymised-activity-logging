import csv
import random
import pyotp
import hashlib
import mailtrap as mt
from getpass import getpass
from datetime import datetime


# Function to send OTP via email with TLS using Mailtrap
def send_otp_email(email, otp):
    # Create the email message
    mail = mt.Mail(
        sender=mt.Address(email="mailtrap@demomailtrap.com", name="Mailtrap Test"),
        to=[mt.Address(email=email)],
        subject="OTP for Login",
        text=f"Your OTP is: {otp}",
        category="OTP Email"
    )
    client = mt.MailtrapClient(token="APICODE")
    client.send(mail)

# Generate random credentials database for testing
def generate_credentials(num_users):
    credentials = []
    uname = 'Rishab'
    pword = '1234'
    em = 'XYZ@gmail.com'
    credentials.append({'username': uname, 'password': pword, 'email': em})
    for i in range(num_users):
        username = f'User{i+1}'
        password = f'Password{i+1}'
        email = f'email{i+1}@gmail.com'
        credentials.append({'username': username, 'password': password, 'email': email})
    return credentials

# Function to hash a string using SHA-256
def hash_string(string):
    return hashlib.sha256(string.encode()).hexdigest()

# Generate random credentials database with 5 users for testing
credentials_db = generate_credentials(5)

# Generate a secret key for each user for OTP
for user in credentials_db:
    user['secret'] = pyotp.random_base32()

# Create a CSV file for logging activity
with open('user_logins.csv', mode='a', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Timestamp', 'Username (Hashed)', 'Email (Hashed)', 'Status'])

# Login process
username = input("Enter your username: ")
password = getpass("Enter your password: ")

# Search for the user in the credentials database
user_found = False
for user in credentials_db:
    if user['username'] == username and user['password'] == password:
        user_found = True
        email = user['email']
        secret = user['secret']
        break

if not user_found:
    print("Invalid username or password.")
    exit()

# Generate OTP and send it via email
totp = pyotp.TOTP(secret)
otp = totp.now()

send_otp_email(email, otp)

# Perform MFA
user_input_otp = input("Enter the OTP sent to your email: ")
if not user_input_otp==otp:
    print("OTP verification failed. Login unsuccessful.")
    with open('user_logins.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([datetime.now().strftime("%Y-%m-%d %H:%M:%S"), hash_string(username), hash_string(email), 'Failed'])
    exit()

# Login successful, log activity in CSV
print("Login successful.")
with open('user_logins.csv', mode='a', newline='') as file:
    writer = csv.writer(file)
    writer.writerow([datetime.now().strftime("%Y-%m-%d %H:%M:%S"), hash_string(username), hash_string(email), 'Successful'])
