from enum import Enum

from pydantic import BaseModel

from src.users.schemas import CreateUser
from src.orders.schemas import CreateOrder
from src.data.demo_db import (
    update_user_by_id_demo_db,
    update_order_by_id_demo_db,
    create_orders_demo_db,
    create_users_demo_db,
    delete_user_by_id_demo_db,
    delete_order_by_id_demo_db,
    USERS,
    ORDERS,
)

table_map = {
    "orders": {
        "table": "orders",
        "create_schema": CreateOrder,
        "create_function": create_orders_demo_db,
        "update_function": update_order_by_id_demo_db,
        "delete_function": delete_order_by_id_demo_db,
        "table_ref": ORDERS,
    },
    "users": {
        "table": "users",
        "create_schema": CreateUser,
        "create_function": create_users_demo_db,
        "update_function": update_user_by_id_demo_db,
        "delete_function": delete_user_by_id_demo_db,
        "table_ref": USERS,
    },
}


class TableEnum(str, Enum):
    orders = "orders"
    users = "users"


class TableOp(BaseModel):
    table: TableEnum
