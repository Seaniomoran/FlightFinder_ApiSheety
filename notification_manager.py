import os
import smtplib
#from twilio.rest import Client

customers_endpoint = f"{(os.getenv('SHEETY_PRICES_ENDPOINT')).replace('prices', 'users')}"
MY_EMAIL = os.getenv("EMAIL_17")  #enter your email
MY_PASSWORD = os.getenv("EMAIL_17_PASSWORD")  #enter google account, security, app password
EMAIL_PROVIDER_SMTP_ADDRESS = "smtp.gmail.com"

# TWILIO_ACCOUNT_ID = os.getenv("TWILIO_ACCOUNT_ID")
# TWILIO_TOKEN = os.getenv("TWILIO_TOKEN")
# MY_PHONE_NUM = os.getenv("MY_PHONE_NUM")
# TWILIO_PHONE_NUM = os.getenv("TWILIO_PHONE_NUM")
#
#
# class NotificationManager:
#     #This class is responsible for sending notifications with the deal flight details.
#
#     def __init__(self):
#         self.client = Client(TWILIO_ACCOUNT_ID, TWILIO_TOKEN)
#
#     def send_text(self, message: str):
#         message = self.client.messages.create(
#             body=f"{message}",
#             from_=f'{TWILIO_PHONE_NUM}',
#             to=f'{MY_PHONE_NUM}')
#         print(message.status)


class NotificationManager:
    #This class is responsible for sending notifications with the deal flight details to customers.

    def send_emails(self, emails, message, google_flight_link):
        with smtplib.SMTP(EMAIL_PROVIDER_SMTP_ADDRESS) as connection:
            connection.starttls()
            connection.login(user=MY_EMAIL, password=MY_PASSWORD)
            for email in emails:
                connection.sendmail(
                    from_addr=MY_EMAIL,
                    to_addrs=email,
                    msg=f"Subject:New Low Price Flight!\n\n{message}\n{google_flight_link}".encode('utf-8')
                )
