from __future__ import annotations
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict


class GroupInviteInfo(BaseModel):
    code: str = Field(alias="code")
    group: str = Field(alias="group")
    expires: Optional[str] = Field(default=None, alias="expires")

    model_config = ConfigDict(populate_by_name=True)
