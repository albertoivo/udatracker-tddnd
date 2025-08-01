from typing import Optional, List
from app.models import Order


class InMemoryStorage:
    """A class to handle in-memory storage operations for orders."""

    def __init__(self):
        self.storage = {}
        self.orders = {}  # Specific storage for orders

    def get(self, key):
        return self.storage.get(key)

    def set(self, key, value):
        self.storage[key] = value

    def delete(self, key):
        if key in self.storage:
            del self.storage[key]

    def clear(self):
        self.storage.clear()
        self.orders.clear()

    # Order-specific methods
    def save_order(self, order: Order) -> None:
        """Save an order to storage."""
        self.orders[order.order_id] = order

    def get_order(self, order_id: str) -> Optional[Order]:
        """Retrieve an order by ID."""
        return self.orders.get(order_id)

    def get_all_orders(self) -> List[Order]:
        """Retrieve all orders."""
        return list(self.orders.values())

    def delete_order(self, order_id: str) -> bool:
        """Delete an order by ID. Returns True if deleted, False if not found."""
        if order_id in self.orders:
            del self.orders[order_id]
            return True
        return False

    def get_orders_by_status(self, status: str) -> List[Order]:
        """Retrieve all orders with a specific status."""
        return [order for order in self.orders.values() if order.status == status]

    def get_orders_by_customer(self, customer_id: str) -> List[Order]:
        """Retrieve all orders for a specific customer."""
        return [
            order for order in self.orders.values() if order.customer_id == customer_id
        ]
