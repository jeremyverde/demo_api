from fastapi.testclient import TestClient
import asyncio
import pytest

from src.main import app
from unittest.mock import MagicMock

pytest_plugins = ('pytest_asyncio')

client = TestClient(app)


@pytest.mark.asyncio
async def test_health_return_time_env():
    response = client.get("/v1/users")
    assert response.status_code == 200
    response_json = response.json()
    assert len(response_json) != None
    assert response_json[0]["name"] != None
