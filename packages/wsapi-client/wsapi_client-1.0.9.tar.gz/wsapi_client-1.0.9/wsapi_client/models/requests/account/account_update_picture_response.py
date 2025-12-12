from __future__ import annotations
from pydantic import BaseModel, Field, ConfigDict


class AccountUpdatePictureResponse(BaseModel):
    picture_id: str = Field(alias="pictureId")

    model_config = ConfigDict(populate_by_name=True)