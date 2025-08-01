import unittest
from unittest.mock import Mock, patch
from datetime import datetime

from app.order_tracker import OrderTracker
from app.models import Order
from app.in_memory_storage import InMemoryStorage


class TestOrderTrackerCreateOrder(unittest.TestCase):
    """Unit tests for the OrderTracker.create_order method."""

    def setUp(self):
        """Set up test fixtures before each test method."""
        self.mock_storage = Mock(spec=InMemoryStorage)
        self.order_tracker = OrderTracker(storage=self.mock_storage)

        self.valid_order_data = {
            "order_id": "ORD001",
            "item_name": "Laptop",
            "quantity": 2,
            "customer_id": "CUST001",
        }

    def test_create_order_success(self):
        """Test successful order creation with valid data."""
        self.mock_storage.get_order.return_value = None
        self.order_tracker.create_order(**self.valid_order_data)
        self.mock_storage.get_order.assert_called_once_with("ORD001")
        self.mock_storage.save_order.assert_called_once()

        saved_order = self.mock_storage.save_order.call_args[0][0]
        self.assertIsInstance(saved_order, Order)
        self.assertEqual(saved_order.order_id, "ORD001")

    def test_create_order_duplicate_id(self):
        """Test that creating an order with duplicate ID raises ValueError."""
        existing_order = Order("ORD001", "Item", 1, "CUST001")
        self.mock_storage.get_order.return_value = existing_order

        with self.assertRaises(ValueError) as context:
            self.order_tracker.create_order(**self.valid_order_data)

        self.assertIn("Order with ID 'ORD001' already exists", str(context.exception))

        self.mock_storage.save_order.assert_not_called()

    def test_create_order_invalid_order_id(self):
        """Test validation of order_id parameter."""
        test_cases = [
            ("", "order_id is mandatory"),
            (None, "order_id is mandatory"),
            (123, "order_id is mandatory"),
            ([], "order_id is mandatory"),
        ]

        for invalid_order_id, expected_message in test_cases:
            with self.subTest(order_id=invalid_order_id):
                with self.assertRaises(ValueError) as context:
                    self.order_tracker.create_order(
                        order_id=invalid_order_id,
                        item_name="Laptop",
                        quantity=2,
                        customer_id="CUST001",
                    )
                self.assertEqual(str(context.exception), expected_message)

    def test_create_order_invalid_item_name(self):
        """Test validation of item_name parameter."""
        test_cases = [
            ("", "item_name is mandatory"),
            (None, "item_name is mandatory"),
            (123, "item_name is mandatory"),
            ([], "item_name is mandatory"),
        ]

        for invalid_item_name, expected_message in test_cases:
            with self.subTest(item_name=invalid_item_name):
                with self.assertRaises(ValueError) as context:
                    self.order_tracker.create_order(
                        order_id="ORD001",
                        item_name=invalid_item_name,
                        quantity=2,
                        customer_id="CUST001",
                    )
                self.assertEqual(str(context.exception), expected_message)

    def test_create_order_invalid_quantity(self):
        """Test validation of quantity parameter."""
        test_cases = [
            (0, "quantity is mandatory and must be bigger than 0"),
            (-1, "quantity is mandatory and must be bigger than 0"),
            ("2", "quantity is mandatory and must be bigger than 0"),
            (2.5, "quantity is mandatory and must be bigger than 0"),
            (None, "quantity is mandatory and must be bigger than 0"),
        ]

        for invalid_quantity, expected_message in test_cases:
            with self.subTest(quantity=invalid_quantity):
                with self.assertRaises(ValueError) as context:
                    self.order_tracker.create_order(
                        order_id="ORD001",
                        item_name="Laptop",
                        quantity=invalid_quantity,
                        customer_id="CUST001",
                    )
                self.assertEqual(str(context.exception), expected_message)

    def test_create_order_invalid_customer_id(self):
        """Test validation of customer_id parameter."""
        test_cases = [
            ("", "customer_id is mandatory"),
            (None, "customer_id is mandatory"),
            (123, "customer_id is mandatory"),
            ([], "customer_id is mandatory"),
        ]

        for invalid_customer_id, expected_message in test_cases:
            with self.subTest(customer_id=invalid_customer_id):
                with self.assertRaises(ValueError) as context:
                    self.order_tracker.create_order(
                        order_id="ORD001",
                        item_name="Laptop",
                        quantity=2,
                        customer_id=invalid_customer_id,
                    )
                self.assertEqual(str(context.exception), expected_message)

    def test_create_order_with_default_storage(self):
        """Test OrderTracker initialization with default storage."""
        tracker = OrderTracker()
        self.assertIsInstance(tracker.storage, InMemoryStorage)

    @patch("app.models.datetime")
    def test_create_order_timestamps(self, mock_datetime):
        """Test that created_at and updated_at timestamps are set correctly."""
        mock_now = datetime(2025, 7, 31, 12, 0, 0)
        mock_datetime.now.return_value = mock_now

        self.mock_storage.get_order.return_value = None
        self.order_tracker.create_order(**self.valid_order_data)

        saved_order = self.mock_storage.save_order.call_args[0][0]
        self.assertEqual(saved_order.created_at, mock_now)
        self.assertEqual(saved_order.updated_at, mock_now)


class TestOrderTrackerGetOrder(unittest.TestCase):
    """Unit tests for the OrderTracker.get_order method."""

    def setUp(self):
        """Set up test fixtures before each test method."""
        self.mock_storage = Mock(spec=InMemoryStorage)
        self.order_tracker = OrderTracker(storage=self.mock_storage)

        self.sample_order = Order(
            order_id="ORD001",
            item_name="Laptop",
            quantity=2,
            customer_id="CUST001",
            status="pending",
        )

    def test_get_order_success(self):
        """Test successful order retrieval with valid order_id."""
        self.mock_storage.get_order.return_value = self.sample_order
        result = self.order_tracker.get_order("ORD001")
        self.mock_storage.get_order.assert_called_once_with("ORD001")
        self.assertIsInstance(result, dict)
        self.assertEqual(result["order_id"], "ORD001")

    def test_get_order_not_found(self):
        """Test order retrieval when order doesn't exist."""
        self.mock_storage.get_order.return_value = None
        result = self.order_tracker.get_order("NONEXISTENT")
        self.mock_storage.get_order.assert_called_once_with("NONEXISTENT")
        self.assertIsNone(result)

    def test_get_order_invalid_order_id(self):
        """Test validation of order_id parameter."""
        test_cases = [
            ("", "order_id is mandatory"),
            (None, "order_id is mandatory"),
            (123, "order_id is mandatory"),
            ([], "order_id is mandatory"),
            ({}, "order_id is mandatory"),
            (True, "order_id is mandatory"),
        ]

        for invalid_order_id, expected_message in test_cases:
            with self.subTest(order_id=invalid_order_id):
                with self.assertRaises(ValueError) as context:
                    self.order_tracker.get_order(invalid_order_id)
                self.assertEqual(str(context.exception), expected_message)

                self.mock_storage.get_order.assert_not_called()
                self.mock_storage.reset_mock()

    def test_get_order_with_different_statuses(self):
        """Test retrieving orders with different statuses."""
        statuses = ["pending", "shipped", "delivered", "cancelled"]

        for status in statuses:
            with self.subTest(status=status):
                order = Order("ORD001", "Item", 1, "CUST001", status)
                self.mock_storage.get_order.return_value = order
                result = self.order_tracker.get_order("ORD001")
                self.assertEqual(result["status"], status)
                self.mock_storage.reset_mock()

    def test_get_order_storage_integration(self):
        """Test get_order with real InMemoryStorage (integration test)."""
        real_storage = InMemoryStorage()
        tracker = OrderTracker(storage=real_storage)
        created_order = tracker.create_order("ORD001", "Laptop", 2, "CUST001")
        retrieved_order = tracker.get_order("ORD001")
        self.assertEqual(created_order["order_id"], retrieved_order["order_id"])
        self.assertEqual(created_order["item_name"], retrieved_order["item_name"])

        non_existent = tracker.get_order("NONEXISTENT")
        self.assertIsNone(non_existent)


class TestOrderTrackerUpdateOrderStatus(unittest.TestCase):
    """Unit tests for the OrderTracker.update_order_status method."""

    def setUp(self):
        """Set up test fixtures before each test method."""
        self.mock_storage = Mock(spec=InMemoryStorage)
        self.order_tracker = OrderTracker(storage=self.mock_storage)

        self.sample_order = Order(
            order_id="ORD001",
            item_name="Laptop",
            quantity=2,
            customer_id="CUST001",
            status="pending",
        )

    def test_update_order_status_success(self):
        """Test successful order status update with valid data."""
        self.mock_storage.get_order.return_value = self.sample_order
        result = self.order_tracker.update_order_status("ORD001", "shipped")
        self.mock_storage.get_order.assert_called_once_with("ORD001")
        self.mock_storage.save_order.assert_called_once()

        saved_order = self.mock_storage.save_order.call_args[0][0]
        self.assertEqual(saved_order.status, "shipped")

        self.assertIsInstance(result, dict)
        self.assertEqual(result["order_id"], "ORD001")

    def test_update_order_status_order_not_found(self):
        """Test updating status when order doesn't exist."""
        self.mock_storage.get_order.return_value = None
        result = self.order_tracker.update_order_status("NONEXISTENT", "shipped")
        self.mock_storage.get_order.assert_called_once_with("NONEXISTENT")
        self.mock_storage.save_order.assert_not_called()

        self.assertIsNone(result)

    def test_update_order_status_invalid_order_id(self):
        """Test validation of order_id parameter."""
        test_cases = [
            ("", "order_id is mandatory"),
            (None, "order_id is mandatory"),
            (123, "order_id is mandatory"),
            ([], "order_id is mandatory"),
            ({}, "order_id is mandatory"),
            (True, "order_id is mandatory"),
        ]

        for invalid_order_id, expected_message in test_cases:
            with self.subTest(order_id=invalid_order_id):
                with self.assertRaises(ValueError) as context:
                    self.order_tracker.update_order_status(invalid_order_id, "shipped")
                self.assertEqual(str(context.exception), expected_message)
                self.mock_storage.get_order.assert_not_called()
                self.mock_storage.save_order.assert_not_called()
                self.mock_storage.reset_mock()

    def test_update_order_status_invalid_new_status(self):
        """Test validation of new_status parameter."""
        test_cases = [
            ("", "new_status is mandatory"),
            (None, "new_status is mandatory"),
            (123, "new_status is mandatory"),
            ([], "new_status is mandatory"),
            ({}, "new_status is mandatory"),
            (True, "new_status is mandatory"),
        ]

        for invalid_status, expected_message in test_cases:
            with self.subTest(new_status=invalid_status):
                with self.assertRaises(ValueError) as context:
                    self.order_tracker.update_order_status("ORD001", invalid_status)
                self.assertEqual(str(context.exception), expected_message)
                self.mock_storage.get_order.assert_not_called()
                self.mock_storage.save_order.assert_not_called()
                self.mock_storage.reset_mock()

    @patch("app.models.datetime")
    def test_update_order_status_updates_timestamp(self, mock_datetime):
        """Test that updating status also updates the updated_at timestamp."""
        original_time = datetime(2025, 7, 31, 10, 0, 0)
        updated_time = datetime(2025, 7, 31, 12, 0, 0)
        mock_datetime.now.return_value = updated_time

        self.sample_order.created_at = original_time
        self.sample_order.updated_at = original_time
        self.mock_storage.get_order.return_value = self.sample_order

        self.order_tracker.update_order_status("ORD001", "shipped")

        saved_order = self.mock_storage.save_order.call_args[0][0]
        self.assertEqual(
            saved_order.created_at, original_time
        )  # Should remain unchanged
        self.assertEqual(saved_order.updated_at, updated_time)  # Should be updated

    def test_update_order_status_storage_integration(self):
        """Test update_order_status with real InMemoryStorage (integration test)."""
        real_storage = InMemoryStorage()
        tracker = OrderTracker(storage=real_storage)

        created_order = tracker.create_order("ORD001", "Laptop", 2, "CUST001")
        self.assertEqual(created_order["status"], "pending")

        updated_order = tracker.update_order_status("ORD001", "shipped")
        self.assertEqual(updated_order["status"], "shipped")

        retrieved_order = tracker.get_order("ORD001")
        self.assertEqual(retrieved_order["status"], "shipped")

        non_existent_update = tracker.update_order_status("NONEXISTENT", "shipped")
        self.assertIsNone(non_existent_update)

    def test_update_order_status_common_statuses(self):
        """Test updating to common order statuses."""
        common_statuses = [
            "pending",
            "confirmed",
            "processing",
            "shipped",
            "delivered",
            "cancelled",
            "returned",
            "refunded",
        ]

        for status in common_statuses:
            with self.subTest(status=status):
                self.sample_order.status = "pending"
                self.mock_storage.get_order.return_value = self.sample_order
                result = self.order_tracker.update_order_status("ORD001", status)
                self.assertEqual(result["status"], status)
                self.mock_storage.reset_mock()


class TestOrderTrackerGetAllOrders(unittest.TestCase):
    """Unit tests for the OrderTracker.get_all_orders method."""

    def setUp(self):
        """Set up test fixtures before each test method."""
        self.mock_storage = Mock(spec=InMemoryStorage)
        self.order_tracker = OrderTracker(storage=self.mock_storage)

        self.sample_orders = [
            Order("ORD001", "Laptop", 2, "CUST001", "pending"),
            Order("ORD002", "Mouse", 1, "CUST002", "shipped"),
            Order("ORD003", "Keyboard", 1, "CUST001", "delivered"),
        ]

    def test_get_all_orders_success(self):
        """Test successful retrieval of all orders."""
        self.mock_storage.get_all_orders.return_value = self.sample_orders
        result = self.order_tracker.get_all_orders()
        self.mock_storage.get_all_orders.assert_called_once()

        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 3)

        self.assertEqual(result[0]["order_id"], "ORD001")
        self.assertEqual(result[1]["order_id"], "ORD002")
        self.assertEqual(result[2]["order_id"], "ORD003")

        for order_dict in result:
            self.assertIn("created_at", order_dict)
            self.assertIn("updated_at", order_dict)

    def test_get_all_orders_empty_storage(self):
        """Test get_all_orders when no orders exist."""
        self.mock_storage.get_all_orders.return_value = []
        result = self.order_tracker.get_all_orders()
        self.mock_storage.get_all_orders.assert_called_once()
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 0)

    def test_get_all_orders_single_order(self):
        """Test get_all_orders with only one order."""
        single_order = [Order("ORD001", "Laptop", 1, "CUST001", "pending")]
        self.mock_storage.get_all_orders.return_value = single_order
        result = self.order_tracker.get_all_orders()

        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["order_id"], "ORD001")
        self.assertEqual(result[0]["status"], "pending")

    def test_get_all_orders_preserves_order_sequence(self):
        """Test that get_all_orders preserves the order sequence from storage."""
        ordered_orders = [
            Order("ORD003", "Item C", 1, "CUST003", "pending"),
            Order("ORD001", "Item A", 1, "CUST001", "shipped"),
            Order("ORD002", "Item B", 1, "CUST002", "delivered"),
        ]
        self.mock_storage.get_all_orders.return_value = ordered_orders

        result = self.order_tracker.get_all_orders()

        self.assertEqual(result[0]["order_id"], "ORD003")
        self.assertEqual(result[1]["order_id"], "ORD001")
        self.assertEqual(result[2]["order_id"], "ORD002")

    def test_get_all_orders_storage_integration(self):
        """Test get_all_orders with real InMemoryStorage (integration test)."""
        real_storage = InMemoryStorage()
        tracker = OrderTracker(storage=real_storage)

        result = tracker.get_all_orders()
        self.assertEqual(len(result), 0)

        tracker.create_order("ORD001", "Laptop", 2, "CUST001")
        tracker.create_order("ORD002", "Mouse", 1, "CUST002")
        tracker.create_order("ORD003", "Keyboard", 1, "CUST001")

        all_orders = tracker.get_all_orders()

        self.assertEqual(len(all_orders), 3)
        order_ids = [order["order_id"] for order in all_orders]
        self.assertIn("ORD001", order_ids)
        self.assertIn("ORD002", order_ids)
        self.assertIn("ORD003", order_ids)


class TestOrderTrackerGetOrdersByStatus(unittest.TestCase):
    """Unit tests for the OrderTracker.get_orders_by_status method."""

    def setUp(self):
        """Set up test fixtures before each test method."""
        self.mock_storage = Mock(spec=InMemoryStorage)
        self.order_tracker = OrderTracker(storage=self.mock_storage)

        self.sample_orders = [
            Order("ORD001", "Laptop", 2, "CUST001", "pending"),
            Order("ORD002", "Mouse", 1, "CUST002", "shipped"),
            Order("ORD003", "Keyboard", 1, "CUST001", "shipped"),
            Order("ORD004", "Monitor", 1, "CUST003", "delivered"),
            Order("ORD005", "Headset", 1, "CUST002", "pending"),
        ]

    def test_get_orders_by_status_success_shipped(self):
        """Test successful retrieval of orders with 'shipped' status."""
        shipped_orders = [
            order for order in self.sample_orders if order.status == "shipped"
        ]
        self.mock_storage.get_orders_by_status.return_value = shipped_orders
        result = self.order_tracker.get_orders_by_status("shipped")
        self.mock_storage.get_orders_by_status.assert_called_once_with("shipped")
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 2)

        for order_dict in result:
            self.assertEqual(order_dict["status"], "shipped")

        order_ids = [order["order_id"] for order in result]
        self.assertIn("ORD002", order_ids)
        self.assertIn("ORD003", order_ids)

    def test_get_orders_by_status_success_pending(self):
        """Test successful retrieval of orders with 'pending' status."""
        pending_orders = [
            order for order in self.sample_orders if order.status == "pending"
        ]
        self.mock_storage.get_orders_by_status.return_value = pending_orders

        result = self.order_tracker.get_orders_by_status("pending")
        self.mock_storage.get_orders_by_status.assert_called_once_with("pending")
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 2)

        for order_dict in result:
            self.assertEqual(order_dict["status"], "pending")

        order_ids = [order["order_id"] for order in result]
        self.assertIn("ORD001", order_ids)
        self.assertIn("ORD005", order_ids)

    def test_get_orders_by_status_no_matches(self):
        """Test get_orders_by_status when no orders match the status."""
        self.mock_storage.get_orders_by_status.return_value = []
        result = self.order_tracker.get_orders_by_status("cancelled")
        self.mock_storage.get_orders_by_status.assert_called_once_with("cancelled")
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 0)

    def test_get_orders_by_status_invalid_status(self):
        """Test validation of status parameter."""
        test_cases = [
            ("", "status is mandatory"),
            (None, "status is mandatory"),
            (123, "status is mandatory"),
            ([], "status is mandatory"),
            ({}, "status is mandatory"),
            (True, "status is mandatory"),
        ]

        for invalid_status, expected_message in test_cases:
            with self.subTest(status=invalid_status):
                with self.assertRaises(ValueError) as context:
                    self.order_tracker.get_orders_by_status(invalid_status)
                self.assertEqual(str(context.exception), expected_message)
                self.mock_storage.get_orders_by_status.assert_not_called()
                self.mock_storage.reset_mock()

    def test_get_orders_by_status_common_statuses(self):
        """Test filtering by common order statuses."""
        common_statuses = [
            "pending",
            "confirmed",
            "processing",
            "shipped",
            "delivered",
            "cancelled",
            "returned",
            "refunded",
        ]

        for status in common_statuses:
            with self.subTest(status=status):
                filtered_orders = [
                    Order(f"ORD{i}", f"Item{i}", 1, f"CUST{i}", status)
                    for i in range(2)
                ]
                self.mock_storage.get_orders_by_status.return_value = filtered_orders
                result = self.order_tracker.get_orders_by_status(status)
                self.assertEqual(len(result), 2)
                for order_dict in result:
                    self.assertEqual(order_dict["status"], status)

                self.mock_storage.reset_mock()

    def test_get_orders_by_status_storage_integration(self):
        """Test get_orders_by_status with real InMemoryStorage (integration test)."""
        real_storage = InMemoryStorage()
        tracker = OrderTracker(storage=real_storage)

        tracker.create_order("ORD001", "Laptop", 2, "CUST001")
        tracker.create_order("ORD002", "Mouse", 1, "CUST002")
        tracker.create_order("ORD003", "Keyboard", 1, "CUST001")

        tracker.update_order_status("ORD001", "shipped")
        tracker.update_order_status("ORD003", "shipped")

        pending_orders = tracker.get_orders_by_status("pending")
        self.assertEqual(len(pending_orders), 1)
        self.assertEqual(pending_orders[0]["order_id"], "ORD002")

        shipped_orders = tracker.get_orders_by_status("shipped")
        self.assertEqual(len(shipped_orders), 2)
        shipped_ids = [order["order_id"] for order in shipped_orders]
        self.assertIn("ORD001", shipped_ids)
        self.assertIn("ORD003", shipped_ids)

        delivered_orders = tracker.get_orders_by_status("delivered")
        self.assertEqual(len(delivered_orders), 0)


if __name__ == "__main__":
    unittest.main()
