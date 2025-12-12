from __future__ import annotations
from pydantic import BaseModel, Field, ConfigDict


class ContactUpdateRequest(BaseModel):
    full_name: str = Field(alias="fullName")
    first_name: str = Field(alias="firstName")

    model_config = ConfigDict(populate_by_name=True)