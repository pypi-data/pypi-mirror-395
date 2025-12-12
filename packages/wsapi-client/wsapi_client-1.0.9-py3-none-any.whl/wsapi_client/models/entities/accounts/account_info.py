from __future__ import annotations
from pydantic import BaseModel, Field, ConfigDict


class AccountInfo(BaseModel):
    id: str = Field(alias="id")
    device_id: int = Field(alias="deviceId")
    phone: str = Field(alias="phone")
    push_name: str = Field(alias="pushName")
    business_name: str = Field(alias="businessName")
    status: str = Field(alias="status")
    picture_id: str = Field(alias="pictureId")

    model_config = ConfigDict(populate_by_name=True)