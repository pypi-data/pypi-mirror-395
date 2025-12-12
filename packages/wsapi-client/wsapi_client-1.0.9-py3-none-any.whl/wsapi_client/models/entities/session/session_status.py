from __future__ import annotations
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict


class SessionStatus(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    connected: bool = Field(alias="connected")
    is_logged_in: bool = Field(alias="isLoggedIn")
    # Legacy fields for backwards compatibility
    status: Optional[str] = Field(default=None, alias="status")
    message: Optional[str] = Field(default=None, alias="message")
