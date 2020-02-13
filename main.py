from flask import Flask, request, redirect
from twilio.twiml.messaging_response import MessagingResponse

from database_commands import add_entry, query_all, query_all_today
from parsing_logic import parse_expense, shortcuts

application = Flask(__name__)

@application.route('/sms', methods = ['GET', 'POST'])

def ingest_message():
    message_body = request.form['Body']
    response = MessagingResponse()

    try:
        #USAGE NOTE: When using add_entry with parse_expense, you MUST unpack the resulting tuple with * as follows:
        #add_entry(*parse_expense('123 for some thing at some place'))
        if message_body in shortcuts:
            add_entry(*parse_expense(shortcuts[message_body]))
        else:
            add_entry(*parse_expense(message_body))
        response.message('Entry successfully added!')

    except:
        response.message('Failed to add entry.')
    finally:
        return str(response)


if __name__ == '__main__':
    application.run(debug = False)
