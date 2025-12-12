from __future__ import annotations
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict


class ContactInfo(BaseModel):
    id: str = Field(alias="id")
    full_name: Optional[str] = Field(default=None, alias="fullName")
    business_name: Optional[str] = Field(default=None, alias="businessName")
    push_name: Optional[str] = Field(default=None, alias="pushName")
    status: Optional[str] = Field(default=None, alias="status")
    picture_id: Optional[str] = Field(default=None, alias="pictureId")
    in_phone_address_book: Optional[bool] = Field(default=None, alias="inPhoneAddressBook")

    model_config = ConfigDict(populate_by_name=True)
