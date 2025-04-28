import unittest
from unittest.mock import patch, MagicMock
from src import load_products, process_sale, restock_products

class TestIntegration(unittest.TestCase):
    """
    Integration tests for the entire system.
    """

    def setUp(self):
        """
        Setup the test environment.
        """
        self.products = [
            {"id": 1, "name": "Product 1", "price": 10.99},
            {"id": 2, "name": "Product 2", "price": 9.99},
            {"id": 3, "name": "Product 3", "price": 12.99},
        ]

    @patch('your_module.load_products')
    @patch('your_module.process_sale')
    @patch('your_module.restock_products')
    def test_integration(self, mock_restock_products, mock_process_sale, mock_load_products):
        """
        Test the full flow of loading products, processing a sale, and restocking.
        """
        # Mock the load products function to return the test products
        mock_load_products.return_value = self.products

        # Simulate a full user session
        loaded_products = load_products()
        self.assertEqual(loaded_products, self.products)

        # Process a sale
        sale_result = process_sale(loaded_products[0], 2)
        self.assertTrue(sale_result)

        # Restock products
        restock_result = restock_products(loaded_products[0], 5)
        self.assertTrue(restock_result)

        # Validate the entire system
        mock_process_sale.assert_called_once_with(loaded_products[0], 2)
        mock_restock_products.assert_called_once_with(loaded_products[0], 5)

if __name__ == "__main__":
    unittest.main()