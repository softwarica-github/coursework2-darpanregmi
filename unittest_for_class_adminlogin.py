import unittest
from voting_system_1 import AdminLogin
from tkinter import Tk
from unittest.mock import patch, Mock

class TestAdminLogin(unittest.TestCase):

    def setUp(self):
        self.root = Tk()
        self.voting_system_instance = Mock()  # Assuming the AdminLogin needs a VotingSystem instance
        self.admin_login = AdminLogin(self.root, self.voting_system_instance)

    def test_login_empty_fields(self):
        with patch('voting_system_1.messagebox.showwarning') as mock_msgbox_warning:
            # Given: Empty username and password fields
            self.admin_login.username_var.set('')
            self.admin_login.password_var.set('')

            # When: Login is called
            self.admin_login.Login()

            # Then: A warning messagebox should be shown
            mock_msgbox_warning.assert_called_with('Voting System Message', 'Fields are required')

    def test_successful_login(self):
        with patch('voting_system_1.mysqlcon.get_admin_details', return_value=True), patch('voting_system_1.messagebox.showinfo') as mock_msgbox_info:
            # Given: Correct username and password
            self.admin_login.username_var.set('835d6dc88b708bc646d6db82c853ef4182fabbd4a8de59c213f2b5ab3ae7d9be')
            self.admin_login.password_var.set('95082382fd163ef1522fcfcc372b33f4873f1a608e400050379be940f75a021a')

            # When: Login is called
            self.admin_login.Login()

            # Then: An info message box should be shown with success message
            print(mock_msgbox_info.call_args)


    def test_failed_login(self):
        with patch('voting_system_1.mysqlcon.get_admin_details', return_value=None), patch('voting_system_1.messagebox.showerror') as mock_msgbox_error:
            # Given: Incorrect username or password
            self.admin_login.username_var.set('wrong_username')
            self.admin_login.password_var.set('wrong_password')

            # When: Login is called
            self.admin_login.Login()

            # Then: An error message box should be shown
            mock_msgbox_error.assert_called_with('Voting System Message', 'Wrong Credentials')

    def test_exception_during_login(self):
        with patch('voting_system_1.mysqlcon.get_admin_details', side_effect=Exception('Test Exception')), patch('voting_system_1.messagebox.showerror') as mock_msgbox_error:
            # Given: An exception occurs during the database lookup
            self.admin_login.username_var.set('username')
            self.admin_login.password_var.set('password')

            # When: Login is called
            self.admin_login.Login()

            # Then: An error message box should be shown
            mock_msgbox_error.assert_called_with('Voting System Message', 'An unexpected error occurred during login.')

if __name__ == '__main__':
    unittest.main()
