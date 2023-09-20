import unittest
from unittest.mock import patch, MagicMock
from tkinter import StringVar, Tk
from voting_system_1 import voterRegistration


class TestVoterRegistration(unittest.TestCase):

    def setUp(self):
        self.root = Tk()
        self.app_instance = MagicMock()
        self.reg_instance = voterRegistration(self.root, self.app_instance)
        self.reg_instance.display()

    def test_successful_registration(self):
        with patch('voting_system_1.mysqlcon.findByCitizenship', return_value=None), \
             patch('voting_system_1.mysqlcon.findByVoterId', return_value=None), \
             patch('voting_system_1.mysqlcon.addVoter', return_value=True), \
             patch('voting_system_1.messagebox.showinfo') as mock_msgbox:

            self.reg_instance.name.set('Test User')
            self.reg_instance.citizenship.set('12345678901')
            self.reg_instance.phone.set('9876543210')
            self.reg_instance.district.set('Kathmandu')
            self.reg_instance.gender.set('Male')
            self.reg_instance.password.set('Password123!')
            self.reg_instance.cpassword.set('Password123!')
            
            self.reg_instance.register()

            mock_msgbox.assert_called() 

    def test_incomplete_fields(self):
        with patch('voting_system_1.messagebox.showwarning') as mock_msgbox:
            self.reg_instance.name.set('')
            self.reg_instance.register()
            mock_msgbox.assert_called_with('Voting System Message', 'All fields are required to be filled.')

if __name__ == '__main__':
    unittest.main()
