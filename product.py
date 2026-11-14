# -PRODUCT-
# STORE PRODUCT INFO
# MANAGE STATE

from abc import ABC, abstractmethod
from supplier import Supplier


# abstract class, cannot be instantiated, only inherited
class Product(ABC):
    # self.__ (private attributes, only in class)
    def __init__(self, product_id: str, name: str, price: float,
                 stock: int, supplier: Supplier):
        self.__product_id: str = product_id
        self.__name: str = name
        self.__price: float = price
        self.__stock: int = stock
        self.__supplier: Supplier = supplier   # association

    def get_product_id(self) -> str:
        return self.__product_id

    def get_name(self) -> str:
        return self.__name

    # for OrderLine
    def get_price(self) -> float:
        return self.__price

    def get_supplier(self) -> Supplier:
        return self.__supplier

    # display one row of product info
    def display_information(self) -> None:
        print(f"ID:{self.__product_id} | Name:{self.__name} | "
              f"Price:${self.__price} | Stock:{self.__stock}")

    # update stock (encapsulation)
    def update_stock(self, quantity: int) -> bool:
        if quantity < 0:
            print("Stock cannot be negative.")
            return False
        self.__stock = quantity
        return True

    # return as dict due to json (only here)
    def to_dict(self) -> dict:
        return {"ID": self.__product_id, "Name": self.__name,
                "Price": self.__price, "Stock": self.__stock,
                "Supplier": self.__supplier.to_dict()}

    # abstract method, must be implemented in child class
    @abstractmethod
    def get_fulfilment_info(self) -> str:
        pass

    def __init__(self, product_id: str, name: str, price: float,
                 stock: int, supplier: Supplier):
        # validation: the Product protects its own rules
        if price <= 0:
            raise ValueError("Price must be greater than zero.")
        if stock < 0:
            raise ValueError("Stock quantity cannot be negative.")
        self.__product_id: str = product_id
        # ... the rest of __init__ stays the same

    def update_stock(self, quantity: int) -> None:
        if quantity < 0:
            raise ValueError("Stock quantity cannot be negative.")
        self.__stock = quantity
