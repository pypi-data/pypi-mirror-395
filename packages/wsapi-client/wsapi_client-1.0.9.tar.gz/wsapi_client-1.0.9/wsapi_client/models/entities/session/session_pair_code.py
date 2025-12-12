from __future__ import annotations
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict


class SessionPairCode(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    code: str = Field(alias="code")
    # Legacy field for backwards compatibility
    phone_number: Optional[str] = Field(default=None, alias="phoneNumber")
