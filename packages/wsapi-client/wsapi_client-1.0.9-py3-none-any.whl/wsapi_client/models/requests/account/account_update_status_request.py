from __future__ import annotations
from pydantic import BaseModel, Field, ConfigDict


class AccountUpdateStatusRequest(BaseModel):
    status: str = Field(alias="status")

    model_config = ConfigDict(populate_by_name=True)