from supplier import Supplier
from productfactory import ProductFactory
from order import Order
from discountstrategy import (DiscountStrategy, NoDiscount,
                              PercentageDiscount, BulkDiscount,
                              StudentDiscount)
import inspect
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def make_order(discount=None) -> Order:
    supplier = Supplier("S001", "TechSupply", "sales@techsupply.com")
    product = ProductFactory.create("physical", "P001", "Item", 250.0, 10,
                                    supplier)
    order = Order("O001", discount)
    order.add_order_line(product, 1)   # lines add up to 250
    return order


class TestDiscounts(unittest.TestCase):
    def test_no_discount_is_default(self):
        self.assertAlmostEqual(make_order().calculate_total(), 250.0)

    def test_bulk_discount_over_threshold(self):
        order = make_order(BulkDiscount(200, 20))
        self.assertAlmostEqual(order.calculate_total(), 230.0)

    def test_bulk_discount_under_threshold(self):
        order = make_order(BulkDiscount(300, 20))
        self.assertAlmostEqual(order.calculate_total(), 250.0)

    def test_percentage_discount(self):
        order = make_order(PercentageDiscount(10))
        self.assertAlmostEqual(order.calculate_total(), 225.0)

    def test_set_discount_changes_strategy(self):
        order = make_order(BulkDiscount(200, 20))
        self.assertAlmostEqual(order.calculate_total(), 230.0)
        order.set_discount(PercentageDiscount(10))
        self.assertAlmostEqual(order.calculate_total(), 225.0)

    def test_new_strategy_needs_no_change_to_order(self):
        order = make_order(StudentDiscount())
        self.assertAlmostEqual(order.calculate_total(), 237.5)

    def test_order_has_no_discount_if_elif_logic(self):
        source = inspect.getsource(Order.calculate_total)
        self.assertNotIn("elif", source)
        self.assertNotIn("percentage", source)

    def test_strategies_inherit_from_base(self):
        for strategy in (NoDiscount(), PercentageDiscount(5),
                         BulkDiscount(10, 1), StudentDiscount()):
            self.assertIsInstance(strategy, DiscountStrategy)

    def test_base_strategy_is_abstract(self):
        with self.assertRaises(TypeError):
            DiscountStrategy()

    def test_invalid_percentage_rejected(self):
        with self.assertRaises(ValueError):
            PercentageDiscount(150)


if __name__ == "__main__":
    unittest.main()
