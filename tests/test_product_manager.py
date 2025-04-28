import unittest
from src.product_manager import load_products

class TestProductManager(unittest.TestCase):
    
    def setUp(self):
        """Setup the test environment."""
        self.products_file = "data/products.txt"
        self.products = load_products(self.products_file)

    def test_load_products(self):
        """Test that products are loaded from the file."""
        self.assertGreater(len(self.products), 0, "No products loaded from file")

    def test_load_products_file_exists(self):
        """Test that the products file exists."""
        self.assertTrue(self.products_file, "Products file does not exist")

    def test_load_products_file_not_empty(self):
        """Test that the products file is not empty."""
        with open(self.products_file, 'r') as file:
            self.assertGreater(len(file.read()), 0, "Products file is empty")

    def test_load_products_type(self):
        """Test that the loaded products are of the correct type."""
        self.assertIsInstance(self.products, list, "Loaded products are not a list")

    def test_load_products_content(self):
        """Test that the loaded products have the correct content."""
        for product in self.products:
            self.assertIsInstance(product, dict, "Product is not a dictionary")
            self.assertIn('name', product, "Product does not have a name")
            self.assertIn('price', product, "Product does not have a price")

if __name__ == "__main__":
    unittest.main()