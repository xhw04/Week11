from supplier import Supplier
from productfactory import ProductFactory
from order import Order, OrderLine
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestValidation(unittest.TestCase):
    def setUp(self):
        self.supplier = Supplier("S001", "TechSupply", "sales@techsupply.com")
        self.product = ProductFactory.create("physical", "P001", "Lamp",
                                             25.0, 10, self.supplier)

    def test_zero_price_rejected(self):
        with self.assertRaises(ValueError):
            ProductFactory.create("physical", "P002", "Bad", 0, 5,
                                  self.supplier)

    def test_negative_price_rejected(self):
        with self.assertRaises(ValueError):
            ProductFactory.create("digital", "D002", "Bad", -1, 5,
                                  self.supplier)

    def test_negative_stock_rejected_on_creation(self):
        with self.assertRaises(ValueError):
            ProductFactory.create("physical", "P003", "Bad", 5.0, -1,
                                  self.supplier)

    def test_negative_stock_rejected_on_update(self):
        with self.assertRaises(ValueError):
            self.product.update_stock(-5)

    def test_digital_product_keeps_the_same_stock_rule(self):
        digital = ProductFactory.create("digital", "D001", "Editor", 49.9,
                                        100, self.supplier)
        with self.assertRaises(ValueError):
            digital.update_stock(-1)

    def test_zero_order_quantity_rejected(self):
        with self.assertRaises(ValueError):
            OrderLine(self.product, 0)

    def test_negative_order_quantity_rejected(self):
        order = Order("O001")
        with self.assertRaises(ValueError):
            order.add_order_line(self.product, -2)


if __name__ == "__main__":
    unittest.main()
