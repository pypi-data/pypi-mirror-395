from __future__ import annotations
from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict
from ...entities.users.sender import Sender


class GroupDescription(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    topic: Optional[str] = None
    timestamp: Optional[datetime] = None


class GroupEvent(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    id: str
    sender: Sender
    description: Optional[GroupDescription] = None
