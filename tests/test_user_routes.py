import pytest

from fastapi.testclient import TestClient
from pydantic import ValidationError
from datetime import datetime
from uuid import uuid4
from unittest.mock import patch

from src.main import app
from src.users.schemas import User
from src.orders.schemas import Order


client = TestClient(app)


@pytest.mark.asyncio
@patch("src.users.router.get_users_demo_db")
async def test_get_users(mock_get_users_demo_db):
    mock_get_users_demo_db.return_value = [
        User(user_id=uuid4(), name="John Doe", email="john@example.com")
    ]
    response = client.get("/v1/users")
    assert response.status_code == 200
    response_json = response.json()
    assert len(response_json) == 1
    assert response_json[0]["name"] == "John Doe"


@pytest.mark.asyncio
@patch("src.users.router.create_users_demo_db")
async def test_create_users(mock_create_users_demo_db):
    mock_create_users_demo_db.return_value = [
        User(user_id=uuid4(), name="John Doe", email="john@example.com")
    ]
    users = [{"name": "John Doe", "email": "john@example.com"}]
    response = client.post("/v1/users", json=users)
    assert response.status_code == 201
    response_json = response.json()
    assert len(response_json) == 1
    assert response_json[0]["name"] == "John Doe"


@pytest.mark.asyncio
@patch("src.users.router.get_user_by_id_demo_db")
async def test_get_user_by_id(mock_get_user_by_id_demo_db):
    user_id = uuid4()
    mock_get_user_by_id_demo_db.return_value = User(
        user_id=user_id, name="John Doe", email="john@example.com"
    )
    response = client.get(f"/v1/users/{user_id}")
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["name"] == "John Doe"


@pytest.mark.asyncio
@patch("src.users.router.delete_user_by_id_demo_db")
async def test_delete_user_by_id(mock_delete_user_by_id_demo_db):
    user_id = uuid4()
    mock_delete_user_by_id_demo_db.return_value = None
    response = client.delete(f"/v1/users/{user_id}")
    assert response.status_code == 204


@pytest.mark.asyncio
@patch("src.users.router.get_orders_by_user_id_demo_db")
async def test_get_user_orders(mock_get_orders_by_user_id_demo_db):
    user_id = uuid4()
    mock_get_orders_by_user_id_demo_db.return_value = [
        Order(order_id=uuid4(), date=datetime.now(), total=811.19, user_id=user_id)
    ]
    response = client.get(f"/v1/users/{user_id}/orders")
    assert response.status_code == 200
    response_json = response.json()
    assert len(response_json) == 1
    assert response_json[0]["total"] == 811.19


@pytest.mark.asyncio
async def test_create_user_invalid_email():
    users = [{"name": "John Doe", "email": "invalid-email"}]
    with pytest.raises(ValidationError):
        response = client.post("/v1/users", json=users)
        assert response.status_code == 422
        response_json = response.json()
        assert response_json["detail"][0]["msg"] == "value is not a valid email address"


@pytest.mark.asyncio
async def test_create_user_missing_name():
    users = [{"email": "john@example.com"}]
    with pytest.raises(AssertionError):
        response = client.post("/v1/users", json=users)
        assert response.status_code == 422
        response_json = response.json()
        assert response_json["detail"][0]["msg"] == "field required"


@pytest.mark.asyncio
async def test_get_user_invalid_id():
    invalid_user_id = "invalid-uuid"
    with pytest.raises(AssertionError):
        response = client.get(f"/v1/users/{invalid_user_id}")
        assert response.status_code == 422
        response_json = response.json()
        assert response_json["detail"][0]["msg"] == "value is not a valid uuid"


@pytest.mark.asyncio
async def test_delete_user_invalid_id():
    invalid_user_id = "invalid-uuid"
    with pytest.raises(AssertionError):
        response = client.delete(f"/v1/users/{invalid_user_id}")
        assert response.status_code == 422
        response_json = response.json()
        assert response_json["detail"][0]["msg"] == "value is not a valid uuid"


@pytest.mark.asyncio
async def test_get_user_orders_invalid_user_id():
    invalid_user_id = "invalid-uuid"
    with pytest.raises(AssertionError):
        response = client.get(f"/v1/users/{invalid_user_id}/orders")
        assert response.status_code == 422
        response_json = response.json()
        assert response_json["detail"][0]["msg"] == "value is not a valid uuid"
