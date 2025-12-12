from __future__ import annotations
from pydantic import BaseModel, Field, ConfigDict


class GroupParticipantInfo(BaseModel):
    id: str = Field(alias="id")
    is_admin: bool = Field(alias="isAdmin")
    is_super_admin: bool = Field(alias="isSuperAdmin")
    display_name: str = Field(alias="displayName")

    model_config = ConfigDict(populate_by_name=True)