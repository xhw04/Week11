from product import Product
from physicalproduct import PhysicalProduct
from digitalproduct import DigitalProduct
from supplier import Supplier


class ProductFactory:
    # extra = weight (kg) for physical, download size (MB) for digital
    @staticmethod
    def create(product_type: str, product_id: str, name: str, price: float,
               stock_quantity: int, supplier: Supplier,
               extra: float | None = None) -> Product:
        if product_type == "physical":
            weight = 1.0 if extra is None else extra
            return PhysicalProduct(product_id, name, price,
                                   stock_quantity, supplier, weight)
        elif product_type == "digital":
            size = 100.0 if extra is None else extra
            return DigitalProduct(product_id, name, price,
                                  stock_quantity, supplier, size)
        else:
            raise ValueError(f"Unknown product type: {product_type}")
