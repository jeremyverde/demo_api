from fastapi.testclient import TestClient
import asyncio
import pytest

from src.main import app
from unittest.mock import MagicMock

pytest_plugins = "pytest_asyncio"

client = TestClient(app)


@pytest.mark.asyncio
async def test_health_return_time_env():
    response = client.get("health")
    assert response.status_code == 200
    assert response.json()["time"] != None
