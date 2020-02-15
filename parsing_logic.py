#Standardlib Imports
import datetime
import re

#3rd Party Module Imports
#

#Project File Imports
#




def parse_expense(input):

    sms_syntax = re.compile('(?P<cost>\d+)'                  #Some num of digits = cost
                            '(?: for (?P<item>.+?))?'        #Everything after "for" = item, optional
                            '(?: at (?P<location>.+))?$')    #Everything after "at" = location, optional
    parsed_result = tuple([str(datetime.date.today())]+list((sms_syntax.search(input).group('cost', 'item', 'location'))))
    return parsed_result

shortcuts = {

"bus": "6 for metrobus",
"subway": "5 for subway"

}
