import unittest
from src.sale_manager import process_sale

class TestSaleManager(unittest.TestCase):
    """
    Test suite for the sale manager functionality.
    """

    def setUp(self):
        """
        Setup method to initialize test data.
        """
        self.sale_data = {
            'product_id': 1,
            'quantity': 2,
            'price': 10.99
        }

    def test_process_sale(self):
        """
        Test the sale process logic.

        This test case should simulate sales and verify the results.
        """
        # Simulate a sale
        result = process_sale(self.sale_data)

        # Verify the result
        self.assertIsNotNone(result)
        self.assertIsInstance(result, dict)
        self.assertIn('total', result)
        self.assertIn('tax', result)
        self.assertGreaterEqual(result['total'], 0)
        self.assertGreaterEqual(result['tax'], 0)

    def test_process_sale_with_zero_quantity(self):
        """
        Test the sale process logic with zero quantity.

        This test case should simulate sales with zero quantity and verify the results.
        """
        # Simulate a sale with zero quantity
        sale_data = {
            'product_id': 1,
            'quantity': 0,
            'price': 10.99
        }
        result = process_sale(sale_data)

        # Verify the result
        self.assertIsNotNone(result)
        self.assertIsInstance(result, dict)
        self.assertIn('total', result)
        self.assertIn('tax', result)
        self.assertEqual(result['total'], 0)
        self.assertEqual(result['tax'], 0)

    def test_process_sale_with_negative_quantity(self):
        """
        Test the sale process logic with negative quantity.

        This test case should simulate sales with negative quantity and verify the results.
        """
        # Simulate a sale with negative quantity
        sale_data = {
            'product_id': 1,
            'quantity': -1,
            'price': 10.99
        }
        result = process_sale(sale_data)

        # Verify the result
        self.assertIsNotNone(result)
        self.assertIsInstance(result, dict)
        self.assertIn('total', result)
        self.assertIn('tax', result)
        self.assertGreaterEqual(result['total'], 0)
        self.assertGreaterEqual(result['tax'], 0)

    def test_process_sale_with_zero_price(self):
        """
        Test the sale process logic with zero price.

        This test case should simulate sales with zero price and verify the results.
        """
        # Simulate a sale with zero price
        sale_data = {
            'product_id': 1,
            'quantity': 2,
            'price': 0
        }
        result = process_sale(sale_data)

        # Verify the result
        self.assertIsNotNone(result)
        self.assertIsInstance(result, dict)
        self.assertIn('total', result)
        self.assertIn('tax', result)
        self.assertEqual(result['total'], 0)
        self.assertEqual(result['tax'], 0)

    def test_process_sale_with_negative_price(self):
        """
        Test the sale process logic with negative price.

        This test case should simulate sales with negative price and verify the results.
        """
        # Simulate a sale with negative price
        sale_data = {
            'product_id': 1,
            'quantity': 2,
            'price': -10.99
        }
        result = process_sale(sale_data)

        # Verify the result
        self.assertIsNotNone(result)
        self.assertIsInstance(result, dict)
        self.assertIn('total', result)
        self.assertIn('tax', result)
        self.assertGreaterEqual(result['total'], 0)
        self.assertGreaterEqual(result['tax'], 0)

if __name__ == "__main__":
    unittest.main()