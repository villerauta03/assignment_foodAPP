import tkinter as tk
from tkinter import messagebox

class UserProfilePage(tk.Frame):

    def __init__(self, master, user_email, user_data):
        super().__init__(master)
        self.master = master
        self.user_email = user_email
        self.user_data = user_data  #incase old user data
        tk.Label(self, text="User Profile", font=("Arial", 16)).grid(row=0, column=0, columnspan=2, pady=10)

        #display the user email
        tk.Label(self, text="Email:", font=("Arial", 12)).grid(row=1, column=0, sticky="w", padx=5)
        tk.Label(self, text=user_email, font=("Arial", 12)).grid(row=1, column=1, sticky="w", padx=5)

        #row for full name
        tk.Label(self, text="Full Name:", font=("Arial", 12)).grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.full_name_value = tk.Label(self, text=self.user_data.get("full_name", ""), font=("Arial", 12))
        self.full_name_value.grid(row=2, column=1, sticky="w", padx=5, pady=5)

        #field to update name
        tk.Label(self, text="Enter new full name:", font=("Arial", 10)).grid(row=3, column=0, sticky="w", padx=5)
        self.full_name_entry = tk.Entry(self, width=40)
        self.full_name_entry.grid(row=3, column=1, sticky="w", padx=5)
        self.full_name_entry.insert(0, self.user_data.get("full_name", ""))

        #row for Home Address display and label
        tk.Label(self, text="Home Address:", font=("Arial", 12)).grid(row=4, column=0, sticky="w", padx=5, pady=5)
        self.address_value = tk.Label(self, text=self.user_data.get("home_address", ""), font=("Arial", 12))
        self.address_value.grid(row=4, column=1, sticky="w", padx=5, pady=5)

        #entry field to update address
        tk.Label(self, text="Enter new address:", font=("Arial", 10)).grid(row=5, column=0, sticky="w", padx=5)
        self.address_entry = tk.Entry(self, width=40)
        self.address_entry.grid(row=5, column=1, sticky="w", padx=5)
        self.address_entry.insert(0, self.user_data.get("home_address", ""))

        #Save Changes button updates stored data and labels
        tk.Button(self, text="Save Changes", command=self.save_changes).grid(row=6, column=0, columnspan=2, pady=10)

        #back button returns to the main page
        tk.Button(self, text="Back", command=self.go_back).grid(row=7, column=0, columnspan=2, pady=5)

    def save_changes(self): #Save changes  full name, address
        full_name = self.full_name_entry.get().strip()
        home_address = self.address_entry.get().strip()
        self.user_data["full_name"] = full_name
        self.user_data["home_address"] = home_address

        #update labels
        self.full_name_value.config(text=full_name)
        self.address_value.config(text=home_address)

        #update stored user data
        self.master.registration.users[self.user_email] = self.user_data

        messagebox.showinfo("Profile Updated", "Your profile has been updated successfully!")

    def go_back(self): #return to main page 
        self.master.login_user(self.user_email)
