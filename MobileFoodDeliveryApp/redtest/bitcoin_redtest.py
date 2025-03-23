import unittest
from tkinter import Tk
from Payment_Processing import BitcoinPaymentGUI, PaymentProcessing  # Adjusted to use Payment_Processing

class TestBitcoinPayment(unittest.TestCase):
    def setUp(self):
        self.root = Tk()  # Create a Tkinter root window
        self.payment_processing = PaymentProcessing()  # Instantiate PaymentProcessing
        self.app = BitcoinPaymentGUI(self.root, self.payment_processing)  # Create the GUI instance
    
    def test_bitcoin_valid_payment(self):
        # Simulate valid Bitcoin details
        self.app.sender_entry.insert(0, "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa")  # Valid Bitcoin address
        self.app.recipient_entry.insert(0, "3J98t1WpEZ73CNmQviecrnyiWrnqRhWNLy")  # Another valid Bitcoin address
        self.app.amount_entry.insert(0, "0.01")  # Valid amount
        
        try:
            self.app.process_payment()
            self.assertTrue(True)  # If no exception, test passes
        except Exception as e:
            self.fail(f"Bitcoin payment processing raised an exception: {e}")

if __name__ == "__main__":
    unittest.main()
