import unittest
from unittest.mock import patch, MagicMock
from tkinter import StringVar, Tk
import hashlib
from voting_system_1 import voterLogin  # Make sure to replace 'your_module' with the name of your module.

class TestVoterLogin(unittest.TestCase):

    def setUp(self):
        self.root = Tk()
        self.app_instance = MagicMock()
        self.login_instance = voterLogin(self.root, self.app_instance)
        self.login_instance.display()

    def test_login_missing_fields(self):
        with patch('voting_system_1.messagebox.showwarning') as mock_msgbox:
            self.login_instance.voterId.set('')
            self.login_instance.password1.set('')
            self.login_instance.login()
            mock_msgbox.assert_called_with('Voting System Message', 'Missing fields')

    def test_login_wrong_credentials(self):
        with patch('voting_system_1.mysqlcon.findByVoterIdAndPassword', return_value=None), patch('voting_system_1.messagebox.showerror') as mock_msgbox_error:
            self.login_instance.voterId.set('123456')
            self.login_instance.password1.set('password123')
            self.login_instance.login()
            mock_msgbox_error.assert_called_with('Voting System Message', 'Wrong Credentials')

    def test_login_successful(self):
        fake_result = ("123456", "hashed_password")  # This can be modified to fit what the database returns
        with patch('voting_system_1.mysqlcon.findByVoterIdAndPassword', return_value=fake_result):
            callback = MagicMock()
            self.login_instance = voterLogin(self.root, self.app_instance, on_success=callback)
            self.login_instance.display()
            self.login_instance.voterId.set('123456')
            self.login_instance.password1.set('password123')
            self.login_instance.login()
            callback.assert_called_once_with('123456')

    def test_hash_password(self):
        raw_password = "test_password"
        hashed = self.login_instance.hash_password(raw_password)
        self.assertEqual(hashed, hashlib.sha256(raw_password.encode('utf-8')).hexdigest())

if __name__ == '__main__':
    unittest.main()
