from __future__ import annotations
from pydantic import BaseModel, Field, ConfigDict


class AccountUpdateNameRequest(BaseModel):
    name: str = Field(alias="name")

    model_config = ConfigDict(populate_by_name=True)