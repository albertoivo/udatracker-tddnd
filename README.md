# Order Tracker API

A simple and efficient order tracking system built with Flask, providing RESTful APIs for managing order lifecycle from creation to completion.

## 🎯 Motivation

This project was created to demonstrate a complete order tracking system with the following objectives:

- **Simplicity**: Easy to understand and maintain codebase
- **Scalability**: Clean architecture with separation of concerns
- **Testing**: Comprehensive unit and integration test coverage
- **Deployment**: Ready-to-use Docker containerization
- **Documentation**: Clear API documentation and usage examples

The system allows businesses to track orders through their entire lifecycle, from initial creation to final delivery, with real-time status updates and customer-specific filtering capabilities.

## 🧩 Challenges & Design Philosophy

This project was developed as part of the **Udacity TDD (Test-Driven Development) course**, where the primary focus was on creating a comprehensive testing strategy rather than complex business logic.

### Design Decisions:
- **Minimalist Approach**: The `app` and `order_tracker` components were intentionally kept as simple as possible
- **Functionality Over Complexity**: Simple logic but fully functional system
- **Test-First Mentality**: Every feature was developed following TDD principles
- **Maximum Test Coverage**: Extensive unit and integration tests covering all possible scenarios

### Learning Focus:
- **Test-Driven Development**: Writing tests before implementation
- **Testing Strategies**: Unit tests, integration tests, and API testing
- **Code Quality**: Maintaining high standards through automated testing
- **Refactoring Confidence**: Safe code changes backed by comprehensive test suites

The result is a deliberately simple yet robust system that demonstrates how powerful TDD can be in creating reliable, maintainable software.

## ✏️ Architecture

The project follows a layered architecture pattern:

```
├── app/
│   ├── models.py           # Data models (Order)
│   ├── in_memory_storage.py # Storage layer
│   ├── order_tracker.py    # Business logic layer
│   └── app.py             # Flask API layer
├── tests/
│   ├── test_order_tracker.py # Unit tests
│   └── test_api.py          # Integration tests
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```

## 🚀 Quick Start

### Prerequisites

- **Docker & Docker Compose** (Recommended)
- **Python 3.11+** (For local development)

### 🐳 Docker Setup (Recommended)

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd udatracker/backend
   ```

2. **Start the application:**
   ```bash
   docker-compose up --build
   ```

3. **Access the API:**
   - API Base URL: `http://localhost:5000`

4. **Stop the application:**
   ```bash
   docker-compose down
   ```

### 💻 Local Development Setup

1. **Clone and navigate:**
   ```bash
   git clone <repository-url>
   cd udatracker/backend
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application:**
   ```bash
   export FLASK_APP=app/app.py
   export FLASK_ENV=development
   export FLASK_DEBUG=true
   flask run 
   ```

5. **Access the API:**
   - API Base URL: `http://localhost:5000`

## 📋 API Endpoints

### Base URL: `http://localhost:5000/api`

### 🔍 Overview
- **GET** `/` - API documentation and available endpoints

### 📦 Order Management

#### Create Order
- **POST** `/api/create`
- **Description**: Create a new order
- **Request Body**:
  ```json
  {
    "order_id": "ORDER001",
    "item_name": "Laptop",
    "quantity": 1,
    "customer_id": "CUST001"
  }
  ```
- **Response**: `201 Created`
  ```json
  {
    "order_id": "ORDER001",
    "item_name": "Laptop",
    "quantity": 1,
    "customer_id": "CUST001",
    "status": "pending",
    "created_at": "2025-01-15T10:00:00Z",
    "updated_at": "2025-01-15T10:00:00Z"
  }
  ```

#### Get Order
- **GET** `/api/get/<order_id>`
- **Description**: Retrieve a specific order by ID
- **Response**: `200 OK` | `404 Not Found`

#### Update Order Status
- **PUT** `/api/update/<order_id>`
- **Description**: Update order status
- **Request Body**:
  ```json
  {
    "status": "shipped"
  }
  ```
- **Response**: `200 OK` | `404 Not Found`

#### List All Orders
- **GET** `/api/orders`
- **Description**: Get all orders
- **Response**: `200 OK`
  ```json
  {
    "orders": [...],
    "count": 10
  }
  ```

#### Filter Orders by Customer
- **GET** `/api/orders?customer_id=<customer_id>`
- **Description**: Get orders for a specific customer
- **Response**: `200 OK`
  ```json
  {
    "orders": [...],
    "count": 3,
    "customer_id": "CUST001"
  }
  ```

#### Filter Orders by Status
- **GET** `/api/orders/status/<status>`
- **Description**: Get orders with a specific status
- **Response**: `200 OK`
  ```json
  {
    "orders": [...],
    "count": 5,
    "status": "pending"
  }
  ```
## 🧪 Testing

### Run All Tests
```bash
# Using pytest
python -m pytest

# Verbose output
python -m pytest -v
```

### Run Specific Test Types
```bash
# Unit tests only
python -m pytest tests/test_order_tracker.py

# Integration tests only
python -m pytest tests/test_api.py

# Specific test
python -m pytest tests/test_api.py::TestAPIIntegration::test_create_order_success
```

## 🛠️ Development

### Code Quality
```bash
# Linting with flake8
flake8 app/ tests/

# Code formatting (if using black)
black app/ tests/
```

### Project Structure
```
backend/
├── app/
│   ├── __init__.py
│   ├── models.py           # Order data model
│   ├── in_memory_storage.py # Storage operations
│   ├── order_tracker.py    # Business logic
│   └── app.py             # Flask application
├── tests/
│   ├── conftest.py        # Test configuration
│   ├── test_order_tracker.py # Unit tests
│   └── test_api.py        # Integration tests
├── Dockerfile             # Container definition
├── docker-compose.yml     # Multi-service setup
├── requirements.txt       # Python dependencies
├── pytest.ini           # Test configuration
└── .flake8              # Linting configuration
```

## 🚢 Deployment

### Docker Production
```bash
# Build production image
docker build -t order-tracker-api .

# Run container
docker run -p 5000:5000 order-tracker-api
```

### Environment Variables
- `FLASK_ENV`: `development` | `production`
- `FLASK_DEBUG`: `1` | `0`
- `FLASK_APP`: `app/app.py`

---

**Built with ❤️ by AlbertoIvo using Flask, Docker, and Python**
