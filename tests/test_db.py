import pytest
from datetime import datetime
from uuid import UUID, uuid4
from src.users.schemas import User, CreateUser
from src.orders.schemas import Order, CreateOrder

from src.data.demo_db import (
    get_users_demo_db,
    get_orders_demo_db,
    get_user_by_id_demo_db,
    get_order_by_id_demo_db,
    create_users_demo_db,
    create_orders_demo_db,
    delete_user_by_id_demo_db,
    delete_order_by_id_demo_db,
    get_orders_by_user_id_demo_db,
)


@pytest.mark.asyncio
async def test_get_users_demo_db():
    users = await get_users_demo_db()
    assert len(users) == 1
    assert users[0].name == "John Wick"


@pytest.mark.asyncio
async def test_get_orders_demo_db():
    orders = await get_orders_demo_db()
    assert len(orders) == 1
    assert orders[0].total == 811.19


@pytest.mark.asyncio
async def test_get_user_by_id_demo_db():
    user_id = UUID("be7c9d38-49f6-4970-b636-6ffa90bba41b")
    user = await get_user_by_id_demo_db(user_id)
    assert user is not None
    assert user.name == "John Wick"


@pytest.mark.asyncio
async def test_get_order_by_id_demo_db():
    order_id = UUID("2a3bf8e3-ee45-4856-a5b1-04935cc50e4e")
    order = await get_order_by_id_demo_db(order_id)
    assert order is not None
    assert order.total == 811.19


@pytest.mark.asyncio
async def test_create_users_demo_db():
    new_users = [CreateUser(name="Jane Doe", email="jane@doe.com")]
    created_users = await create_users_demo_db(new_users)
    assert len(created_users) == 1
    assert created_users[0].name == "Jane Doe"


@pytest.mark.asyncio
async def test_create_orders_demo_db():
    order_date = datetime.now()
    new_orders = [
        CreateOrder(
            date=order_date,
            user_id="be7c9d38-49f6-4970-b636-6ffa90bba41b",
            total=123.45,
        )
    ]
    created_orders = await create_orders_demo_db(new_orders)
    assert len(created_orders) == 1
    assert created_orders[0].total == 123.45


@pytest.mark.asyncio
async def test_delete_user_by_id_demo_db():
    user_id = UUID("be7c9d38-49f6-4970-b636-6ffa90bba41b")
    await delete_user_by_id_demo_db(user_id)
    user = await get_user_by_id_demo_db(user_id)
    assert user is None


@pytest.mark.asyncio
async def test_delete_order_by_id_demo_db():
    order_id = UUID("2a3bf8e3-ee45-4856-a5b1-04935cc50e4e")
    await delete_order_by_id_demo_db(order_id)
    order = await get_order_by_id_demo_db(order_id)
    assert order is None


@pytest.mark.asyncio
async def test_get_orders_by_user_id_demo_db():
    user_id = UUID("be7c9d38-49f6-4970-b636-6ffa90bba41b")
    orders = await get_orders_by_user_id_demo_db(user_id)
    assert len(orders) == 1
    assert orders[0].total == 123.45
    assert orders[0].user_id == user_id
