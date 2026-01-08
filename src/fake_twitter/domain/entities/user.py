from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4
from pydantic import BaseModel, ConfigDict, Field, EmailStr


class User(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID = Field(default_factory=uuid4)
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    full_name: str = Field(..., min_length=1, max_length=100)
    bio: Optional[str] = Field(None, max_length=500)
    created_at: datetime = Field(default_factory=datetime.now)
    followers_count: int = Field(default=0, ge=0)
    following_count: int = Field(default=0, ge=0)

    def follow(self) -> None:
        self.followers_count += 1

    def unfollow(self) -> None:
        if self.followers_count > 0:
            self.followers_count -= 1
