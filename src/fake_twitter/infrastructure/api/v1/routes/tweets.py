from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from src.fake_twitter.application.use_cases.tweet_use_cases import TweetUseCases
from src.fake_twitter.application.dtos.tweet_dtos import (
    TweetCreateDTO,
    TweetUpdateDTO,
    TweetResponseDTO,
)
from src.fake_twitter.infrastructure.api.dependencies import get_tweet_use_cases


router = APIRouter(prefix="/tweets", tags=["tweets"])


@router.post("/", response_model=TweetResponseDTO, status_code=status.HTTP_201_CREATED)
async def create_tweet(
    tweet_dto: TweetCreateDTO, use_cases: TweetUseCases = Depends(get_tweet_use_cases)
):
    """Create a new tweet"""
    tweet = await use_cases.create_tweet(tweet_dto)
    return TweetResponseDTO.model_validate(tweet)


@router.get("/{tweet_id}", response_model=TweetResponseDTO)
async def get_tweet(
    tweet_id: UUID, use_cases: TweetUseCases = Depends(get_tweet_use_cases)
):
    """Get a tweet by ID"""
    tweet = await use_cases.get_tweet_by_id(tweet_id)
    if not tweet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Tweet not found"
        )
    return TweetResponseDTO.model_validate(tweet)


@router.get("/user/{user_id}", response_model=List[TweetResponseDTO])
async def get_tweets_by_user(
    user_id: UUID,
    skip: int = 0,
    limit: int = 100,
    use_cases: TweetUseCases = Depends(get_tweet_use_cases),
):
    """Get all tweets by a user with pagination"""
    tweets = await use_cases.get_tweets_by_user(user_id, skip, limit)
    return [TweetResponseDTO.model_validate(tweet) for tweet in tweets]


@router.get("/", response_model=List[TweetResponseDTO])
async def get_all_tweets(
    skip: int = 0,
    limit: int = 100,
    use_cases: TweetUseCases = Depends(get_tweet_use_cases),
):
    """Get all tweets with pagination"""
    tweets = await use_cases.get_all_tweets(skip, limit)
    return [TweetResponseDTO.model_validate(tweet) for tweet in tweets]


@router.put("/{tweet_id}", response_model=TweetResponseDTO)
async def update_tweet(
    tweet_id: UUID,
    tweet_dto: TweetUpdateDTO,
    use_cases: TweetUseCases = Depends(get_tweet_use_cases),
):
    """Update a tweet"""
    tweet = await use_cases.update_tweet(tweet_id, tweet_dto)
    if not tweet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Tweet not found"
        )
    return TweetResponseDTO.model_validate(tweet)


@router.delete("/{tweet_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_tweet(
    tweet_id: UUID, use_cases: TweetUseCases = Depends(get_tweet_use_cases)
):
    """Delete a tweet"""
    deleted = await use_cases.delete_tweet(tweet_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Tweet not found"
        )


@router.post("/{tweet_id}/like", response_model=TweetResponseDTO)
async def like_tweet(
    tweet_id: UUID, use_cases: TweetUseCases = Depends(get_tweet_use_cases)
):
    """Like a tweet"""
    tweet = await use_cases.like_tweet(tweet_id)
    if not tweet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Tweet not found"
        )
    return TweetResponseDTO.model_validate(tweet)


@router.post("/{tweet_id}/unlike", response_model=TweetResponseDTO)
async def unlike_tweet(
    tweet_id: UUID, use_cases: TweetUseCases = Depends(get_tweet_use_cases)
):
    """Unlike a tweet"""
    tweet = await use_cases.unlike_tweet(tweet_id)
    if not tweet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Tweet not found"
        )
    return TweetResponseDTO.model_validate(tweet)


@router.post("/{tweet_id}/retweet", response_model=TweetResponseDTO)
async def retweet(
    tweet_id: UUID, use_cases: TweetUseCases = Depends(get_tweet_use_cases)
):
    """Retweet a tweet"""
    tweet = await use_cases.retweet(tweet_id)
    if not tweet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Tweet not found"
        )
    return TweetResponseDTO.model_validate(tweet)
