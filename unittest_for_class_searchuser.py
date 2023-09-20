import unittest
from voting_system_1 import SearchUser
from tkinter import StringVar, Tk
from unittest.mock import MagicMock, patch

class TestSearchUser(unittest.TestCase):

    def setUp(self):
        self.root = Tk()
        self.user = SearchUser(self.root)

    def test_invalid_citizenship(self):
        # Mocking the messagebox
        with patch('voting_system_1.messagebox.showwarning') as mock_msgbox:
            # Given: Invalid citizenship
            self.user.citizenship.set('1234')

            # When: search is called
            self.user.search()

            # Then: A warning message box should be shown
            mock_msgbox.assert_called_with('Voting System Message', '🎱 Field is required\n🎱 Citizenship number length must be 11 digit')

    def test_no_such_user(self):
        # Mocking the messagebox and the getUserByCitizenship method
        with patch('voting_system_1.messagebox.showinfo') as mock_msgbox_info, patch('voting_system_1.mysqlcon.getUserByCitizenship', return_value=None):
            # Given: A valid citizenship but no user associated with it
            self.user.citizenship.set('12345678901')

            # When: search is called
            self.user.search()

            # Then: An info messagebox should be shown with message 'No such User'
            mock_msgbox_info.assert_called_with('Voting System Message', 'No such User')

    def test_user_exists(self):
        # Mocking the messagebox and the getUserByCitizenship method
        with patch('voting_system_1.messagebox.showinfo') as mock_msgbox_info, patch('voting_system_1.mysqlcon.getUserByCitizenship', return_value=("John", "1234567890", "Male", "DistrictX")):
            # Given: A valid citizenship and a user associated with it
            self.user.citizenship.set('12345678901')

            # When: search is called
            self.user.search()

            # Then: An info messagebox should be shown displaying the user's details
            mock_msgbox_info.assert_called_with('Voting System Message', f"User Details:\nName: John\nPhone: 1234567890\nGender: Male\nDistrict: DistrictX")

if __name__ == '__main__':
    unittest.main()
