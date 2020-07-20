# Standardlib Imports
import datetime as dt
import re

# 3rd Party Module Imports
from twilio.twiml.messaging_response import MessagingResponse

# Project File Imports
from database_commands import add_entry, query_spent, query_spent_range, today, this_week, this_month
from send_sms import check_alerts


# USAGE NOTE: When using add_entry with parse_expense,
# you MUST unpack the resulting list with * as follows:
# add_entry(*parse_expense('123 for some thing at some place'))
def parse_inc_message(user_id, phone_number, input):

    commands = {

        "spent": (query_spent, *user_id, today),
        "spent today": (query_spent, *user_id, today),
        "spent week": (query_spent_range, *user_id, this_week),
        "spent month": (query_spent_range, *user_id, this_month),
        "left": "",
        "left today": "",
        "left week": "",
        "left month": ""

                }

    shortcuts = {

        "bus": "6 for metrobus",
        "subway": "5 for subway"

                }

    response = MessagingResponse()

    try:
        if input in commands:
            response.message(str(commands[input][0](commands[input][1], commands[input][2])))
        elif input in shortcuts:
            add_entry(*user_id+parse_expense(shortcuts[input]))
            response.message("Entry successfuly added!")
        else:
            add_entry(*user_id+parse_expense(input))
            response.message("Entry successfuly added!")
    except Exception:
        response.message("Uh-oh! Something went wrong. Please try again.")
    finally:
        check_alerts(*user_id, phone_number)
        return str(response)





# Returns a comma-separated list of string
def parse_expense(input):

    sms_syntax = re.compile(r'(?P<cost>\d+)'
                            # Some num of digits = cost
                            r'(?: for (?P<item>.+?))?'
                            # Everything after "for" = item, optional
                            r'(?: at (?P<location>.+?))?'
                            # Everything after "at" = location, optional
                            r'(?: on (?P<date>.+))?$'
                            # Everything after "on" = date, optional
                            )
    if re.search('(?: on (?P<date>.+))$', input):
        parsed_result = list(sms_syntax.search(input).group(
            'date', 'cost', 'item', 'location'))
    else:
        parsed_result = [str(dt.date.today())]+list(
            sms_syntax.search(input).group('cost', 'item', 'location'))
    return parsed_result
