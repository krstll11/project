from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class RoleBase(BaseModel):
    name: str = Field(..., max_length=50)

class UserBase(BaseModel):
    email: EmailStr = Field(..., max_length=100)
    nickname: str = Field(..., max_length=50)
    role_id: int

class CategoryBase(BaseModel):
    name: str = Field(..., max_length=50)

class AdBase(BaseModel):
    title: str = Field(..., max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    price: Optional[float] = None
    author_id: int
    category_id: int

class ResponseBase(BaseModel):
    message: str = Field(..., max_length=500)
    ad_id: int
    user_id: int

class FavoriteBase(BaseModel):
    id: int
    ad_id: int
    user_id: int