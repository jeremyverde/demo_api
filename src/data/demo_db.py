from datetime import datetime
from src.users.schemas import User, CreateUser
from src.orders.schemas import Order, CreateOrder
from uuid import UUID


format_string = "%Y-%m-%dT%H:%M:%S"

user_table = [
    {
        "id": UUID("be7c9d38-49f6-4970-b636-6ffa90bba41b"),
        "name": "John Wick",
        "email": "johnny@utah.com",
        "active": True,
    }
]
order_table = [
    {
        "id": UUID("2a3bf8e3-ee45-4856-a5b1-04935cc50e4e"),
        "date": datetime.now(),
        "user": UUID("be7c9d38-49f6-4970-b636-6ffa90bba41b"),
        "total": 811.19,
    }
]


async def get_users_demo_db() -> list[User]:
    return [User(**user) for user in user_table]


async def get_orders_demo_db() -> list[Order]:
    return [Order(**order) for order in order_table]


async def get_user_by_id_demo_db(id: UUID) -> User:
    for user in user_table:
        if user["id"] == id:
            return User(**user)
    return None


async def get_order_by_id_demo_db(id: UUID) -> Order:
    for order in order_table:
        if order["id"] == id:
            return Order(**order)
    return None


# todo: exceptions
async def add_users_to_db(users):
    user_table.extend(users)


async def add_orders_to_db(orders):
    order_table.extend(orders)


# todo: check exists against email
# todo: cleanup
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
        order_rec = Order(date=order.date, user=order.user, total=order.total)
        new_orders.append(order_rec.model_dump(mode="python"))
    await add_orders_to_db(new_orders)
    return [Order(**order) for order in new_orders]


async def delete_user_by_id_demo_db(id: UUID) -> None:
    for user in user_table:
        if user["id"] == id:
            user_table.remove(user)
            return None
    return None


async def delete_order_by_id_demo_db(id: UUID) -> None:
    for order in order_table:
        if order["id"] == id:
            order_table.remove(order)
            return None
    return None
