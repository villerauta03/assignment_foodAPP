import unittest
from Payment_Processing import PaymentProcessing

class TestApplyDiscount(unittest.TestCase):
    def setUp(self):
        self.payment_processing = PaymentProcessing()

    def test_percentage_discount(self):
        # Test basic percentage discount
        total_price = 100
        discount_amount = 10  # 10%
        result = self.payment_processing.apply_discount(total_price, discount_amount, "percentage")
        self.assertEqual(result, 90)  # 10% off 100 is 90

    def test_fixed_discount(self):
        # Test basic fixed discount
        total_price = 100
        discount_amount = 20  # Fixed amount
        result = self.payment_processing.apply_discount(total_price, discount_amount, "fixed")
        self.assertEqual(result, 80)  # 100 - 20 = 80

if __name__ == "__main__":
    unittest.main()
