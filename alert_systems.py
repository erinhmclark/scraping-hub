""" """
import smtplib
import os
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

DEV_GMAIL = os.environ.get('DEV_GMAIL')
DEV_GMAIL_APP_PW = os.environ.get('DEV_GMAIL_APP_PW')


def send_from_gmail(sender_email, app_password, subject, message, receiver_email):
    """ Send a basic email from a gmail account.
        Note this requires you to set up the gmail account with 2-factor authentication,
        along with generating an app password which is uses here for access.
    """
    with smtplib.SMTP("smtp.gmail.com", 587) as smpt:
        smpt.ehlo()
        smpt.starttls()
        smpt.ehlo()

        smpt.login(sender_email, app_password)

        msg = f'Subject: {subject}\n\n{message}'
        smpt.sendmail(sender_email, receiver_email, msg)


if __name__ == '__main__':

    # TODO Fetch emails from csv, DB
    send_to = 'someone@gmail.com'
    send_from_gmail(DEV_GMAIL, DEV_GMAIL_APP_PW, 'test email', 'hello there', send_to)

