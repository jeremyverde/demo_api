from fastapi import APIRouter

router = APIRouter(tags=["users"])


@router.get("/v1/users")
async def get_users():
    return [{"user_id": 1, "user": {}}]
