from __future__ import annotations
from typing import List
from pydantic import BaseModel, Field, ConfigDict


class GroupUpdateRequestParticipantsRequest(BaseModel):
    participants: List[str] = Field(alias="participants", default_factory=list)
    action: str = Field(alias="action")

    model_config = ConfigDict(populate_by_name=True)