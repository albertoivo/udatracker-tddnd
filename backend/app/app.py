from flask import Flask, jsonify, request, Blueprint, abort
from app.order_tracker import OrderTracker
from app.in_memory_storage import InMemoryStorage

app = Flask(__name__)

# Initialize the order tracker with in memory storage
storage = InMemoryStorage()
order_tracker = OrderTracker(storage=storage)

# Create API blueprint with /api prefix
api = Blueprint("api", __name__, url_prefix="/api")


# Error handlers
@app.errorhandler(400)
def bad_request(error):
    return jsonify({"error": "Bad request"}), 400


@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500


@app.route("/")
def index():
    return jsonify(
        {
            "message": "Welcome to the Order Tracker API!",
            "endpoints": {
                "create_order": "POST /api/create",
                "get_order": "GET /api/get/<order_id>",
                "update_order_status": "PUT /api/update/<order_id>",
                "get_all_orders": "GET /api/orders",
                "get_orders_by_customer": "GET /api/orders?customer_id=<customer_id>",
                "get_orders_by_status": "GET /api/orders/status/<status>",
            },
        }
    )


@api.route("/create", methods=["POST"])
def create_order():
    """Create a new order."""
    data = request.get_json()

    if not data:
        abort(400)

    # Validate required fields
    required_fields = ["order_id", "item_name", "quantity", "customer_id"]
    for field in required_fields:
        if field not in data:
            abort(400)

    try:
        # Create the order
        order = order_tracker.create_order(
            order_id=data["order_id"],
            item_name=data["item_name"],
            quantity=data["quantity"],
            customer_id=data["customer_id"],
        )
        return jsonify(order), 201
    except ValueError:
        abort(400)


@api.route("/get/<order_id>", methods=["GET"])
def get_order(order_id):
    """Get an order by ID."""
    try:
        order = order_tracker.get_order(order_id)
        if order is None:
            abort(404)
        return jsonify(order), 200
    except ValueError:
        abort(400)


@api.route("/update/<order_id>", methods=["PUT"])
def update_order_status(order_id):
    """Update order status."""
    data = request.get_json()

    if not data or "status" not in data:
        abort(400)

    try:
        order = order_tracker.update_order_status(order_id, data["status"])
        if order is None:
            abort(404)
        return jsonify(order), 200
    except ValueError:
        abort(400)


@api.route("/orders", methods=["GET"])
def get_all_orders():
    """Get all orders, optionally filtered by customer_id."""
    # Check if customer_id filter is provided
    customer_id = request.args.get("customer_id")

    if customer_id:
        try:
            # Filter by customer_id
            orders = order_tracker.get_orders_by_customer(customer_id)
            return (
                jsonify(
                    {"orders": orders, "count": len(orders), "customer_id": customer_id}
                ),
                200,
            )
        except ValueError:
            abort(400)
    else:
        # Return all orders
        orders = order_tracker.get_all_orders()
        return jsonify({"orders": orders, "count": len(orders)}), 200


@api.route("/orders/status/<status>", methods=["GET"])
def get_orders_by_status(status):
    """Get orders by status."""
    try:
        orders = order_tracker.get_orders_by_status(status)
        return jsonify({"orders": orders, "count": len(orders), "status": status}), 200
    except ValueError:
        abort(400)


# Register the API blueprint
app.register_blueprint(api)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
