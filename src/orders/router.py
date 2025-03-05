from fastapi import APIRouter

router = APIRouter(tags=["orders"])


@router.get("/v1/orders")
async def get_orders():
    return [{"order_id": 123, "order": {}}]
