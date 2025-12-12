from __future__ import annotations
from pydantic import BaseModel, Field, ConfigDict


class GroupUpdateDescriptionRequest(BaseModel):
    description: str = Field(alias="description")

    model_config = ConfigDict(populate_by_name=True)