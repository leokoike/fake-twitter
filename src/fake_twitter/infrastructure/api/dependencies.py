from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

from src.fake_twitter.application.use_cases.tweet_use_cases import TweetUseCases
from src.fake_twitter.application.use_cases.user_use_cases import UserUseCases
from src.fake_twitter.infrastructure.database.connection import get_db
from src.fake_twitter.infrastructure.repositories.sqlalchemy_tweet_repository import (
    SQLAlchemyTweetRepository,
)
from src.fake_twitter.infrastructure.repositories.sqlalchemy_user_repository import (
    SQLAlchemyUserRepository,
)


async def get_db_session(db: AsyncSession = Depends(get_db)) -> AsyncSession:
    return db


async def get_tweet_use_cases(
    db: AsyncSession = Depends(get_db_session),
) -> TweetUseCases:
    tweet_repository = SQLAlchemyTweetRepository(db)
    return TweetUseCases(tweet_repository)


async def get_user_use_cases(
    db: AsyncSession = Depends(get_db_session),
) -> UserUseCases:
    user_repository = SQLAlchemyUserRepository(db)
    return UserUseCases(user_repository)
