from supplier import Supplier
from product_loader import load_products
from inventory import Inventory
from input_helpers import get_positive_float
import contextlib
import io
import os
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


CSV_TEXT = (
    "product_type,product_id,name,price,stock_quantity\n"
    "physical,P001,Desk Lamp,25.00,10\n"
    "digital,D001,Photo Editor,49.90,100\n"
    "service,S001,Installation,30.00,5\n"
    "physical,P002,Office Chair,abc,3\n"
    "physical,P003,Monitor Stand,39.50,7\n"
)


class TestGetPositiveFloat(unittest.TestCase):
    def test_asks_again_until_valid(self):
        output = io.StringIO()
        with patch("builtins.input", side_effect=["abc", "-5", "12.50"]):
            with contextlib.redirect_stdout(output):
                result = get_positive_float("Price: ")
        self.assertEqual(result, 12.5)
        self.assertIn("Please enter a valid number", output.getvalue())
        self.assertIn("greater than zero", output.getvalue())

    def test_zero_is_rejected(self):
        with patch("builtins.input", side_effect=["0", "3"]):
            with contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(get_positive_float("Price: "), 3.0)


class TestLoadProducts(unittest.TestCase):
    def setUp(self):
        self.supplier = Supplier("S001", "TechSupply", "sales@techsupply.com")
        self.inventory = Inventory()

    def run_load(self, path):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            load_products(path, self.inventory, self.supplier)
        return output.getvalue()

    def test_missing_file_is_handled(self):
        text = self.run_load("does_not_exist.csv")
        self.assertIn("Products file not found", text)
        self.assertIn("Load attempt finished.", text)
        self.assertEqual(len(self.inventory.get_products()), 0)

    def test_bad_rows_skipped_and_valid_rows_loaded(self):
        with tempfile.TemporaryDirectory() as folder:
            path = os.path.join(folder, "products.csv")
            with open(path, "w", newline="") as file:
                file.write(CSV_TEXT)
            text = self.run_load(path)
        self.assertEqual(len(self.inventory.get_products()), 3)
        self.assertIn("Skipping row 4", text)   # unknown type "service"
        self.assertIn("Skipping row 5", text)   # price "abc"
        self.assertIn("3 products loaded.", text)
        self.assertTrue(text.strip().endswith("Load attempt finished."))


if __name__ == "__main__":
    unittest.main()
