from __future__ import annotations
from pydantic import BaseModel, Field, ConfigDict


class ChatPicture(BaseModel):
    picture_id: str = Field(alias="pictureId")
    picture_url: str = Field(alias="pictureUrl")

    model_config = ConfigDict(populate_by_name=True)
