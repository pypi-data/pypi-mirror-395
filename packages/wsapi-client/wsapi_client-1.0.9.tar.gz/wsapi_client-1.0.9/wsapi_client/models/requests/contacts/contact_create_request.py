from __future__ import annotations
from pydantic import BaseModel, Field, ConfigDict


class ContactCreateRequest(BaseModel):
    id: str = Field(alias="id")
    full_name: str = Field(alias="fullName")
    first_name: str = Field(alias="firstName")

    model_config = ConfigDict(populate_by_name=True)