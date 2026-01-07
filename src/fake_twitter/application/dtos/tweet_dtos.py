from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, Field


class TweetCreateDTO(BaseModel):
    content: str = Field(..., min_length=1, max_length=280)
    user_id: UUID


class TweetUpdateDTO(BaseModel):
    content: str = Field(..., min_length=1, max_length=280)


class TweetResponseDTO(BaseModel):
    id: UUID
    content: str
    user_id: UUID
    created_at: datetime
    likes_count: int
    retweets_count: int

    class Config:
        from_attributes = True
