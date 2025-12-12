from __future__ import annotations
from typing import List, Optional
from pydantic import BaseModel, Field, ConfigDict


class InstanceSettings(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    name: Optional[str] = Field(default=None, alias="name")
    description: Optional[str] = Field(default=None, alias="description")
    webhook_url: Optional[str] = Field(default=None, alias="webhookUrl")
    webhook_auth_header: Optional[str] = Field(default=None, alias="webhookAuthHeader")
    webhook_auth_value: Optional[str] = Field(default=None, alias="webhookAuthValue")
    pull_mode: Optional[bool] = Field(default=None, alias="pullMode")
    event_filters: Optional[List[str]] = Field(default=None, alias="eventFilters")
