from abc import ABC, abstractmethod
from typing import Optional, List
from uuid import UUID

from src.fake_twitter.domain.entities.tweet import Tweet


class TweetRepository(ABC):
    @abstractmethod
    async def create(self, tweet: Tweet) -> Tweet:
        pass

    @abstractmethod
    async def get_by_id(self, tweet_id: UUID) -> Optional[Tweet]:
        pass

    @abstractmethod
    async def get_by_user_id(
        self, user_id: UUID, skip: int = 0, limit: int = 100
    ) -> List[Tweet]:
        pass

    @abstractmethod
    async def get_all(self, skip: int = 0, limit: int = 100) -> List[Tweet]:
        pass

    @abstractmethod
    async def update(self, tweet: Tweet) -> Tweet:
        pass

    @abstractmethod
    async def delete(self, tweet_id: UUID) -> bool:
        pass
