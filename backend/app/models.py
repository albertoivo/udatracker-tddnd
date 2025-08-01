from dataclasses import dataclass
from typing import Optional
from datetime import datetime


@dataclass
class Order:
    """
    Order model representing an order in the system.

    Attributes:
        order_id (str): Unique identifier for the order
        item_name (str): Name of the item being ordered
        quantity (int): Quantity of items ordered
        customer_id (str): Unique identifier for the customer
        status (str): Current status of the order (e.g., 'pending', 'shipped', 'delivered')
        created_at (datetime): Timestamp when the order was created
        updated_at (datetime): Timestamp when the order was last updated
    """

    order_id: str
    item_name: str
    quantity: int
    customer_id: str
    status: str = "pending"
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def __post_init__(self):
        """Initialize timestamps if not provided."""
        if self.created_at is None:
            self.created_at = datetime.now()
        if self.updated_at is None:
            self.updated_at = datetime.now()

    def update_status(self, new_status: str) -> None:
        """
        Update the order status and timestamp.

        Args:
            new_status (str): The new status for the order
        """
        self.status = new_status
        self.updated_at = datetime.now()

    def to_dict(self) -> dict:
        """
        Convert the order to a dictionary representation.

        Returns:
            dict: Dictionary representation of the order
        """
        return {
            "order_id": self.order_id,
            "item_name": self.item_name,
            "quantity": self.quantity,
            "customer_id": self.customer_id,
            "status": self.status,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Order":
        """
        Create an Order instance from a dictionary.

        Args:
            data (dict): Dictionary containing order data

        Returns:
            Order: New Order instance
        """
        # Parse datetime strings if present
        created_at = None
        updated_at = None

        if "created_at" in data and data["created_at"]:
            created_at = datetime.fromisoformat(data["created_at"])
        if "updated_at" in data and data["updated_at"]:
            updated_at = datetime.fromisoformat(data["updated_at"])

        return cls(
            order_id=data["order_id"],
            item_name=data["item_name"],
            quantity=data["quantity"],
            customer_id=data["customer_id"],
            status=data.get("status", "pending"),
            created_at=created_at,
            updated_at=updated_at,
        )
