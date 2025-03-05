from datetime import datetime
from src.users.schemas import User


user_table = [{'id':1,'name':'Jeremy','email':'jeremy@jeremy.com','active': True}]
order_table = [{'id':123456, 'date':datetime.now(), "user":1, "total":811.19}]

async def get_users_demo_db() -> list[User]:
    return [User(**user) for user in user_table]

async def get_user_by_id(id: int) -> User:
    for user in user_table:
        if user['id'] == id:
            return User(**user)
    return None
