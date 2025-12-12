from __future__ import annotations
from typing import Dict, List, Optional
from pydantic import BaseModel, Field, ConfigDict


class ChatBusinessCategory(BaseModel):
    id: str = Field(alias="id")
    name: str = Field(alias="name")

    model_config = ConfigDict(populate_by_name=True)


class BusinessHours(BaseModel):
    day_of_week: str = Field(alias="dayOfWeek")
    mode: str = Field(alias="mode")
    open_time: str = Field(alias="openTime")
    close_time: str = Field(alias="closeTime")

    model_config = ConfigDict(populate_by_name=True)


class ChatBusinessProfile(BaseModel):
    id: str = Field(alias="id")
    address: str = Field(alias="address")
    description: str = Field(alias="description")
    email: str = Field(alias="email")
    website: str = Field(alias="website")
    latitude: float = Field(alias="latitude")
    longitude: float = Field(alias="longitude")
    member_since: str = Field(alias="memberSince")
    categories: List[ChatBusinessCategory] = Field(alias="categories")
    business_hours_time_zone: str = Field(alias="businessHoursTimeZone")
    business_hours: List[BusinessHours] = Field(alias="businessHours")
    profile_options: Dict[str, str] = Field(alias="profileOptions")

    model_config = ConfigDict(populate_by_name=True)
