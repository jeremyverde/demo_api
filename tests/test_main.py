from fastapi.testclient import TestClient
import asyncio
import pytest

from src.main import app
from uuid import uuid4, UUID
from src.main import app, SETTINGS
from src.data.demo_db import user_table as ut, order_table as ot
import importlib

from pydantic import ValidationError


pytest_plugins = "pytest_asyncio"

client = TestClient(app)


@pytest.fixture(scope="module", autouse=True)
def reload_demo_db():
    import src.data.demo_db

    importlib.reload(src.data.demo_db)


@pytest.mark.asyncio
async def test_health_return_time_env():
    response = client.get("health")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_health_return_time_env():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["time"] is not None
    assert response.json()["environment"] == SETTINGS.env


@pytest.mark.asyncio
async def test_add_record():
    table = "orders"
    records = [
        {
            "date": "2025-03-07T03:56:34.028Z",
            "user_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            "total": 100.00,
        }
    ]
    response = client.post(f"/v1/add_record/{table}", json=records)
    assert response.status_code == 201
    assert response.json() is not None


@pytest.mark.asyncio
async def test_update_record_hit():
    table = "orders"
    record_id = "2a3bf8e3-ee45-4856-a5b1-04935cc50e4e"
    record = {
        "date": "2025-03-07T03:56:34.028Z",
        "user_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "total": 100.00,
    }
    response = client.put(f"/v1/update_record/{table}/{record_id}", json=record)
    assert response.status_code == 200
    assert response.json() is not None


@pytest.mark.asyncio
async def test_update_record_miss():
    table = "orders"
    record_id = "3fa85f64-5717-4562-b3fc-2c963f66afa6"
    record = {
        "date": "2025-03-07T03:56:34.028Z",
        "user_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "total": 100.00,
    }
    response = client.put(f"/v1/update_record/{table}/{record_id}", json=record)
    assert response.status_code == 404
    assert response.json() is None


@pytest.mark.asyncio
async def test_delete_record_hit():
    table = "orders"
    record_id = "2a3bf8e3-ee45-4856-a5b1-04935cc50e4e"
    response = client.delete(f"/v1/delete_record/{table}/{record_id}")
    assert response.status_code == 204


@pytest.mark.asyncio
async def test_delete_record_miss():
    table = "orders"
    record_id = str(uuid4())
    response = client.delete(f"/v1/delete_record/{table}/{record_id}")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_join_tables_hit():
    table1 = "orders"
    table2 = "users"
    key = "user_id"
    response = client.get(f"/v1/join/{table1}/{table2}/{key}")
    assert response.status_code == 200
    assert response.json() is not None
    assert len(response.json()) > 0


@pytest.mark.asyncio
async def test_join_tables_miss():
    table1 = "orders"
    table2 = "users"
    key = "whale_id"
    response = client.get(f"/v1/join/{table1}/{table2}/{key}")
    assert response.status_code == 200
    assert response.json() is None

@pytest.mark.asyncio
async def test_add_record_invalid_table():
    table = "invalid_table"
    records = [
        {
            "date": "2025-03-07T03:56:34.028Z",
            "user_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            "total": 100.00,
        }
    ]
    response = client.post(f"/v1/add_record/{table}", json=records)
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_add_record_invalid_data():
    with pytest.raises(ValidationError):
        table = "orders"
        records = [
            {
                "date": "invalid_date",
                "user_id": "invalid_uuid",
                "total": "invalid_total",
            }
        ]
        response = client.post(f"/v1/add_record/{table}", json=records)
        assert response.status_code == 422


@pytest.mark.asyncio
async def test_update_record_invalid_table():
    table = "invalid_table"
    record_id = "2a3bf8e3-ee45-4856-a5b1-04935cc50e4e"
    record = {
        "date": "2025-03-07T03:56:34.028Z",
        "user_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "total": 100.00,
    }
    response = client.put(f"/v1/update_record/{table}/{record_id}", json=record)
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_update_record_invalid_data():
    with pytest.raises(ValidationError):
        table = "orders"
        record_id = "2a3bf8e3-ee45-4856-a5b1-04935cc50e4e"
        record = {
            "date": "invalid_date",
            "user_id": "invalid_uuid",
            "total": "invalid_total",
        }
        response = client.put(f"/v1/update_record/{table}/{record_id}", json=record)
        assert response.status_code == 422


@pytest.mark.asyncio
async def test_delete_record_invalid_table():
    table = "invalid_table"
    record_id = "2a3bf8e3-ee45-4856-a5b1-04935cc50e4e"
    response = client.delete(f"/v1/delete_record/{table}/{record_id}")
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_delete_record_invalid_id():
    table = "orders"
    record_id = "invalid_uuid"
    response = client.delete(f"/v1/delete_record/{table}/{record_id}")
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_join_tables_invalid_table1():
    table1 = "invalid_table"
    table2 = "users"
    key = "user_id"
    response = client.get(f"/v1/join/{table1}/{table2}/{key}")
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_join_tables_invalid_table2():
    table1 = "orders"
    table2 = "invalid_table"
    key = "user_id"
    response = client.get(f"/v1/join/{table1}/{table2}/{key}")
    assert response.status_code == 422
