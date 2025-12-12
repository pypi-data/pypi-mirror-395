from __future__ import annotations
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict


class Sender(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    id: str
    is_me: Optional[bool] = Field(default=None, alias="isMe")
    push_name: Optional[str] = Field(default=None, alias="pushName")
    # Legacy fields for backwards compatibility
    user: Optional[str] = None
    device: Optional[int] = None
