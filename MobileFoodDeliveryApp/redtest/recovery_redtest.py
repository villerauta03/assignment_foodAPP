import unittest
from unittest.mock import patch
from tkinter import Tk
from main import Application, PasswordRecoveryFrame, save_users, load_users  # Replace with your actual module and imports

class TestPasswordRecovery(unittest.TestCase):
    def setUp(self):
        # Mock user data
        self.users = {"user@example.com": {"password": "oldpassword123"}}
        save_users(self.users)  # Save the mock users to the file
        self.app = Application()
        self.app.withdraw()  # Hide the root window

    def tearDown(self):
        # Clean up saved users file
        import os
        if os.path.exists("users.json"):
            os.remove("users.json")

    def test_password_reset_success(self):
        email = "user@example.com"
        frame = PasswordRecoveryFrame(self.app)
        frame.email_entry.insert(0, email)
        frame.reset_password()

        updated_users = load_users()
        self.assertEqual(updated_users[email]["password"], "Temp1234")  # Verify password was updated

    @patch("tkinter.messagebox.showerror")
    def test_password_reset_failure(self, mock_showerror):
        email = "invalid@example.com"
        frame = PasswordRecoveryFrame(self.app)
        frame.email_entry.insert(0, email)
        frame.reset_password()

        mock_showerror.assert_called_once_with("Error", "Email not found.")  # Verify error message is shown

if __name__ == "__main__":
    unittest.main()
