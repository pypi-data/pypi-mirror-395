from __future__ import annotations
from pydantic import BaseModel, Field, ConfigDict


class AccountUpdatePictureRequest(BaseModel):
    picture_base64: str = Field(alias="pictureBase64")

    model_config = ConfigDict(populate_by_name=True)