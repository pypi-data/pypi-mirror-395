from __future__ import annotations
from typing import List
from pydantic import BaseModel, Field, ConfigDict


class GroupUpdateParticipantsRequest(BaseModel):
    participants: List[str] = Field(alias="participants")

    model_config = ConfigDict(populate_by_name=True)
