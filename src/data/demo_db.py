from datetime import datetime
from src.users.schemas import User, CreateUser
from src.orders.schemas import Order, CreateOrder
from uuid import UUID
import pandas as pd

from src.logger import logger


format_string = "%Y-%m-%dT%H:%M:%S"

user_table = [
    {
        "user_id": UUID("be7c9d38-49f6-4970-b636-6ffa90bba41b"),
        "name": "John Wick",
        "email": "johnny@utah.com",
        "active": True,
    }
]
order_table = [
    {
        "order_id": UUID("2a3bf8e3-ee45-4856-a5b1-04935cc50e4e"),
        "date": datetime.now(),
        "user_id": UUID("be7c9d38-49f6-4970-b636-6ffa90bba41b"),
        "total": 811.19,
    }
]


async def get_users_demo_db() -> list[User]:
    return [User(**user) for user in user_table]


async def get_orders_demo_db() -> list[Order]:
    return [Order(**order) for order in order_table]


async def get_user_by_id_demo_db(id: UUID) -> User:
    for user in user_table:
        if user.get("user_id") == id:
            return User(**user)
    return None


async def get_order_by_id_demo_db(id: UUID) -> Order:
    for order in order_table:
        if order.get("order_id") == id:
            return Order(**order)
    return None


async def update_user_by_id_demo_db(id: UUID, user: CreateUser) -> User:
    for db_user in user_table:
        if db_user.get("user_id") == id:
            db_user.update(user)
            return User(**db_user)
    return None


async def update_order_by_id_demo_db(id: UUID, order: CreateOrder) -> Order:
    for db_order in order_table:
        print(f"db_order: {db_order}")
        if db_order.get("order_id") == id:
            db_order.update(order)
            print(f"updated order: {db_order}")
            logger.info(f"updated order: {db_order}")
            return Order(**db_order)
    print(f"order not found: {id}")
    return None


async def add_users_to_db(users):
    user_table.extend(users)


async def add_orders_to_db(orders):
    order_table.extend(orders)


async def create_users_demo_db(users: list[CreateUser]):
    new_users = []
    for user in users:
        user_rec = User(name=user.name, email=user.email)
        new_users.append(user_rec.model_dump(mode="python"))
    await add_users_to_db(new_users)
    return [User(**user) for user in new_users]


async def create_orders_demo_db(orders: list[CreateOrder]):
    new_orders = []
    for order in orders:
        order_rec = Order(date=order.date, user_id=order.user_id, total=order.total)
        new_orders.append(order_rec.model_dump(mode="python"))
    await add_orders_to_db(new_orders)
    return [Order(**order) for order in new_orders]


async def delete_user_by_id_demo_db(id: UUID) -> None:
    for user in user_table:
        if user["user_id"] == id:
            user_table.remove(user)
            return 1
    return None


async def delete_order_by_id_demo_db(id: UUID) -> None:
    for order in order_table:
        if order["order_id"] == id:
            order_table.remove(order)
            return 1
    return None


async def get_orders_by_user_id_demo_db(user_id: UUID) -> list[Order]:
    return [Order(**order) for order in order_table if order["user_id"] == user_id]


async def join_tables(table1, table2, key):
    df1 = pd.DataFrame(table1)
    df2 = pd.DataFrame(table2)
    try:
        result = pd.merge(df1, df2, left_on=key, right_on=key)
        return result
    except Exception as e:
        logger.error(f"Error joining tables: {e}")
    return None
