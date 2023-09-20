import unittest
from voting_system_1 import UpdateUser
from tkinter import StringVar, Tk
from unittest.mock import MagicMock, patch

class TestUpdateUser(unittest.TestCase):

    def setUp(self):
        self.root = Tk()
        self.user = UpdateUser(self.root)

    def test_search_no_user(self):
        with patch('voting_system_1.messagebox.showinfo') as mock_msgbox_info, patch('voting_system_1.mysqlcon.findByCitizenships', return_value=None):
            # Given: A citizenship without an associated user
            self.user.citizenship.set('12345678900')

            # When: search is called
            self.user.search()

            # Then: An info messagebox should be shown with message 'No such User'
            mock_msgbox_info.assert_called_with('Voting System Message', 'No such User')

    def test_search_user_exists(self):
        with patch('voting_system_1.mysqlcon.findByCitizenships', return_value=("12345678901", "John", "1234567890", "DistrictX", "Male", "seomehh")):
            # Given: A citizenship with an associated user
            self.user.citizenship.set('12345678901')

            # When: search is called
            self.user.search()

            # Then: The name, phone, gender, and district fields should be populated
            self.assertEqual(self.user.name.get(), "John")
            self.assertEqual(self.user.phone.get(), "1234567890")
            self.assertEqual(self.user.gender.get(), "Male")
            self.assertEqual(self.user.district.get(), "DistrictX")

    def test_update_invalid_phone(self):
        with patch('voting_system_1.messagebox.showwarning') as mock_msgbox_warning:
            # Given: Invalid phone number
            self.user.name.set("John")
            self.user.phone.set('123456')
            self.user.gender.set('Male')
            self.user.district.set('DistrictX')
            self.user.citizenship.set('12345678901')
            

            # When: update is called
            self.user.update()

            # Then: A warning message box should be shown
            mock_msgbox_warning.assert_called_with('Voting System Message', 'Invalid phone number. It must be 10 digits.')

    def test_update_success(self):
        with patch('voting_system_1.mysqlcon.updateUserByCitizenship', return_value=True), patch('voting_system_1.messagebox.showinfo') as mock_msgbox_info:
            # Given: Valid details
            self.user.name.set("John")
            self.user.phone.set('1234567890')
            self.user.gender.set('Male')
            self.user.district.set('DistrictX')
            self.user.citizenship.set('12345678901')
            

            # When: update is called
            self.user.update()

            # Then: An info message box should be shown with success message
            mock_msgbox_info.assert_called_with('Voting System Message', 'User updated successfully.')

    def test_update_fail(self):
        with patch('voting_system_1.mysqlcon.updateUserByCitizenship', return_value=False), patch('voting_system_1.messagebox.showerror') as mock_msgbox_error:
            # Given: Valid details but updateUserByCitizenship returns False
            self.user.name.set("John")
            self.user.phone.set('1234567890')
            self.user.gender.set('Male')
            self.user.district.set('DistrictX')
            self.user.citizenship.set('12345678901')

            # When: update is called
            self.user.update()

            # Then: An error message box should be shown
            mock_msgbox_error.assert_called_with('Voting System Message', 'Failed to update the user.')

if __name__ == '__main__':
    unittest.main()
