import unittest
from unittest import mock
import tkinter as tk
from tkinter import messagebox


class PaymentProcessing:
    def __init__(self):
        self.available_gateways = ["credit_card", "paypal"]

    def validate_payment_method(self, payment_method, payment_details):
        if payment_method not in self.available_gateways:
            raise ValueError("Invalid payment method")
        if payment_method == "credit_card":
            if not self.validate_credit_card(payment_details):
                raise ValueError("Invalid credit card details")
        return True

    def validate_credit_card(self, details):
        card_number = details.get("card_number", "")
        expiry_date = details.get("expiry_date", "")
        cvv = details.get("cvv", "")
        if len(card_number) != 16 or len(cvv) != 3:
            return False
        return True
    
    def apply_discount(self, total_price, discount_amount, discount_type="percentage"):
        if discount_type == "percentage":
            total_price -= (total_price * (discount_amount / 100))
        elif discount_type == "fixed":
            total_price -= discount_amount
        return max(total_price, 0)  
        
    def process_payment(self, order, payment_method, payment_details, discount_amount=0, discount_type="percentage"):
        try:
            self.validate_payment_method(payment_method, payment_details)
            order["total_amount"] = self.apply_discount(order["total_amount"], discount_amount, discount_type)
            payment_response = self.mock_payment_gateway(payment_method, payment_details, order["total_amount"])
            if payment_response["status"] == "success":
                return "Payment successful, Order confirmed"
            else:
                return "Payment failed, please try again"
        except Exception as e:
            return f"Error: {str(e)}"

    def mock_payment_gateway(self, method, details, amount):
        if method == "credit_card" and details["card_number"] == "1111222233334444":
            return {"status": "failure", "message": "Card declined"}
        return {"status": "success", "transaction_id": "abc123"}


class TestPaymentProcessing(unittest.TestCase):
    def setUp(self):
        self.payment_processing = PaymentProcessing()
    
    def test_apply_discount_percentage(self):
        result = self.payment_processing.apply_discount(100, 10, "percentage")
        self.assertEqual(result, 90)
    
    def test_apply_discount_fixed(self):
        result = self.payment_processing.apply_discount(100, 20, "fixed")
        self.assertEqual(result, 80)
    
    def test_process_payment_with_discount(self):
        order = {"total_amount": 100.00}
        payment_details = {"card_number": "1234567812345678", "expiry_date": "12/25", "cvv": "123"}
        with mock.patch.object(self.payment_processing, 'mock_payment_gateway', return_value={"status": "success"}):
            result = self.payment_processing.process_payment(order, "credit_card", payment_details, 10, "percentage")
            self.assertEqual(result, "Payment successful, Order confirmed")


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


if __name__ == "__main__":
    root = tk.Tk()
    payment_processing = PaymentProcessing()
    app = BitcoinPaymentGUI(root, payment_processing)
    
    # Running the unit tests
    unittest.main(verbosity=2, exit=False)
    
    root.mainloop()
