from datetime import datetime
from uuid import UUID, uuid4
from pydantic import BaseModel, ConfigDict, Field


class Tweet(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID = Field(default_factory=uuid4)
    content: str = Field(..., min_length=1, max_length=280)
    user_id: UUID
    created_at: datetime = Field(default_factory=datetime.now)
    likes_count: int = Field(default=0, ge=0)
    retweets_count: int = Field(default=0, ge=0)

    def like(self) -> None:
        self.likes_count += 1

    def unlike(self) -> None:
        if self.likes_count > 0:
            self.likes_count -= 1

    def retweet(self) -> None:
        self.retweets_count += 1
