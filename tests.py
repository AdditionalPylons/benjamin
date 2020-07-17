# Standardlib Imports
"""import os"""
import unittest

# 3rd Party Module Imports
"""from twilio.rest import Client"""

# Project File Imports
from database_commands import add_entry, connect, custom_query, get_user_id, today
from parsing_logic import parse_expense, shortcuts
"""from send_sms import custom_notif"""


class TestParser(unittest.TestCase):

    test_values = {"cost": "00", "item": "test item",
                   "location": "test location", "date": "9999-01-01"}

    cost = test_values["cost"]
    item = test_values["item"]
    location = test_values["location"]
    date = test_values["date"]

    def test_parser_on_cost_only_input(self):
        self.assertEqual(parse_expense(f"{self.cost}"), ([f'{today}', f'{self.cost}', None, None]), "Parser is failing on single-value input.")

    def test_parser_on_cost_item_input(self):
        self.assertEqual(parse_expense(f"{self.cost} for {self.item}"), ([f'{today}', f'{self.cost}', f'{self.item}', None]), "Parser is failing on cost,item two-value input.")

    def test_parser_on_cost_location_input(self):
        self.assertEqual(parse_expense(f"{self.cost} at {self.location}"), ([f'{today}', f'{self.cost}', None, f'{self.location}']), "Parser is failing on cost,location two-value input.")

    def test_parser_on_cost_date_input(self):
        self.assertEqual(parse_expense(f"{self.cost} on {self.date}"), ([f'{self.date}', f'{self.cost}', None, None]), "Parser is failing on cost,date two-value input.")

    def test_parser_on_cost_item_location_input(self):
        self.assertEqual(parse_expense(f"{self.cost} for {self.item} at {self.location}"), ([f'{today}', f'{self.cost}', f'{self.item}', f'{self.location}']), "Parser is failing on cost,date two-value input.")

    def test_parser_on_cost_item_date_input(self):
        self.assertEqual(parse_expense(f"{self.cost} for {self.item} on {self.date}"), ([f'{self.date}', f'{self.cost}', f'{self.item}', None]), "Parser is failing on cost,date two-value input.")

    def test_parser_on_cost_item_location_date_input(self):
        self.assertEqual(parse_expense(f"{self.cost} for {self.item} at {self.location} on {self.date}"), ([f'{self.date}', f'{self.cost}', f'{self.item}', f'{self.location}']), "Parser is failing on cost,date two-value input.")


class TestShortcuts(unittest.TestCase):

    # Remember to update test_cases to include new shortcuts as they are added
    test_cases = ["bus", "subway"]

    def test_bus_shortcut_returns_correct_values(self):
        self.assertTrue("bus" in shortcuts, "'bus' was not found in dictionary 'shortcuts' in parsing_logic.py")
        self.assertEqual((shortcuts["bus"]), "6 for metrobus", "'bus' shortcut is not parsing properly.")

    def test_subway_shortcut_returns_correct_values(self):
        self.assertTrue("subway" in shortcuts)
        self.assertEqual((shortcuts["subway"]), "5 for subway", "'subway' shortcut is not parsing properly.")

    def test_all_shortcuts_are_in_dict_and_parse_successfully(self):
        for case in self.test_cases:
            self.assertTrue(case in shortcuts, f"{case} was not found in dictionary 'shortcuts' in parsing_logic.py")
        try:
            parse_expense(shortcuts[case])
        except Exception:
            self.fail(f"{case} shortcut isn't parsing correctly!")


class TestDatabase(unittest.TestCase):

    def test_database_connection_successful(self):
        try:
            connect()
        except Exception:
            self.fail("Can't connect to the database.")

    def test_can_write_to_database(self):
        try:
            add_entry(2,'9999-01-01', 00, 'test item', 'test location')
        except Exception:
            self.fail("Can't write to the database.")
        else:
            custom_query("DELETE FROM expenses WHERE user_id = 2 AND date = '9999-01-01' AND cost = '00' AND item = 'test item' AND location = 'test location'")

    def test_add_entry(self):
        number = "+1234567890"
        message_body = "00 for test item at test location on 9999-01-01"
        try:
            add_entry(*get_user_id(number)+parse_expense(message_body))
        except Exception:
            self.fail("add_entry is failing")
        else:
            custom_query("DELETE FROM expenses WHERE user_id = 2 AND date = '9999-01-01' AND cost = '00' AND item = 'test item' AND location = 'test location'")


"""class TestTwilio(unittest.TestCase):

    def test_can_send_sms_to_valid_number(self):
        my_cell_number = os.environ.get('my_cell_number')
        test_account_sid = os.environ.get('twilio_test_account_sid')
        test_auth_token = os.environ.get('twilio_test_auth_token')
        twilio_number = os.environ.get('twilio_number')
        test_number = os.environ.get('twilio_test_number')
        client = Client(test_account_sid, test_auth_token)
        try:
            client.messages.create(to = my_cell_number,from_ = test_number,body = 'test')
        except Exception:
            self.fail("Can't send SMS with Twilio.")"""


if __name__ == '__main__':
    unittest.main()
