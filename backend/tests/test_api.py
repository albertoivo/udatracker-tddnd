import unittest
import json
from app.app import app


class TestAPIIntegration(unittest.TestCase):
    """Integration tests for the Order Tracker API."""

    def setUp(self):
        """Set up test client and test data."""
        self.app = app.test_client()
        self.app.testing = True
        # Clear storage before each test to avoid conflicts
        from app.app import storage

        storage.clear()

    def test_create_order_success(self):
        """Test POST /api/create with valid data returns 201 Created."""
        # Prepare test data
        order_data = {
            "order_id": "ORDER001",
            "item_name": "Test Item",
            "quantity": 5,
            "customer_id": "CUST001",
        }

        # Send POST request
        response = self.app.post(
            "/api/create", data=json.dumps(order_data), content_type="application/json"
        )

        # Assert response status
        self.assertEqual(response.status_code, 201)

        # Parse response data
        response_data = json.loads(response.data)

        # Assert response contains expected fields
        self.assertIn("order_id", response_data)
        self.assertIn("item_name", response_data)
        self.assertIn("quantity", response_data)
        self.assertIn("customer_id", response_data)
        self.assertIn("status", response_data)
        self.assertIn("created_at", response_data)
        self.assertIn("updated_at", response_data)

        # Assert response data matches request data
        self.assertEqual(response_data["order_id"], order_data["order_id"])
        self.assertEqual(response_data["item_name"], order_data["item_name"])
        self.assertEqual(response_data["quantity"], order_data["quantity"])
        self.assertEqual(response_data["customer_id"], order_data["customer_id"])
        self.assertEqual(response_data["status"], "pending")

    def test_get_order_success(self):
        """Test GET /api/get/<order_id> with existing order returns 200 OK with correct data."""
        # First, create an order to fetch
        order_data = {
            "order_id": "ORDER002",
            "item_name": "Test Item 2",
            "quantity": 3,
            "customer_id": "CUST002",
        }

        # Create the order
        create_response = self.app.post(
            "/api/create", data=json.dumps(order_data), content_type="application/json"
        )
        self.assertEqual(create_response.status_code, 201)

        # Now fetch the created order
        get_response = self.app.get(f'/api/get/{order_data["order_id"]}')

        # Assert response status
        self.assertEqual(get_response.status_code, 200)

        # Parse response data
        response_data = json.loads(get_response.data)

        # Assert response contains expected fields
        self.assertIn("order_id", response_data)
        self.assertIn("item_name", response_data)
        self.assertIn("quantity", response_data)
        self.assertIn("customer_id", response_data)
        self.assertIn("status", response_data)
        self.assertIn("created_at", response_data)
        self.assertIn("updated_at", response_data)

        # Assert response data matches the created order
        self.assertEqual(response_data["order_id"], order_data["order_id"])
        self.assertEqual(response_data["item_name"], order_data["item_name"])
        self.assertEqual(response_data["quantity"], order_data["quantity"])
        self.assertEqual(response_data["customer_id"], order_data["customer_id"])
        self.assertEqual(response_data["status"], "pending")

        # Assert timestamps are present and valid
        self.assertIsNotNone(response_data["created_at"])
        self.assertIsNotNone(response_data["updated_at"])

    def test_get_order_not_found(self):
        """Test GET /api/get/<order_id> with non-existing order returns 404 Not Found."""
        # Try to fetch a non-existing order
        response = self.app.get("/api/get/NONEXISTENT_ORDER")

        # Assert response status
        self.assertEqual(response.status_code, 404)

        # Parse response data
        response_data = json.loads(response.data)

        # Assert error message
        self.assertIn("error", response_data)
        self.assertEqual(response_data["error"], "Not found")

    def test_update_order_status_success(self):
        """Test PUT /api/update/<order_id> with new status returns 200 OK with updated data."""
        # First, create an order to update
        order_data = {
            "order_id": "ORDER003",
            "item_name": "Test Item 3",
            "quantity": 2,
            "customer_id": "CUST003",
        }

        # Create the order
        create_response = self.app.post(
            "/api/create", data=json.dumps(order_data), content_type="application/json"
        )
        self.assertEqual(create_response.status_code, 201)

        # Now update the order status
        update_data = {"status": "shipped"}

        update_response = self.app.put(
            f'/api/update/{order_data["order_id"]}',
            data=json.dumps(update_data),
            content_type="application/json",
        )

        # Assert response status
        self.assertEqual(update_response.status_code, 200)

        # Parse response data
        response_data = json.loads(update_response.data)

        # Assert response contains expected fields
        self.assertIn("order_id", response_data)
        self.assertIn("item_name", response_data)
        self.assertIn("quantity", response_data)
        self.assertIn("customer_id", response_data)
        self.assertIn("status", response_data)
        self.assertIn("created_at", response_data)
        self.assertIn("updated_at", response_data)

        # Assert original data is preserved
        self.assertEqual(response_data["order_id"], order_data["order_id"])
        self.assertEqual(response_data["item_name"], order_data["item_name"])
        self.assertEqual(response_data["quantity"], order_data["quantity"])
        self.assertEqual(response_data["customer_id"], order_data["customer_id"])

        # Assert status was updated
        self.assertEqual(response_data["status"], "shipped")

        # Assert timestamps are present
        self.assertIsNotNone(response_data["created_at"])
        self.assertIsNotNone(response_data["updated_at"])

    def test_update_order_status_not_found(self):
        """Test PUT /api/update/<order_id> with non-existing order returns 404 Not Found."""
        # Try to update a non-existing order
        update_data = {"status": "shipped"}

        response = self.app.put(
            "/api/update/NONEXISTENT_ORDER",
            data=json.dumps(update_data),
            content_type="application/json",
        )

        # Assert response status
        self.assertEqual(response.status_code, 404)

        # Parse response data
        response_data = json.loads(response.data)

        # Assert error message
        self.assertIn("error", response_data)
        self.assertEqual(response_data["error"], "Not found")

    def test_get_all_orders_success(self):
        """Test GET /api/orders returns 200 OK with list of previously created orders."""
        # First, create some orders to retrieve
        orders_to_create = [
            {
                "order_id": "ORDER004",
                "item_name": "Test Item 4",
                "quantity": 1,
                "customer_id": "CUST004",
            },
            {
                "order_id": "ORDER005",
                "item_name": "Test Item 5",
                "quantity": 3,
                "customer_id": "CUST005",
            },
            {
                "order_id": "ORDER006",
                "item_name": "Test Item 6",
                "quantity": 2,
                "customer_id": "CUST004",  # Same customer as first order
            },
        ]

        # Create all orders
        created_orders = []
        for order_data in orders_to_create:
            create_response = self.app.post(
                "/api/create",
                data=json.dumps(order_data),
                content_type="application/json",
            )
            self.assertEqual(create_response.status_code, 201)
            created_orders.append(json.loads(create_response.data))

        # Now fetch all orders
        get_response = self.app.get("/api/orders")

        # Assert response status
        self.assertEqual(get_response.status_code, 200)

        # Parse response data
        response_data = json.loads(get_response.data)

        # Assert response structure
        self.assertIn("orders", response_data)
        self.assertIn("count", response_data)
        self.assertIsInstance(response_data["orders"], list)
        self.assertIsInstance(response_data["count"], int)

        # Assert we got the correct number of orders
        self.assertEqual(response_data["count"], 3)
        self.assertEqual(len(response_data["orders"]), 3)

        # Assert each created order is in the response
        returned_order_ids = [order["order_id"] for order in response_data["orders"]]
        for created_order in created_orders:
            self.assertIn(created_order["order_id"], returned_order_ids)

        # Assert all orders have required fields
        for order in response_data["orders"]:
            self.assertIn("order_id", order)
            self.assertIn("item_name", order)
            self.assertIn("quantity", order)
            self.assertIn("customer_id", order)
            self.assertIn("status", order)
            self.assertIn("created_at", order)
            self.assertIn("updated_at", order)

    def test_get_orders_by_customer_success(self):
        """Test GET /api/orders?customer_id=<customer_id> returns 200 OK with filtered orders."""
        # First, create orders for different customers
        orders_to_create = [
            {
                "order_id": "ORDER007",
                "item_name": "Customer A Item 1",
                "quantity": 1,
                "customer_id": "CUST_A",
            },
            {
                "order_id": "ORDER008",
                "item_name": "Customer A Item 2",
                "quantity": 2,
                "customer_id": "CUST_A",
            },
            {
                "order_id": "ORDER009",
                "item_name": "Customer B Item 1",
                "quantity": 3,
                "customer_id": "CUST_B",
            },
        ]

        # Create all orders
        for order_data in orders_to_create:
            create_response = self.app.post(
                "/api/create",
                data=json.dumps(order_data),
                content_type="application/json",
            )
            self.assertEqual(create_response.status_code, 201)

        # Now fetch orders for CUST_A only
        get_response = self.app.get("/api/orders?customer_id=CUST_A")

        # Assert response status
        self.assertEqual(get_response.status_code, 200)

        # Parse response data
        response_data = json.loads(get_response.data)

        # Assert response structure
        self.assertIn("orders", response_data)
        self.assertIn("count", response_data)
        self.assertIn("customer_id", response_data)
        self.assertEqual(response_data["customer_id"], "CUST_A")

        # Assert we got only CUST_A orders
        self.assertEqual(response_data["count"], 2)
        self.assertEqual(len(response_data["orders"]), 2)

        # Assert all returned orders belong to CUST_A
        for order in response_data["orders"]:
            self.assertEqual(order["customer_id"], "CUST_A")
            self.assertIn(order["order_id"], ["ORDER007", "ORDER008"])

        # Assert all orders have required fields
        for order in response_data["orders"]:
            self.assertIn("order_id", order)
            self.assertIn("item_name", order)
            self.assertIn("quantity", order)
            self.assertIn("customer_id", order)
            self.assertIn("status", order)
            self.assertIn("created_at", order)
            self.assertIn("updated_at", order)


if __name__ == "__main__":
    unittest.main()
