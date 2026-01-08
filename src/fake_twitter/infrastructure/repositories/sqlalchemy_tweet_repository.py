from typing import Optional, List
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.fake_twitter.domain.entities.tweet import Tweet
from src.fake_twitter.domain.repositories.tweet_repository import TweetRepository
from src.fake_twitter.infrastructure.database.models import TweetModel


class SQLAlchemyTweetRepository(TweetRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, tweet: Tweet) -> Tweet:
        tweet_model = TweetModel(**tweet.model_dump())
        self.session.add(tweet_model)
        await self.session.flush()
        await self.session.refresh(tweet_model)
        return Tweet.model_validate(tweet_model)

    async def get_by_id(self, tweet_id: UUID) -> Optional[Tweet]:
        result = await self.session.execute(
            select(TweetModel).where(TweetModel.id == tweet_id)
        )
        tweet_model = result.scalar_one_or_none()
        return Tweet.model_validate(tweet_model) if tweet_model else None

    async def get_by_user_id(
        self, user_id: UUID, skip: int = 0, limit: int = 100
    ) -> List[Tweet]:
        result = await self.session.execute(
            select(TweetModel)
            .where(TweetModel.user_id == user_id)
            .offset(skip)
            .limit(limit)
        )
        tweet_models = result.scalars().all()
        return [Tweet.model_validate(tweet_model) for tweet_model in tweet_models]

    async def get_all(self, skip: int = 0, limit: int = 100) -> List[Tweet]:
        result = await self.session.execute(
            select(TweetModel).offset(skip).limit(limit)
        )
        tweet_models = result.scalars().all()
        return [Tweet.model_validate(tweet_model) for tweet_model in tweet_models]

    async def update(self, tweet: Tweet) -> Tweet:
        result = await self.session.execute(
            select(TweetModel).where(TweetModel.id == tweet.id)
        )
        tweet_model = result.scalar_one_or_none()
        if tweet_model:
            for key, value in tweet.model_dump().items():
                setattr(tweet_model, key, value)
            await self.session.flush()
            await self.session.refresh(tweet_model)
            return Tweet.model_validate(tweet_model)
        raise ValueError(f"Tweet with id {tweet.id} not found")

    async def delete(self, tweet_id: UUID) -> bool:
        result = await self.session.execute(
            select(TweetModel).where(TweetModel.id == tweet_id)
        )
        tweet_model = result.scalar_one_or_none()
        if tweet_model:
            await self.session.delete(tweet_model)
            await self.session.flush()
            return True
        return False
