from fastapi import APIRouter, status
from uuid import UUID
from .schemas import Order, CreateOrder
from src.data.demo_db import (
    get_orders_demo_db,
    get_order_by_id_demo_db,
    create_orders_demo_db,
    delete_order_by_id_demo_db,
)

router = APIRouter(tags=["orders"])


@router.get("/v1/orders")
async def get_orders() -> list[Order]:
    users = await get_orders_demo_db()
    return users


@router.post("/v1/orders", status_code=status.HTTP_201_CREATED)
async def create_orders(users: list[CreateOrder]) -> list[Order]:
    return await create_orders_demo_db(users)


@router.get("/v1/orders/{order_id}")
async def get_order_by_id(order_id: UUID) -> Order:
    return await get_order_by_id_demo_db(order_id)


@router.delete("/v1/orders/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_order_by_id(order_id: UUID) -> None:
    return await delete_order_by_id_demo_db(order_id)
