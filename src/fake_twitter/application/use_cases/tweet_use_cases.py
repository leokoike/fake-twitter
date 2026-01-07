from typing import List, Optional
from uuid import UUID

from fake_twitter.domain.entities.tweet import Tweet
from fake_twitter.domain.repositories.tweet_repository import TweetRepository
from fake_twitter.application.dtos.tweet_dtos import TweetCreateDTO, TweetUpdateDTO


class TweetUseCases:
    def __init__(self, tweet_repository: TweetRepository):
        self.tweet_repository = tweet_repository

    async def create_tweet(self, tweet_dto: TweetCreateDTO) -> Tweet:
        tweet = Tweet(
            content=tweet_dto.content,
            user_id=tweet_dto.user_id,
        )
        return await self.tweet_repository.create(tweet)

    async def get_tweet_by_id(self, tweet_id: UUID) -> Optional[Tweet]:
        return await self.tweet_repository.get_by_id(tweet_id)

    async def get_tweets_by_user(self, user_id: UUID, skip: int = 0, limit: int = 100) -> List[Tweet]:
        return await self.tweet_repository.get_by_user_id(user_id, skip, limit)

    async def get_all_tweets(self, skip: int = 0, limit: int = 100) -> List[Tweet]:
        return await self.tweet_repository.get_all(skip, limit)

    async def update_tweet(self, tweet_id: UUID, tweet_dto: TweetUpdateDTO) -> Optional[Tweet]:
        tweet = await self.tweet_repository.get_by_id(tweet_id)
        if not tweet:
            return None
        
        tweet.content = tweet_dto.content
        return await self.tweet_repository.update(tweet)

    async def delete_tweet(self, tweet_id: UUID) -> bool:
        return await self.tweet_repository.delete(tweet_id)

    async def like_tweet(self, tweet_id: UUID) -> Optional[Tweet]:
        tweet = await self.tweet_repository.get_by_id(tweet_id)
        if not tweet:
            return None
        
        tweet.like()
        return await self.tweet_repository.update(tweet)

    async def unlike_tweet(self, tweet_id: UUID) -> Optional[Tweet]:
        tweet = await self.tweet_repository.get_by_id(tweet_id)
        if not tweet:
            return None
        
        tweet.unlike()
        return await self.tweet_repository.update(tweet)

    async def retweet(self, tweet_id: UUID) -> Optional[Tweet]:
        tweet = await self.tweet_repository.get_by_id(tweet_id)
        if not tweet:
            return None
        
        tweet.retweet()
        return await self.tweet_repository.update(tweet)
