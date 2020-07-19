# Standardlib Imports
import os

# 3rd Party Module Imports
from twilio.rest import Client

# Project File Imports
from database_commands import get_budget, query_spent

account_sid = os.environ.get('TWILIO_ACCOUND_SID')
auth_token = os.environ.get('TWILIO_AUTH_TOKEN')
my_cell_number = os.environ.get('MY_CELL_NUMBER')
twilio_number = os.environ.get('TWILIO_NUMBER')

client = Client(account_sid, auth_token)


def custom_notif(phone_number,notif):

    client.messages.create(

        to=phone_number,
        from_=twilio_number,
        body=notif

        )


def check_alerts(user_id, phone_number, period='daily'):
    budget = float(get_budget(user_id, period))
    spent = float(query_spent(user_id))
    remaining = budget - spent
    infinity = float("inf")

    alerts = {

        (0.66*budget, budget): (f"Warning: You've spent {spent} pesos."
                                f"Only {remaining} remaining!"),
        (budget, infinity): (f"Warning: You've spent {spent} pesos."
                                f"You're {spent-budget} over budget for today!")

            }

    for (a, b) in alerts.keys():
        if a <= spent < b:
            custom_notif(phone_number, alerts[(a, b)])
