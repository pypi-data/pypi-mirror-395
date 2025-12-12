from __future__ import annotations
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict


class ChatUpdateMuteRequest(BaseModel):
    duration: Optional[str] = Field(alias="duration", default=None)

    model_config = ConfigDict(populate_by_name=True)