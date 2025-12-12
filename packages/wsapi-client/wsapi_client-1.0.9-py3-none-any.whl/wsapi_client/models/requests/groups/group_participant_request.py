from __future__ import annotations
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict


class GroupParticipantRequest(BaseModel):
    user_id: str = Field(alias="userId")
    requested_at: datetime = Field(alias="requestedAt")

    model_config = ConfigDict(populate_by_name=True)