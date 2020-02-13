import unittest

from parsing_logic import parse_expense, shortcuts

class TestShortcuts(unittest.TestCase):

    #Remember to update test_cases to include new shortcuts as they are added
    test_cases = ["bus", "subway"]

    def test_bus_shortcut_returns_correct_values(self):
        self.assertTrue("bus" in shortcuts, "'bus' was not found in dictionary 'shortcuts' in parsing_logic.py")
        self.assertEqual((shortcuts["bus"]), "6 for metrobus", "'bus' shortcut is not parsing properly")

    def test_subway_shortcut_returns_correct_values(self):
        self.assertTrue("subway" in shortcuts)
        self.assertEqual((shortcuts["subway"]), "5 for subway", "'subway' shortcut is not parsing properly")

    def test_all_shortcuts_are_in_dict_and_parse_successfully(self):
        for case in self.test_cases:
            self.assertTrue(case in shortcuts, f"{case} was not found in dictionary 'shortcuts' in parsing_logic.py")
        try:
            parse_expense(shortcuts[case])
        except Exception:
            self.fail(f"{case} shortcut isn't parsing correctly!")



if __name__ == '__main__':
    unittest.main()
