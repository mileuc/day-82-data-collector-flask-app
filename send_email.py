from email.mime.text import MIMEText
import smtplib
from dotenv import load_dotenv
import os

load_dotenv("./.env")
FROM_EMAIL = os.environ.get("MY_EMAIL")
PASSWORD = os.environ.get("PASSWORD")


def send_email(email, height, average_height, count):
    to_email = email

    cm = "cm"

    if int(height) < 163:
        status = "a <strong>smol bean</strong>"
    elif 163 <= int(height) < 174:
        status = "a <strong>tater tot</strong>"
    elif 174 <= int(height) < 181:
        status = "<strong>average</strong>"
    elif 181 <= int(height) < 190:
        status = "a <strong>tol bean</strong>"
    else:
        status = "an <strong>absolute unit</strong>"

    subject = "Collecting Heights: How smol are you?"
    message = f"Hello,<br><br>Your height is <strong>{height}{cm}</strong>! " \
              f"Wow!<br>You are {status}!<br><br>" \
              f"The average height of all <strong>{count}</strong> users who have participated is <strong>{average_height}{cm}</strong>." \
              f"<br><br>Thanks for participating!<br>Collecting Heights<br>"

    msg = MIMEText(message, 'html')
    msg['Subject'] = subject
    msg['To'] = to_email
    msg['From'] = FROM_EMAIL

    with smtplib.SMTP("smtp.gmail.com", port=587) as connection:  # specify location of the email providers smtp
        connection.starttls()  # a way to secure connection to our email server by encrypting message
        connection.ehlo()  # initiates SMTP communication using an EHLO (Extended Hello) command instead of the HELO command - additional SMTP commands are often available
        connection.login(user=FROM_EMAIL, password=PASSWORD)  # log in by providing a username and password
        # connection.sendmail(from_addr=FROM_EMAIL,
        #                     to_addrs=to_email,
        #                     msg=f"Subject:{subject}\n\n{message}")
        connection.send_message(msg)    # use for HTML enabled messages
