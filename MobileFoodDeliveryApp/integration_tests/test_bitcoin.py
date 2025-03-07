import unittest
from unittest import mock
from Payment_Processing.py import PaymentProcessing  # Import PaymentProcessing class from the other file

class TestBitcoinPaymentProcessing(unittest.TestCase):
    def setUp(self):
        self.payment_processing = PaymentProcessing()

    def test_validate_bitcoin_address_valid(self):
        payment_details = {"sender_address": "validbitcoinaddressvalid"}
        result = self.payment_processing.validate_bitcoin_address(payment_details["sender_address"])
        self.assertTrue(result)

    def test_validate_bitcoin_address_invalid(self):
        payment_details = {"sender_address": "invalidbitcoinaddress"}
        result = self.payment_processing.validate_bitcoin_address(payment_details["sender_address"])
        self.assertFalse(result)

    def test_process_bitcoin_payment_success(self):
        order = {"total_amount": 100.00}
        payment_details = {"sender_address": "validbitcoinaddressvalid"}
        
        with mock.patch.object(self.payment_processing, 'mock_payment_gateway', return_value={"status": "success"}):
            result = self.payment_processing.process_payment(order, "bitcoin", payment_details)
            self.assertEqual(result, "Payment successful, Order confirmed")

    def test_process_bitcoin_payment_failure(self):
        order = {"total_amount": 100.00}
        payment_details = {"sender_address": "invalidbitcoinaddress"}

        with mock.patch.object(self.payment_processing, 'mock_payment_gateway', return_value={"status": "failure", "message": "Invalid Bitcoin address"}):
            result = self.payment_processing.process_payment(order, "bitcoin", payment_details)
            self.assertEqual(result, "Payment failed, please try again")

if __name__ == "__main__":
    unittest.main()
