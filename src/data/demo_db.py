import pandas as pd
import json

from uuid import UUID
from datetime import datetime

from src.users.schemas import User, CreateUser
from src.orders.schemas import Order, CreateOrder
from src.logger import logger
from .init_db import init_db


format_string = "%Y-%m-%dT%H:%M:%S"


def load_tables():
    init_db()
    global USERS, ORDERS
    from src.data.init_db import USERS, ORDERS


load_tables()


async def get_users_demo_db() -> list[User]:
    global USERS
    return USERS


async def get_orders_demo_db() -> list[Order]:
    global ORDERS
    return ORDERS


async def get_user_by_id_demo_db(id: UUID) -> User:
    global USERS
    for user in USERS:
        if user.user_id == id:
            return user
    return None


async def get_order_by_id_demo_db(id: UUID) -> Order:
    global ORDERS
    for order in ORDERS:
        if order.order_id == id:
            return order
    return None


async def update_user_by_id_demo_db(id: UUID, user: CreateUser) -> User:
    global USERS
    for db_user in USERS:
        if db_user.user_id == id:
            db_user = User(
                user_id=db_user.user_id,
                name=user.name,
                email=user.email,
                active=db_user.active,
            )
            return db_user
    return None


async def update_order_by_id_demo_db(id: UUID, order: CreateOrder) -> Order:
    global ORDERS
    for db_order in ORDERS:
        if db_order.order_id == id:
            db_order = Order(
                order_id=db_order.order_id,
                date=order.date,
                user_id=order.user_id,
                total=order.total,
            )
            logger.info(f"updated order: {db_order}")
            return db_order
    return None


async def add_users_to_db(users):
    global USERS
    users_db = [User(**user) for user in users]
    USERS.extend(users_db)


async def add_orders_to_db(orders):
    global ORDERS
    orders_db = [Order(**order) for order in orders]
    ORDERS.extend(orders_db)


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
    global USERS
    for user in USERS:
        if user.user_id == id:
            USERS.remove(user)
            return 1
    return None


async def delete_order_by_id_demo_db(id: UUID) -> None:
    global ORDERS
    for order in ORDERS:
        if order.order_id == id:
            ORDERS.remove(order)
            return 1
    return None


async def get_orders_by_user_id_demo_db(user_id: UUID) -> list[Order]:
    global ORDERS
    return [order for order in ORDERS if order.user_id == user_id]


async def join_tables(table1, table2, key):
    table1_parsed = [table.model_dump(mode="python") for table in table1]
    table2_parsed = [table.model_dump(mode="python") for table in table2]
    df1 = pd.DataFrame(table1_parsed)
    df2 = pd.DataFrame(table2_parsed)
    try:
        result = pd.merge(df1, df2, how="left", left_on=key, right_on=key)
        return result.to_dict(orient="records")
    except Exception as e:
        logger.error(f"Error joining tables: {e}")
    return None
