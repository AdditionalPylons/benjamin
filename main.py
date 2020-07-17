# Standardlib Imports
#

# 3rd Party Module Imports
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

# Project File Imports
from database_commands import add_entry, get_user_id
from parsing_logic import parse_expense, shortcuts
from send_sms import check_alerts

app = Flask(__name__)


@app.route('/callben', methods=['GET', 'POST'])
def ingest_message():
    number = request.form['From']
    message_body = request.form['Body']
    response = MessagingResponse()

    user_id = get_user_id(number)
    try:
        # USAGE NOTE: When using add_entry with parse_expense,
        # you MUST unpack the resulting list with * as follows:
        # add_entry(*parse_expense('123 for some thing at some place'))
        if message_body in shortcuts:
            add_entry(*user_id+parse_expense(shortcuts[message_body]))
        else:
            add_entry(*user_id+parse_expense(message_body))
        response.message('Entry successfully added!')
    except Exception:
        response.message('Failed to add entry.')
    finally:
        check_alerts(user_id, number)
        return str(response)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
