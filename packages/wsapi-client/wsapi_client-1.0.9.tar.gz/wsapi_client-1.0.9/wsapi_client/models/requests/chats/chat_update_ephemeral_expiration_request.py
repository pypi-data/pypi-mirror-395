from __future__ import annotations
from pydantic import BaseModel, Field, ConfigDict


class ChatUpdateEphemeralExpirationRequest(BaseModel):
    expiration: str = Field(alias="expiration")

    model_config = ConfigDict(populate_by_name=True)