from __future__ import annotations
from typing import List
from pydantic import BaseModel, Field, ConfigDict


class GroupCreateRequest(BaseModel):
    name: str = Field(alias="name")
    participants: List[str] = Field(alias="participants", default_factory=list)

    model_config = ConfigDict(populate_by_name=True)