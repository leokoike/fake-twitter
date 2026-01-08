from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field, EmailStr


class UserCreateDTO(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    full_name: str = Field(..., min_length=1, max_length=100)
    bio: Optional[str] = Field(None, max_length=500)


class UserUpdateDTO(BaseModel):
    full_name: Optional[str] = Field(None, min_length=1, max_length=100)
    bio: Optional[str] = Field(None, max_length=500)


class UserResponseDTO(BaseModel):
    id: UUID
    username: str
    email: EmailStr
    full_name: str
    bio: Optional[str]
    created_at: datetime
    followers_count: int
    following_count: int

    model_config = ConfigDict(from_attributes=True)
