from pydantic import BaseModel, Field  # , ConfigDict, AliasChoices
from datetime import datetime

# from pydantic.alias_generators import to_camel
# uncomment and reference for db model
from typing import Optional
from uuid import UUID, uuid4


class Order(BaseModel):
    order_id: UUID = Field(default_factory=uuid4)
    date: datetime = Field(description="date the order was placed")
    user_id: UUID = Field(description="userid of the user who placed the order")
    total: float = Field(description="total price of the order")


class CreateOrder(BaseModel):
    date: datetime = Field(description="date the order was placed")
    user_id: UUID = Field(description="userid of the user who placed the order")
    total: float = Field(description="total price of the order")
