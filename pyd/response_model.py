from pydantic import BaseModel
from pydantic import Field, field_validator

from typing import Optional


class ResponseCreate(BaseModel):
    message: str
    ad_id: int
    @field_validator("message")
    def message_not_empty(cls, v):
        if not v.strip():
            raise ValueError("Message cannot be empty")
        return v.strip()