import unittest
import tkinter as tk
from main import Application  # Import your main application
from User_Profile import UserProfilePage  # Import user profile

class TestUserProfileMinimal(unittest.TestCase):
    def setUp(self):
        # Create an instance of the application
        self.app = Application()
        self.test_email = "test@example.com"
        # Set up a test user
        self.app.registration.users[self.test_email] = {
            "password": "Password123",
            "confirmed": True,
            "full_name": "Test User",
            "home_address": "Old Address"
        }
        # Log in as the test user
        self.app.login_user(self.test_email)
    
    def tearDown(self):
        # Destroy the application instance
        self.app.destroy()

    def test_user_profile_update(self):
        # Navigate to user profile page
        self.app.show_profile_page(self.test_email)
        self.assertIsInstance(self.app.current_frame, UserProfilePage)

        profile_page = self.app.current_frame
        # Simulate user input: update full name
        new_full_name = "Kake Rantala"
        profile_page.full_name_entry.delete(0, tk.END)
        profile_page.full_name_entry.insert(0, new_full_name)
        profile_page.save_changes()

        # Verify that the user's full name has been updated
        updated_data = self.app.registration.users[self.test_email]
        self.assertEqual(updated_data["full_name"], new_full_name)

if __name__ == '__main__':
    unittest.main()
