import unittest
import os
import json
from tkinter import Tk
from tkinter import messagebox

# Assuming your application code is imported here
from main.py import Application, PasswordRecoveryFrame, save_users, load_users

class TestPasswordRecovery(unittest.TestCase):

    def setUp(self):
        """Setup a temporary users.json file and create an instance of the application."""
        self.users = {
            "user@example.com": {
                "password": "oldpassword123"
            },
            "testuser@example.com": {
                "password": "testpassword123"
            }
        }
        # Save this mock data to a file
        save_users(self.users)
        
        self.app = Application()
        self.app.withdraw()  # Hide the root window

    def tearDown(self):
        """Remove the mock users file after tests."""
        if os.path.exists("users.json"):
            os.remove("users.json")

    def test_password_reset_success(self):
        """Test successful password reset."""
        email = "user@example.com"
        
        # Create a PasswordRecoveryFrame for testing
        recovery_frame = PasswordRecoveryFrame(self.app)
        recovery_frame.email_entry.insert(0, email)
        
        # Simulate clicking the reset button
        recovery_frame.reset_password()

        # Check if the new password is set to "Temp1234"
        self.assertEqual(self.users[email]["password"], "Temp1234")

        # Ensure that the user is redirected to the login screen
        self.assertIsInstance(self.app.current_frame, self.app.LoginFrame)

    def test_password_reset_failure(self):
        """Test unsuccessful password reset with non-existing email."""
        email = "nonexistent@example.com"
        
        # Create a PasswordRecoveryFrame for testing
        recovery_frame = PasswordRecoveryFrame(self.app)
        recovery_frame.email_entry.insert(0, email)
        
        # Simulate clicking the reset button
        recovery_frame.reset_password()
        
        # Ensure that the error message is shown for invalid email
        self.assertTrue(messagebox.showerror.called)
        self.assertIn("Email not found", messagebox.showerror.call_args[0][1])

    def test_back_button(self):
        """Test the back button functionality."""
        # Create a PasswordRecoveryFrame for testing
        recovery_frame = PasswordRecoveryFrame(self.app)
        
        # Simulate clicking the back button
        recovery_frame.go_back()

        # Ensure the frame switches back to the login screen
        self.assertIsInstance(self.app.current_frame, self.app.LoginFrame)


if __name__ == "__main__":
    unittest.main()
