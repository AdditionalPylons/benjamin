# Standardlib Imports
import time

# 3rd Party Module Imports
from flask import Flask, request


# Project File Imports
from database_commands import add_entry, get_user_id
from parsing_logic import parse_inc_message
from send_sms import check_alerts

app = Flask(__name__)


@app.route('/callben', methods=['GET', 'POST'])
def ingest_message():
    number = request.form['From']
    message_body = request.form['Body']

    user_id = get_user_id(number)

    return parse_inc_message(user_id, number, message_body)




if __name__ == '__main__':
    app.run(host='0.0.0.0')
