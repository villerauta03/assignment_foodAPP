import unittest 
from Order_Placement import Cart, OrderPlacement, UserProfile, RestaurantMenu, PaymentMethod 

class TestOrderPlacementIntegration(unittest.TestCase): 

    def setUp(self): 
        self.restaurant_menu = RestaurantMenu(available_items=["Burger", "Pizza", "Salad"]) 
        self.user_profile = UserProfile(delivery_address="123 Main St") 
        self.cart = Cart() 
        self.order = OrderPlacement(self.cart, self.user_profile, self.restaurant_menu) 

    def test_delivery_fee_free(self): 
        # Add items to the cart to make the total over 80         
        self.cart.add_item("Pizza", 50.00, 2)  # Total will be 100 + tax 
        total_info = self.order.cart.calculate_total() 
        self.assertEqual(total_info["delivery_fee"], 0.00) 
        self.assertTrue(total_info["total"] > 80) 

    def test_delivery_fee_not_free(self): 
        # Add items to the cart to make the total less than or equal to 80 
        self.cart.add_item("Pizza", 30.00, 2)  # Total will be 60 + tax 
        total_info = self.order.cart.calculate_total() 
        self.assertEqual(total_info["delivery_fee"], 5.00) 
        self.assertTrue(total_info["total"] <= 80) 


if __name__ == "__main__": 
    unittest.main() 
