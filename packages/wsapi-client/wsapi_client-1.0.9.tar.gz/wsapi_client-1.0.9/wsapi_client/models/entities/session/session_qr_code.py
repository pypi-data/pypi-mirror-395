from __future__ import annotations
from pydantic import BaseModel, Field, ConfigDict


class SessionQRCode(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    qr_code: str = Field(alias="qrCode")
