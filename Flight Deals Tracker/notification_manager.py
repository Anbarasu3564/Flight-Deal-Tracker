import os
from twilio.rest import Client
import smtplib
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class NotificationManager:
    """
    This class handles sending notifications through SMS, WhatsApp, and Email.
    """

    def __init__(self):
        self.client = Client(os.environ["ACCOUNT_SID"], os.environ["AUTH_TOKEN"])
        self.my_mail = os.environ["MY_EMAIL"]
        self.app_password = os.environ["APP_PASSWORD"]
        self.connection = None

    def send_sms(self, message_body):
        """
        Sends an SMS notification.
        """
        message = self.client.messages.create(
            body=message_body,
            from_=os.environ["TWILIO_NUM"],
            to=os.environ["VERIFIED_NUM"],
        )
        print(message.sid)

    def send_whatsup(self, message_body):
        """
        Sends a WhatsApp notification.
        """
        message = self.client.messages.create(
            body=message_body,
            from_=f"whatsapp{os.environ['TWILIO_NUM']}",
            to=f"whatsapp{os.environ['VERIFIED_NUM']}",
        )
        print(message.sid)

    def send_email(self, email_body, email_list):
        """
        Sends an email notification to a list of users.
        """
        self.connection = smtplib.SMTP(os.environ["EMAIL_PROVIDER_SMTP_ADDRESS"])
        self.connection.starttls()
        self.connection.login(user=self.my_mail, password=self.app_password)

        for email in email_list:
            self.connection.sendmail(
                from_addr=self.my_mail,
                to_addrs=email,
                msg=f"Subject: New Low Price Flight!\n\n{email_body}".encode('utf-8')
            )
        self.connection.close()
