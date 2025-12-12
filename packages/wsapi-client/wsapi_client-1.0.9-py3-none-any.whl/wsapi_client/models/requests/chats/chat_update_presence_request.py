from __future__ import annotations
from pydantic import BaseModel, Field, ConfigDict


class ChatUpdatePresenceRequest(BaseModel):
    state: str = Field(alias="state")

    model_config = ConfigDict(populate_by_name=True)