import unittest
import tkinter as tk
from main import Application, MainAppFrame  #import classes where changes were made
from User_Profile.py import UserProfilePage       # import user profile


class TestIntegrationUserProfile(unittest.TestCase):

    def setUp(self):
        #Create an instance of app
        self.app = Application()
        #create test user
        self.test_email = "test@example.com"
        self.app.registration.users[self.test_email] = {"password": "Password123", "confirmed": True}
        #test login with the test user
        self.app.login_user(self.test_email)
    
    def tearDown(self):
        # destroy tkinter application after each test made
        self.app.destroy()
    
    def test_user_profile_integration(self):
        #go to user profile page
        self.app.show_profile_page(self.test_email)
        self.assertIsInstance(self.app.current_frame, UserProfilePage)
        profile_page = self.app.current_frame
        
        #new profile data for test
        new_full_name = "kake rantala"
        new_home_address = "moisiontie"
        
        #simulate user input by updating fields
        profile_page.full_name_entry.delete(0, tk.END)
        profile_page.full_name_entry.insert(0, new_full_name)
        profile_page.address_entry.delete(0, tk.END)
        profile_page.address_entry.insert(0, new_home_address)
        
        #save changes on profile page
        profile_page.save_changes()
        
        #verify that the registration data has been updated
        updated_data = self.app.registration.users[self.test_email]
        self.assertEqual(updated_data.get("full_name"), new_full_name)
        self.assertEqual(updated_data.get("home_address"), new_home_address)
        

        #test back button
        profile_page.go_back()
        #check that back button worked as intended ---> mainappframe
        self.assertIsInstance(self.app.current_frame, MainAppFrame)


if __name__ == '__main__':
    unittest.main()
