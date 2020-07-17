# Standardlib Imports
import datetime
import re

# 3rd Party Module Imports
#

# Project File Imports
#


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
        parsed_result = [str(datetime.date.today())]+list(
            sms_syntax.search(input).group('cost', 'item', 'location'))
    return parsed_result


shortcuts = {

    "bus": "6 for metrobus",
    "subway": "5 for subway"

            }
