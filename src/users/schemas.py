from pydantic import BaseModel, Field  # , ConfigDict, AliasChoices

# from pydantic.alias_generators import to_camel
# uncomment and reference for db model
from typing import Optional
from uuid import UUID, uuid4


class User(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    name: str = Field(description="user's full name")
    email: str = Field(description="user's email address")
    active: bool = Field(description="user's current state", default=True)


class CreateUser(BaseModel):
    name: str = Field(description="user's full name")
    email: str = Field(description="user's email address")
