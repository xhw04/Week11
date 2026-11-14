import csv
from inventory import Inventory
from productfactory import ProductFactory
from supplier import Supplier


def load_products(path: str, inventory: Inventory, supplier: Supplier) -> None:
    loaded = 0
    try:
        file = open(path, newline="")
    except FileNotFoundError:
        print(f"Products file not found: {path}")
    else:
        with file:
            reader = csv.reader(file)
            next(reader, None)   # skip the header row
            for line_number, row in enumerate(reader, start=2):
                try:
                    if len(row) < 5:
                        raise ValueError("Row needs 5 columns.")
                    product = ProductFactory.create(
                        row[0], row[1], row[2], float(row[3]), int(row[4]),
                        supplier)
                    if inventory.add_product(product):
                        loaded += 1
                except ValueError as error:
                    print(f"Skipping row {line_number}: {error}")
        print(f"{loaded} products loaded.")
    finally:
        print("Load attempt finished.")
