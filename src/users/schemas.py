from pydantic import BaseModel, Field, EmailStr

from uuid import UUID, uuid4


class User(BaseModel):
    user_id: UUID = Field(default_factory=uuid4)
    name: str = Field(description="user's full name")
    email: EmailStr = Field(description="user's email address")
    active: bool = Field(description="user's current state", default=True)


class CreateUser(BaseModel):
    name: str = Field(description="user's full name")
    email: str = Field(description="user's email address")
