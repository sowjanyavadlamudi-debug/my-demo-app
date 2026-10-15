
import yaml

def load_config():
    with open("../../shared/config.yaml", "r") as f:
        return yaml.safe_load(f)

config = load_config()
DB_POOL_SIZE = config["database"]["connection_pool_size"]

class InventoryManager:

    def __init__(self):
        self.inventory = {
            "PROD-001": {"name": "Laptop", "quantity": 50, "price": 999.99},
            "PROD-002": {"name": "Mouse", "quantity": 200, "price": 29.99},
            "PROD-003": {"name": "Keyboard", "quantity": 150, "price": 79.99},
        }

    def check_stock(self, product_id):
        product = self.inventory.get(product_id)
        if not product:
            return {"available": False, "error": "Product not found"}
        return {"available": product["quantity"] > 0, "quantity": product["quantity"]}

    def reserve_stock(self, product_id, quantity):
        product = self.inventory.get(product_id)
        if not product:
            raise ValueError(f"Product {product_id} not found")

        if product["quantity"] < quantity:
            raise ValueError(f"Insufficient stock. Available: {product['quantity']}")

        product["quantity"] -= quantity
        return {"product_id": product_id, "reserved": quantity, "remaining": product["quantity"]}

