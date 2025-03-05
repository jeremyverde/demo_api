from fastapi import APIRouter
from .schemas import User
from src.data.demo_db import get_users_demo_db, get_user_by_id

router = APIRouter(tags=["users"])


@router.get("/v1/users")
async def get_users() -> list[User]:
    users = await get_users_demo_db()
    return users
