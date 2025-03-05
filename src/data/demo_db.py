from datetime import datetime
from src.users.schemas import User, CreateUser
from uuid import UUID

user_table = [
    {
        "id": "be7c9d38-49f6-4970-b636-6ffa90bba41b",
        "name": "John Wick",
        "email": "johnny@utah.com",
        "active": True,
    }
]
order_table = [
    {
        "id": 123456,
        "date": datetime.now(),
        "user": "be7c9d38-49f6-4970-b636-6ffa90bba41b",
        "total": 811.19,
    }
]


async def get_users_demo_db() -> list[User]:
    return [User(**user) for user in user_table]


async def get_user_by_id_demo_db(id: UUID) -> User:
    for user in user_table:
        if user["id"] == id:
            return User(**user)
    return None


# todo: exceptions
async def add_users_to_db(users):
    user_table.extend(users)


# todo: check exists against email
# todo: cleanup
async def create_users_demo_db(users: list[CreateUser]):
    new_users = []
    for user in users:
        user_rec = User(name=user.name, email=user.email)
        new_users.append(user_rec.model_dump(mode="python"))
    await add_users_to_db(new_users)
    return [User(**user) for user in new_users]

async def delete_user_by_id_demo_db(id: UUID) -> None:
    for user in user_table:
        if user["id"] == id:
            user_table.remove(user)
            return None
    return None