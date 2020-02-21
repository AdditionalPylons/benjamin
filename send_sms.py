#Standardlib Imports
import os

#3rd Party Module Imports
from twilio.rest import Client

#Project File Imports
from database_commands import query_spent_today

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


def check_alerts():
    budget = 300
    spent = int(query_spent_today())
    remaining = budget - spent
    infinity = float("inf")

    alerts = {

    (0.66*budget, budget): f"Warning: You've spent {spent} pesos. Only {remaining} remaining!",
    (budget, infinity): f"Warning: You've spent {spent} pesos. You're {spent-budget} over budget for today!"

    }

    for (a,b) in alerts.keys():
        if a <= spent < b:
            custom_notif(alerts[(a,b)])

check_alerts()
