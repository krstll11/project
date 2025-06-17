from pydantic import BaseModel
from pydantic import Field, field_validator
import re
class UserCreate(BaseModel):
    email: str = Field(..., max_length=100)
    nickname: str = Field(..., max_length=50)
    password: str = Field(..., min_length=8, max_length=100, example="Strongpassword123")
    
    @field_validator("password")
    def password_strength(cls, v):
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters long")
        if not re.search(r"\d", v):
            raise ValueError("Password must contain at least one digit")
        if not re.search(r"[A-Z]", v):
            raise ValueError("Password must contain at least one uppercase letter")
        return v

class UserBase(BaseModel):
    id: int
    email: str
    nickname: str

    class Config:
        from_attributes = True 