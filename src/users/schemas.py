from pydantic import BaseModel, Field # , ConfigDict, AliasChoices
# from pydantic.alias_generators import to_camel
# uncomment and reference for db model 
from typing import Optional

class User(BaseModel):
    id: int = Field(description="unique user ID")
    name: str = Field(description="user's full name")
    email: str = Field(description="user's email address")
    active: bool = Field(description="user's current state")
