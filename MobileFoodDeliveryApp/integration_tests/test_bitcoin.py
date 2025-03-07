import unittest
from unittest import mock
from unittest.mock import patch
import tkinter as tk
from tkinter import messagebox
from payment_processing_module import PaymentProcessing  # Import PaymentProcessing class

class TestPaymentProcessing(unittest.TestCase):
    """
    Unit tests for the PaymentProcessing class to ensure payment validation and processing work correctly.
    """
    def setUp(self):
        """
        Sets up the test environment by creating an instance of PaymentProcessing.
        """
        self.payment_processing = PaymentProcessing()

    def test_validate_payment_method_success(self):
        """
        Test case for successful validation of a valid payment method ('credit_card') with valid details.
        """
        payment_details = {"card_number": "1234567812345678", "expiry_date": "12/25", "cvv": "123"}
        result = self.payment_processing.validate_payment_method("credit_card", payment_details)
        self.assertTrue(result)
    
    def test_validate_payment_method_invalid_gateway(self):
        """
        Test case for validation failure due to an unsupported payment method ('bitcoin').
        """
        payment_details = {"card_number": "1234567812345678", "expiry_date": "12/25", "cvv": "123"}
        with self.assertRaises(ValueError) as context:
            self.payment_processing.validate_payment_method("bitcoin", payment_details)
        self.assertEqual(str(context.exception), "Invalid payment method")

    def test_validate_credit_card_invalid_details(self):
        """
        Test case for validation failure due to invalid credit card details (invalid card number and CVV).
        """
        payment_details = {"card_number": "1234", "expiry_date": "12/25", "cvv": "12"}  # Invalid card number and CVV.
        result = self.payment_processing.validate_credit_card(payment_details)
        self.assertFalse(result)

    def test_process_payment_success(self):
        """
        Test case for successful payment processing using the 'credit_card' method with valid details.
        """
        order = {"total_amount": 100.00}
        payment_details = {"card_number": "1234567812345678", "expiry_date": "12/25", "cvv": "123"}

        # Use mock to simulate a successful payment response from the gateway.
        with mock.patch.object(self.payment_processing, 'mock_payment_gateway', return_value={"status": "success"}):
            result = self.payment_processing.process_payment(order, "credit_card", payment_details)
            self.assertEqual(result, "Payment successful, Order confirmed")

    def test_process_payment_failure(self):
        """
        Test case for payment failure due to a declined credit card.
        """
        order = {"total_amount": 100.00}
        payment_details = {"card_number": "1111222233334444", "expiry_date": "12/25", "cvv": "123"}  # Simulate a declined card.

        # Use mock to simulate a failed payment response from the gateway.
        with mock.patch.object(self.payment_processing, 'mock_payment_gateway', return_value={"status": "failure"}):
            result = self.payment_processing.process_payment(order, "credit_card", payment_details)
            self.assertEqual(result, "Payment failed, please try again")

    def test_process_payment_invalid_method(self):
        """
        Test case for payment processing failure due to an invalid payment method ('bitcoin').
        """
        order = {"total_amount": 100.00}
        payment_details = {"card_number": "1234567812345678", "expiry_date": "12/25", "cvv": "123"}

        # No need for mocking, the method will raise an error directly.
        result = self.payment_processing.process_payment(order, "bitcoin", payment_details)
        self.assertIn("Error: Invalid payment method", result)


class BitcoinPaymentGUI:
    def __init__(self, master, payment_processing):
        self.master = master
        self.master.title("Bitcoin Payment")
        self.master.geometry("400x300")
        self.payment_processing = payment_processing
        
        tk.Label(master, text="Sender Address:").pack()
        self.sender_entry = tk.Entry(master, width=50)
        self.sender_entry.pack()
        
        tk.Label(master, text="Recipient Address:").pack()
        self.recipient_entry = tk.Entry(master, width=50)
        self.recipient_entry.pack()
        
        tk.Label(master, text="Amount:").pack()
        self.amount_entry = tk.Entry(master, width=20)
        self.amount_entry.pack()
        
        tk.Button(master, text="Submit Payment", command=self.process_payment).pack(pady=10)
    
    def process_payment(self):
        sender_address = self.sender_entry.get()
        recipient_address = self.recipient_entry.get()
        amount = self.amount_entry.get()
        
        if len(sender_address) < 26 or len(recipient_address) < 26:
            messagebox.showerror("Error", "Invalid Bitcoin address.")
            return
        
        try:
            amount = float(amount)
            if amount <= 0:
                raise ValueError("Amount must be greater than zero.")
        except ValueError:
            messagebox.showerror("Error", "Invalid amount.")
            return
        
        messagebox.showinfo("Success", "Bitcoin payment processed successfully!")
        self.master.quit()

class TestBitcoinPaymentIntegration(unittest.TestCase):
    """
    Integration tests to ensure BitcoinPaymentGUI and PaymentProcessing work together.
    """
    
    def setUp(self):
        """
        Set up the test environment.
        Create an instance of PaymentProcessing and the root Tkinter window.
        """
        self.payment_processing = PaymentProcessing()
        
        # Mocking messagebox to prevent pop-up windows during tests
        self.mock_messagebox = patch('tkinter.messagebox.showinfo').start()
        self.mock_messagebox_error = patch('tkinter.messagebox.showerror').start()

    def tearDown(self):
        """
        Clean up after each test.
        """
        patch.stopall()
    
    def simulate_gui_input(self, amount, sender_address, recipient_address):
        """
        Simulate the user input into the GUI.
        """
        root = tk.Tk()
        app = BitcoinPaymentGUI(root, self.payment_processing)
        
        # Simulate user entering values
        app.sender_entry.insert(0, sender_address)
        app.recipient_entry.insert(0, recipient_address)
        app.amount_entry.insert(0, amount)
        
        # Simulate button click to process payment
        app.process_payment()
        
        return root  # Return the root for manual inspection if needed

    def test_integration_valid_payment(self):
        """
        Test valid Bitcoin payment.
        """
        # Given valid inputs for Bitcoin payment
        amount = "100"
        sender_address = "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa"
        recipient_address = "1Counterparty9ew22fpK5m9LrhFvLFpzrf7H"

        # Mocking the payment gateway response to simulate successful payment
        with patch.object(self.payment_processing, 'mock_payment_gateway', return_value={"status": "success"}):
            self.simulate_gui_input(amount, sender_address, recipient_address)

        # Check that the success message box was shown
        self.mock_messagebox.assert_called_with("Success", "Bitcoin payment processed successfully!")

    def test_integration_invalid_bitcoin_address(self):
        """
        Test Bitcoin payment with an invalid sender/recipient address.
        """
        # Invalid addresses (too short for Bitcoin addresses)
        amount = "100"
        sender_address = "invalid_sender"
        recipient_address = "invalid_recipient"

        self.simulate_gui_input(amount, sender_address, recipient_address)

        # Check that an error message box is shown
        self.mock_messagebox_error.assert_called_with("Error", "Invalid Bitcoin address.")

    def test_integration_invalid_amount(self):
        """
        Test Bitcoin payment with invalid amount.
        """
        # Invalid amount (not a number)
        amount = "invalid_amount"
        sender_address = "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa"
        recipient_address = "1Counterparty9ew22fpK5m9LrhFvLFpzrf7H"

        self.simulate_gui_input(amount, sender_address, recipient_address)

        # Check that an error message box is shown for invalid amount
        self.mock_messagebox_error.assert_called_with("Error", "Invalid amount.")


if __name__ == "__main__":
    unittest.main(verbosity=2, exit=False)
