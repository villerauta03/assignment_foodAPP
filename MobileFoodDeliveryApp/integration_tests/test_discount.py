import unittest
from unittest import mock
from Payment_Processing.py import PaymentProcessing  # Import the PaymentProcessing class from the other file

class TestPaymentProcessing(unittest.TestCase):
    def setUp(self):
        self.payment_processing = PaymentProcessing()

    def test_apply_discount_percentage(self):
        """
        Test that the percentage discount is applied correctly.
        """
        result = self.payment_processing.apply_discount(100, 10, "percentage")
        self.assertEqual(result, 90)  # 10% off 100 is 90

    def test_apply_discount_fixed(self):
        """
        Test that the fixed discount is applied correctly.
        """
        result = self.payment_processing.apply_discount(100, 20, "fixed")
        self.assertEqual(result, 80)  # 20 off 100 is 80

    def test_process_payment_with_percentage_discount(self):
        """
        Test the complete payment process with a percentage discount.
        """
        order = {"total_amount": 100.00}
        payment_details = {"card_number": "1234567812345678", "expiry_date": "12/25", "cvv": "123"}
        
        # Mock the payment gateway response to simulate a successful payment
        with mock.patch.object(self.payment_processing, 'mock_payment_gateway', return_value={"status": "success"}):
            result = self.payment_processing.process_payment(order, "credit_card", payment_details, 10, "percentage")
            self.assertEqual(result, "Payment successful, Order confirmed")

    def test_process_payment_with_fixed_discount(self):
        """
        Test the complete payment process with a fixed discount.
        """
        order = {"total_amount": 100.00}
        payment_details = {"card_number": "1234567812345678", "expiry_date": "12/25", "cvv": "123"}
        
        # Mock the payment gateway response to simulate a successful payment
        with mock.patch.object(self.payment_processing, 'mock_payment_gateway', return_value={"status": "success"}):
            result = self.payment_processing.process_payment(order, "credit_card", payment_details, 20, "fixed")
            self.assertEqual(result, "Payment successful, Order confirmed")

    def test_process_payment_with_invalid_discount_type(self):
        """
        Test the complete payment process with an invalid discount type.
        """
        order = {"total_amount": 100.00}
        payment_details = {"card_number": "1234567812345678", "expiry_date": "12/25", "cvv": "123"}

        # Mock the payment gateway response to simulate a successful payment
        with mock.patch.object(self.payment_processing, 'mock_payment_gateway', return_value={"status": "success"}):
            result = self.payment_processing.process_payment(order, "credit_card", payment_details, 50, "unknown")
            self.assertEqual(result, "Payment successful, Order confirmed")  # This will still proceed, as the code handles unknown discount types.

    def test_process_payment_with_zero_discount(self):
        """
        Test the complete payment process with no discount (0% or 0 amount).
        """
        order = {"total_amount": 100.00}
        payment_details = {"card_number": "1234567812345678", "expiry_date": "12/25", "cvv": "123"}
        
        # Mock the payment gateway response to simulate a successful payment
        with mock.patch.object(self.payment_processing, 'mock_payment_gateway', return_value={"status": "success"}):
            result = self.payment_processing.process_payment(order, "credit_card", payment_details, 0, "percentage")
            self.assertEqual(result, "Payment successful, Order confirmed")

    def test_process_payment_with_discount_resulting_in_zero(self):
        """
        Test that the total amount doesn't go below zero after applying a discount.
        """
        order = {"total_amount": 50.00}
        payment_details = {"card_number": "1234567812345678", "expiry_date": "12/25", "cvv": "123"}

        # Apply a large discount that would make the total amount negative
        result = self.payment_processing.apply_discount(order["total_amount"], 100, "percentage")
        self.assertEqual(result, 0)  # Total should not go below 0

if __name__ == "__main__":
    unittest.main()
