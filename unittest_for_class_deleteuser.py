import unittest
from voting_system_1 import DeleteUser
import tkinter as tk
from unittest.mock import MagicMock, patch

class TestDeleteUser(unittest.TestCase):

    def setUp(self):
        self.root = tk.Tk()
        self.user = DeleteUser(self.root)

    def test_invalid_citizenship(self):
        # Setup: Mock the logger and the messagebox
        with patch('voting_system_1.logging.warning') as mock_log_warning, patch('voting_system_1.messagebox.showwarning') as mock_msgbox_warning:
            # Given: Invalid citizenship length
            self.user.citizenship.set('1234')

            # When: delete is called
            self.user.delete()

            # Then: A warning log should be generated and a messagebox warning should be shown
            mock_log_warning.assert_called_with('Attempt to delete with missing or invalid citizenship field.')
            mock_msgbox_warning.assert_called_with('Voting System Message', '🎱 Field is required\n🎱 Citizenship number length must be 11 digit')

    # Additional tests would follow a similar pattern...
    
    def test_no_such_user(self):
        # Mock the logger, the messagebox, and the findByCitizenship method
        with patch('voting_system_1.logging.info') as mock_log_info, patch('voting_system_1.messagebox.showinfo') as mock_msgbox_info, patch('voting_system_1.mysqlcon.findByCitizenship', return_value=None):
            # Given: A valid citizenship but no user associated with it
            self.user.citizenship.set('12345678900')

            # When: delete is called
            self.user.delete()

            # Then: An info log should be generated and a messagebox info should be shown
            mock_log_info.assert_called_with('Attempt to delete non-existent user with citizenship 12345678900.')
            mock_msgbox_info.assert_called_with('Voting System Message', 'No such User')

    def test_user_exists_and_deleted(self):
        # Mocking relevant methods
        with patch('voting_system_1.logging.info') as mock_log_info, patch('voting_system_1.messagebox.showinfo') as mock_msgbox_info, patch('voting_system_1.mysqlcon.findByCitizenship', return_value=True), patch('voting_system_1.mysqlcon.deleteUserByCitizenship', return_value=True):
            # Given: A valid citizenship and a user associated with it
            self.user.citizenship.set('12345678901')

            # When: delete is called
            self.user.delete()

            # Then: An info log should be generated and a messagebox info should be shown about successful deletion
            mock_log_info.assert_called_with('User with citizenship 12345678901 deleted successfully.')
            mock_msgbox_info.assert_called_with('Voting System Message', 'User Deleted')

    def test_exception_on_delete(self):
        # Mocking relevant methods
        with patch('voting_system_1.logging.error') as mock_log_error, patch('voting_system_1.messagebox.showerror') as mock_msgbox_error, patch('voting_system_1.mysqlcon.findByCitizenship', side_effect=Exception('DB Error')):
            # Given: An unexpected error while checking for user by citizenship
            self.user.citizenship.set('12345678901')

            # When: delete is called
            self.user.delete()

            # Then: An error log should be generated and a messagebox error should be shown
            mock_log_error.assert_called_with('Error during delete operation: DB Error')
            mock_msgbox_error.assert_called_with('Voting System Message', 'An unexpected error occurred. Please try again later.')


if __name__ == '__main__':
    unittest.main()
