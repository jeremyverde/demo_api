from fastapi import APIRouter, status
from uuid import UUID
from .schemas import User, CreateUser
from src.orders.schemas import Order
from src.data.demo_db import (
    get_users_demo_db,
    get_user_by_id_demo_db,
    create_users_demo_db,
    delete_user_by_id_demo_db,
    get_orders_by_user_id_demo_db,
)


router = APIRouter(tags=["users"])


@router.get("/v1/users")
async def get_users() -> list[User]:
    users = await get_users_demo_db()
    return users


@router.post("/v1/users", status_code=status.HTTP_201_CREATED)
async def create_users(users: list[CreateUser]) -> list[User]:
    return await create_users_demo_db(users)


@router.get("/v1/users/{user_id}")
async def get_user_by_id(user_id: UUID) -> User:
    return await get_user_by_id_demo_db(user_id)


@router.delete("/v1/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user_by_id(user_id: UUID) -> None:
    return await delete_user_by_id_demo_db(user_id)


@router.get("/v1/users/{user_id}/orders")
async def get_user_orders(user_id: UUID) -> list[Order]:
    return await get_orders_by_user_id_demo_db(user_id)
