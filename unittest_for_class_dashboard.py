import unittest
from unittest.mock import patch, MagicMock
from tkinter import StringVar, Tk
from voting_system_1 import dashboard

class TestDashboard(unittest.TestCase):

    def setUp(self):
        self.root = Tk()
        self.app_instance = MagicMock()
        with patch('voting_system_1.mysqlcon.findByVoterId', return_value=["123456", "John", "Doe"]):
            self.dashboard_instance = dashboard(self.root, self.app_instance, "123456")
            self.dashboard_instance.display()
        
    def test_vote_missing_fields(self):
        with patch('voting_system_1.messagebox.showwarning') as mock_msgbox:
            self.dashboard_instance.poll.set('')
            self.dashboard_instance.district.set('')
            self.dashboard_instance.vote()
            mock_msgbox.assert_called_with('Voting System Message', 'All fields are required to be filled.')

    def test_already_voted(self):
        with patch('voting_system_1.mysqlcon.findByVoterIdinVote', return_value=("some_value")), patch('voting_system_1.messagebox.showwarning') as mock_msgbox:
        # Set required fields to pass the initial validation
            self.dashboard_instance.poll.set('Nepali Congress')
            self.dashboard_instance.district.set('Kathmandu')
            
            self.dashboard_instance.vote()
            
            mock_msgbox.assert_called_with('Voting System Message', 'Thanks, but you have voted already.')

    def test_vote_successful(self):
        with patch('voting_system_1.mysqlcon.findByVoterIdinVote', return_value=None), \
             patch('voting_system_1.mysqlcon.submitVote', return_value=True), \
             patch('voting_system_1.messagebox.showinfo') as mock_msgbox_info:
            self.dashboard_instance.poll.set('Nepali Congress')
            self.dashboard_instance.district.set('Achham')
            self.dashboard_instance.vote()
            mock_msgbox_info.assert_called_with('Voting System Message', 'Thanks, Vote submitted successfully.')

    def test_vote_failed(self):
        with patch('voting_system_1.mysqlcon.submitVote', return_value=False), patch('voting_system_1.messagebox.showwarning') as mock_msgbox_warning:
        # Set required fields
            self.dashboard_instance.poll.set('Some Party')
            self.dashboard_instance.district.set('Some District')
            
            self.dashboard_instance.vote()
            
            mock_msgbox_warning.assert_called_with('Voting System Message', 'Try again later, Failed to vote.')


    def test_unexpected_error_during_vote(self):
        with patch('voting_system_1.mysqlcon.submitVote', side_effect=Exception("Mocked Exception")), patch('voting_system_1.messagebox.showerror') as mock_msgbox_error:
        # Set required fields
            self.dashboard_instance.poll.set('Some Party')
            self.dashboard_instance.district.set('Some District')
            
            self.dashboard_instance.vote()
            
            mock_msgbox_error.assert_called_with('Voting System Message', 'An unexpected error occurred while voting.')

    def test_logout(self):
        self.dashboard_instance.logout()
        self.app_instance.Home.assert_called_once()

if __name__ == '__main__':
    unittest.main()
