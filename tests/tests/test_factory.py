from supplier import Supplier
from productfactory import ProductFactory
from product import Product
from physicalproduct import PhysicalProduct
from digitalproduct import DigitalProduct
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestProductFactory(unittest.TestCase):
    def setUp(self):
        self.supplier = Supplier("S001", "TechSupply", "sales@techsupply.com")

    def test_creates_physical_product(self):
        product = ProductFactory.create("physical", "P001", "Lamp", 25.0,
                                        10, self.supplier, 2.0)
        self.assertIsInstance(product, PhysicalProduct)

    def test_creates_digital_product(self):
        product = ProductFactory.create("digital", "D001", "Editor", 49.9,
                                        100, self.supplier, 500)
        self.assertIsInstance(product, DigitalProduct)

    def test_returns_product_type(self):
        product = ProductFactory.create("physical", "P001", "Lamp", 25.0,
                                        10, self.supplier)
        self.assertIsInstance(product, Product)

    def test_unknown_type_raises_clear_error(self):
        with self.assertRaises(ValueError) as context:
            ProductFactory.create("service", "S001", "Install", 30.0, 5,
                                  self.supplier)
        self.assertIn("Unknown product type: service", str(context.exception))


if __name__ == "__main__":
    unittest.main()
