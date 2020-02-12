import os

from twilio.rest import Client

account_sid = os.environ.get('twilio_account_sid')
auth_token = os.environ.get('twilio_auth_token')
my_cell_number = os.environ.get('my_cell_number')
twilio_number = os.environ.get('twilio_number')

client = Client(account_sid, auth_token)

def custom_notif(notif):

    client.messages.create(

    to = my_cell_number,
    from_ = twilio_number,
    body = notif

)
