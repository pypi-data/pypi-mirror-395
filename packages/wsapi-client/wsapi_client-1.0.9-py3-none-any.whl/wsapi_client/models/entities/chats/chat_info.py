from __future__ import annotations
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict


class ChatInfo(BaseModel):
    id: str = Field(alias="id")
    name: Optional[str] = Field(default=None, alias="name")
    push_name: Optional[str] = Field(default=None, alias="pushName")
    is_group: Optional[bool] = Field(default=None, alias="isGroup")
    is_read_only: Optional[bool] = Field(default=None, alias="isReadOnly")
    is_archived: Optional[bool] = Field(default=None, alias="isArchived")
    is_pinned: Optional[bool] = Field(default=None, alias="isPinned")
    is_muted: Optional[bool] = Field(default=None, alias="isMuted")
    is_spam: Optional[bool] = Field(default=None, alias="isSpam")

    model_config = ConfigDict(populate_by_name=True)
