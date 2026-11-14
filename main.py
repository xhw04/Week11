# -FILE HANDLING-
# loading inventory.json
# saving inventory.json

# -MAIN-
# displaying the main menu
# 1. Display all products
# 2. Add a product
# 3. Update stock
# 4. Search for a product
# 5. Save inventory
# 6. Exit

import json
import os
from inventory import Inventory
from product import Product
from supplier import Supplier
from productfactory import ProductFactory
from input_helpers import get_positive_float

file_name = "inventory.json"


# 5.save
def save_inventory(inventory: Inventory) -> None:
    data = [p.to_dict() for p in inventory.get_products()]
    with open(file_name, "w") as file:
        json.dump(data, file, indent=4)


# load: the factory picks the right subclass using "Type"
def create_product_from_dict(item: dict) -> Product:
    s = item["Supplier"]
    supplier = Supplier(s["ID"], s["Name"], s["Email"])
    extra = item.get("Weight", item.get("Download_size"))
    return ProductFactory.create(item["Type"], item["ID"], item["Name"],
                                 item["Price"], item["Stock"], supplier, extra)


# 1.display (load)
def load_inventory() -> Inventory:
    inventory = Inventory()
    if os.path.exists(file_name):
        with open(file_name, "r") as file:
            data = json.load(file)
        for item in data:
            try:
                inventory.add_product(create_product_from_dict(item))
            except (KeyError, ValueError) as error:
                print(f"Skipping bad record: {error}")
        print("inventory.json found. Inventory loaded successfully.")
    else:
        print("inventory.json not found. Creating default inventory.")
        supplier = Supplier("S001", "TechSupply", "sales@techsupply.com")
        inventory.add_product(ProductFactory.create(
            "physical", "P001", "Laptop", 1200.00, 15, supplier, 2.1))
        inventory.add_product(ProductFactory.create(
            "physical", "P002", "Mouse", 25.50, 40, supplier, 0.1))
        inventory.add_product(ProductFactory.create(
            "digital", "P003", "Antivirus", 45.00, 25, supplier, 300))
        save_inventory(inventory)
    return inventory


def add_product_menu(inventory: Inventory) -> None:
    print("\nAdd New Product")
    print("1. Physical product")
    print("2. Digital product")
    choice = input("Choose type (1/2): ")
    if choice not in ("1", "2"):
        print("Invalid type.")
        return
    product_type = "physical" if choice == "1" else "digital"

    product_id = input("Product ID: ")
    name = input("Product Name: ")
    price = get_positive_float("Price: ")
    supplier = Supplier(input("Supplier ID: "), input("Supplier Name: "),
                        input("Supplier Email: "))
    try:
        stock = int(input("Stock Quantity: "))
        label = "Weight (kg): " if product_type == "physical" else "Download size (MB): "
        extra = float(input(label))
        product = ProductFactory.create(product_type, product_id, name,
                                        price, stock, supplier, extra)
    except ValueError as error:
        print(f"Could not add product: {error}")
        return

    if inventory.add_product(product):
        print("\nProduct added successfully!")


def update_stock_menu(inventory: Inventory) -> None:
    print("\nUpdate Stock")
    product = inventory.find_product(input("Enter Product ID: "))
    if product is None:
        print("Product not found.")
        return
    product.display_information()
    try:
        quantity = int(input("New Stock Quantity: "))
        product.update_stock(quantity)
    except ValueError as error:
        print(f"Could not update stock: {error}")
        return
    print("\nStock updated successfully!")

# 4.search product


def search_product_menu(inventory: Inventory) -> None:
    print("\nSearch Product")
    product = inventory.find_product(input("Enter Product ID: "))
    if product is None:
        print("Product not found.")
    else:
        print("Product Found")
        product.display_information()
        print(product.get_fulfilment_info())
        product.get_supplier().display_information()


def main() -> None:
    print("============")
    print("INVENTORY MANAGEMENT SYSTEM")
    print("============\n")
    inventory = load_inventory()

    while True:
        print("\n-----------MENU------------")
        print("1. Display All Products")
        print("2. Add Product")
        print("3. Update Stock")
        print("4. Search Product")
        print("5. Save Inventory")
        print("6. Exit")
        print("---------------------------")

        try:
            choice = int(input("Enter option: "))
        except ValueError:
            print("Please enter a number 1-6.")
            continue

        if choice == 1:
            inventory.display_all()
        elif choice == 2:
            add_product_menu(inventory)
        elif choice == 3:
            update_stock_menu(inventory)
        elif choice == 4:
            search_product_menu(inventory)
        elif choice == 5:
            save_inventory(inventory)
            print("Inventory saved successfully to inventory.json.")
        elif choice == 6:
            save_inventory(inventory)
            print("Inventory saved. Thank you for using Inventory Management System.")
            break
        else:
            print("Invalid option.")


# call main
main()
