import pytest
from fastapi.testclient import TestClient
from datetime import datetime
from unittest.mock import patch
from src.main import app
from src.orders.schemas import Order
from uuid import uuid4

client = TestClient(app)


@pytest.mark.asyncio
@patch("src.orders.router.get_orders_demo_db")
async def test_get_orders(mock_get_orders_demo_db):
    mock_get_orders_demo_db.return_value = [
        Order(user=uuid4(), date=datetime.now(), total=811.19)
    ]
    response = client.get("/v1/orders")
    assert response.status_code == 200
    response_json = response.json()
    assert len(response_json) == 1
    assert response_json[0]["total"] == 811.19


@pytest.mark.asyncio
@patch("src.orders.router.create_orders_demo_db")
async def test_create_orders(mock_create_orders_demo_db):
    mock_create_orders_demo_db.return_value = [
        Order(user=uuid4(), date=datetime.now(), total=0.47)
    ]
    order_date = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

    orders = [
        {
            "date": order_date,
            "user": "be7c9d38-49f6-4970-b636-6ffa90bba41b",
            "total": 0.47,
        }
    ]
    response = client.post("/v1/orders", json=orders)
    assert response.status_code == 201
    response_json = response.json()
    assert len(response_json) == 1
    assert response_json[0]["total"] == 0.47


@pytest.mark.asyncio
@patch("src.orders.router.get_order_by_id_demo_db")
async def test_get_order_by_id(mock_get_order_by_id_demo_db):
    order_id = uuid4()
    mock_get_order_by_id_demo_db.return_value = Order(
        id=order_id, date=datetime.now(), user=uuid4(), total=811.19
    )
    response = client.get(f"/v1/orders/{order_id}")
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["total"] == 811.19


@pytest.mark.asyncio
@patch("src.orders.router.delete_order_by_id_demo_db")
async def test_delete_order_by_id(mock_delete_order_by_id_demo_db):
    user_id = uuid4()
    mock_delete_order_by_id_demo_db.return_value = None
    response = client.delete(f"/v1/orders/{user_id}")
    assert response.status_code == 204
