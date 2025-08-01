from typing import Optional, Dict, Any, List
from app.models import Order
from app.in_memory_storage import InMemoryStorage


class OrderTracker:
    """
    Core business logic for order tracking operations.
    """

    def __init__(self, storage: Optional[InMemoryStorage] = None):
        """
        Initialize the OrderTracker with a storage backend.

        Args:
            storage: Storage backend for persisting orders. If None, creates a new InMemoryStorage.
        """
        self.storage = storage if storage is not None else InMemoryStorage()

    def create_order(
        self, order_id: str, item_name: str, quantity: int, customer_id: str
    ) -> Dict[str, Any]:
        """
        Create a new order with the provided details.

        Args:
            order_id (str): Unique identifier for the order
            item_name (str): Name of the item being ordered
            quantity (int): Quantity of items ordered
            customer_id (str): Unique identifier for the customer

        Returns:
            Dict[str, Any]: Dictionary representation of the created order

        Raises:
            ValueError: If order_id already exists or if any required field is invalid
        """
        # Validate input parameters
        if not order_id or not isinstance(order_id, str):
            raise ValueError("order_id is mandatory")

        if not item_name or not isinstance(item_name, str):
            raise ValueError("item_name is mandatory")

        if not isinstance(quantity, int) or quantity <= 0:
            raise ValueError("quantity is mandatory and must be bigger than 0")

        if not customer_id or not isinstance(customer_id, str):
            raise ValueError("customer_id is mandatory")

        # Check if order with this ID already exists
        if self.storage.get_order(order_id) is not None:
            raise ValueError(f"Order with ID '{order_id}' already exists")

        # Create the order
        order = Order(
            order_id=order_id,
            item_name=item_name,
            quantity=quantity,
            customer_id=customer_id,
            status="pending",
        )

        # Store the order
        self.storage.save_order(order)

        # Return the order as a dictionary
        return order.to_dict()

    def get_order(self, order_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve an order by its ID.

        Args:
            order_id (str): Unique identifier for the order

        Returns:
            Optional[Dict[str, Any]]: Dictionary representation of the order if found, None otherwise

        Raises:
            ValueError: If order_id is invalid
        """
        # Validate input parameter
        if not order_id or not isinstance(order_id, str):
            raise ValueError("order_id is mandatory")

        # Retrieve the order from storage
        order = self.storage.get_order(order_id)

        # Return as dictionary if found, None otherwise
        return order.to_dict() if order else None

    def update_order_status(
        self, order_id: str, new_status: str
    ) -> Optional[Dict[str, Any]]:
        """
        Update the status of an existing order.

        Args:
            order_id (str): Unique identifier for the order
            new_status (str): New status to set for the order

        Returns:
            Optional[Dict[str, Any]]: Dictionary representation of the updated order if found, None if order doesn't exist

        Raises:
            ValueError: If order_id or new_status is invalid
        """
        # Validate input parameters
        if not order_id or not isinstance(order_id, str):
            raise ValueError("order_id is mandatory")

        if not new_status or not isinstance(new_status, str):
            raise ValueError("new_status is mandatory")

        # Retrieve the order from storage
        order = self.storage.get_order(order_id)

        # Return None if order doesn't exist
        if order is None:
            return None

        # Update the order status using the Order's method
        order.update_status(new_status)

        # Save the updated order back to storage
        self.storage.save_order(order)

        # Return the updated order as a dictionary
        return order.to_dict()

    def get_all_orders(self) -> List[Dict[str, Any]]:
        """
        Retrieve all orders from storage.

        Returns:
            List[Dict[str, Any]]: List of dictionary representations of all orders
        """
        # Retrieve all orders from storage
        orders = self.storage.get_all_orders()

        # Convert all orders to dictionaries
        return [order.to_dict() for order in orders]

    def get_orders_by_status(self, status: str) -> List[Dict[str, Any]]:
        """
        Retrieve all orders with a specific status.

        Args:
            status (str): Status to filter orders by

        Returns:
            List[Dict[str, Any]]: List of dictionary representations of orders with the specified status

        Raises:
            ValueError: If status is invalid
        """
        # Validate input parameter
        if not status or not isinstance(status, str):
            raise ValueError("status is mandatory")

        # Retrieve orders with the specified status from storage
        orders = self.storage.get_orders_by_status(status)

        # Convert all orders to dictionaries
        return [order.to_dict() for order in orders]

    def get_orders_by_customer(self, customer_id: str) -> List[Dict[str, Any]]:
        """
        Retrieve all orders for a specific customer.

        Args:
            customer_id (str): Customer ID to filter orders by

        Returns:
            List[Dict[str, Any]]: List of dictionary representations of orders for the specified customer

        Raises:
            ValueError: If customer_id is invalid
        """
        # Validate input parameter
        if not customer_id or not isinstance(customer_id, str):
            raise ValueError("customer_id is mandatory")

        # Retrieve orders for the specified customer from storage
        orders = self.storage.get_orders_by_customer(customer_id)

        # Convert all orders to dictionaries
        return [order.to_dict() for order in orders]
