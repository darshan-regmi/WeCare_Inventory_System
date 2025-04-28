import unittest
from src.restock_manager import restock_products

class TestRestockManager(unittest.TestCase):
    
    def setUp(self):
        """
        Set up initial product quantities for each test.
        """
        self.initial_quantities = {"product1": 10, "product2": 20}
        self.expected_quantities = {"product1": 15, "product2": 25}

    def test_restock_products(self):
        """
        Test the restocking logic by simulating a restock and verifying the updates.
        """
        # Act: Simulate a restock
        restock_products(self.initial_quantities)
        
        # Assert: Verify the updated product quantities
        self.assertEqual(self.initial_quantities, self.expected_quantities)

    def test_restock_products_empty(self):
        """
        Test the restocking logic with an empty product dictionary.
        """
        # Arrange: Set up an empty product dictionary
        empty_quantities = {}
        
        # Act: Simulate a restock
        restock_products(empty_quantities)
        
        # Assert: Verify the updated product quantities
        self.assertEqual(empty_quantities, {})

    def test_restock_products_none(self):
        """
        Test the restocking logic with a None product dictionary.
        """
        # Act: Simulate a restock
        with self.assertRaises(TypeError):
            restock_products(None)

if __name__ == "__main__":
    unittest.main()