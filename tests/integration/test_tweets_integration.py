from httpx import AsyncClient
import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.fake_twitter.infrastructure.database.models import TweetModel


@pytest.mark.asyncio(loop_scope="session")
async def test_create_tweet_and_verify_in_db(
    client: AsyncClient,
    db_session: AsyncSession,
    sample_user_data,
    sample_tweet_data,
):
    """Test creating a tweet via API and verify it's in the database"""
    # Create user first
    user_response = await client.post("/api/v1/users/", json=sample_user_data)
    user_id = user_response.json()["id"]

    # Create tweet via API
    tweet_data = sample_tweet_data.copy()
    tweet_data["user_id"] = user_id
    response = await client.post("/api/v1/tweets/", json=tweet_data)

    assert response.status_code == 201
    data = response.json()
    tweet_id = data["id"]

    # Verify in database
    await db_session.commit()
    result = await db_session.execute(
        select(TweetModel).where(TweetModel.id == tweet_id)
    )
    db_tweet = result.scalar_one_or_none()

    assert db_tweet is not None
    assert db_tweet.content == sample_tweet_data["content"]
    assert str(db_tweet.user_id) == user_id
    assert db_tweet.likes_count == 0
    assert db_tweet.retweets_count == 0


@pytest.mark.asyncio(loop_scope="session")
async def test_get_tweet_by_id(
    client: AsyncClient,
    db_session: AsyncSession,
    sample_user_data,
    sample_tweet_data,
):
    """Test getting a tweet by ID"""
    # Create user and tweet
    user_response = await client.post("/api/v1/users/", json=sample_user_data)
    user_id = user_response.json()["id"]

    tweet_data = sample_tweet_data.copy()
    tweet_data["user_id"] = user_id
    create_response = await client.post("/api/v1/tweets/", json=tweet_data)
    tweet_id = create_response.json()["id"]

    # Get tweet via API
    response = await client.get(f"/api/v1/tweets/{tweet_id}")

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == tweet_id
    assert data["content"] == sample_tweet_data["content"]


@pytest.mark.asyncio(loop_scope="session")
async def test_update_tweet_and_verify_in_db(
    client: AsyncClient,
    db_session: AsyncSession,
    sample_user_data,
    sample_tweet_data,
):
    """Test updating a tweet via API and verify changes in database"""
    # Create user and tweet
    user_response = await client.post("/api/v1/users/", json=sample_user_data)
    user_id = user_response.json()["id"]

    tweet_data = sample_tweet_data.copy()
    tweet_data["user_id"] = user_id
    create_response = await client.post("/api/v1/tweets/", json=tweet_data)
    tweet_id = create_response.json()["id"]

    # Update tweet via API
    update_data = {"content": "Updated tweet content!"}
    response = await client.put(f"/api/v1/tweets/{tweet_id}", json=update_data)

    assert response.status_code == 200

    # Verify in database
    await db_session.commit()
    result = await db_session.execute(
        select(TweetModel).where(TweetModel.id == tweet_id)
    )
    db_tweet = result.scalar_one_or_none()

    assert db_tweet is not None
    assert db_tweet.content == update_data["content"]


@pytest.mark.asyncio(loop_scope="session")
async def test_delete_tweet_and_verify_in_db(
    client: AsyncClient,
    db_session: AsyncSession,
    sample_user_data,
    sample_tweet_data,
):
    """Test deleting a tweet via API and verify it's removed from database"""
    # Create user and tweet
    user_response = await client.post("/api/v1/users/", json=sample_user_data)
    user_id = user_response.json()["id"]

    tweet_data = sample_tweet_data.copy()
    tweet_data["user_id"] = user_id
    create_response = await client.post("/api/v1/tweets/", json=tweet_data)
    tweet_id = create_response.json()["id"]

    # Delete tweet via API
    response = await client.delete(f"/api/v1/tweets/{tweet_id}")

    assert response.status_code == 204

    # Verify not in database
    await db_session.commit()
    result = await db_session.execute(
        select(TweetModel).where(TweetModel.id == tweet_id)
    )
    db_tweet = result.scalar_one_or_none()

    assert db_tweet is None


@pytest.mark.asyncio(loop_scope="session")
async def test_like_tweet_and_verify_count_in_db(
    client: AsyncClient,
    db_session: AsyncSession,
    sample_user_data,
    sample_tweet_data,
):
    """Test liking a tweet and verify like count in database"""
    # Create user and tweet
    user_response = await client.post("/api/v1/users/", json=sample_user_data)
    user_id = user_response.json()["id"]

    tweet_data = sample_tweet_data.copy()
    tweet_data["user_id"] = user_id
    create_response = await client.post("/api/v1/tweets/", json=tweet_data)
    tweet_id = create_response.json()["id"]

    # Like tweet via API
    response = await client.post(f"/api/v1/tweets/{tweet_id}/like")

    assert response.status_code == 200
    data = response.json()
    assert data["likes_count"] == 1

    # Verify in database
    await db_session.commit()
    result = await db_session.execute(
        select(TweetModel).where(TweetModel.id == tweet_id)
    )
    db_tweet = result.scalar_one_or_none()

    assert db_tweet is not None
    assert db_tweet.likes_count == 1


@pytest.mark.asyncio(loop_scope="session")
async def test_retweet_and_verify_count_in_db(
    client: AsyncClient,
    db_session: AsyncSession,
    sample_user_data,
    sample_tweet_data,
):
    """Test retweeting and verify retweet count in database"""
    # Create user and tweet
    user_response = await client.post("/api/v1/users/", json=sample_user_data)
    user_id = user_response.json()["id"]

    tweet_data = sample_tweet_data.copy()
    tweet_data["user_id"] = user_id
    create_response = await client.post("/api/v1/tweets/", json=tweet_data)
    tweet_id = create_response.json()["id"]

    # Retweet via API
    response = await client.post(f"/api/v1/tweets/{tweet_id}/retweet")

    assert response.status_code == 200
    data = response.json()
    assert data["retweets_count"] == 1

    # Verify in database
    await db_session.commit()
    result = await db_session.execute(
        select(TweetModel).where(TweetModel.id == tweet_id)
    )
    db_tweet = result.scalar_one_or_none()

    assert db_tweet is not None
    assert db_tweet.retweets_count == 1


@pytest.mark.asyncio(loop_scope="session")
async def test_get_tweets_by_user_and_verify_in_db(
    client: AsyncClient,
    db_session: AsyncSession,
    sample_user_data,
    sample_tweet_data,
):
    """Test getting tweets by user and verify count matches database"""
    # Create user
    user_response = await client.post("/api/v1/users/", json=sample_user_data)
    user_id = user_response.json()["id"]

    # Create multiple tweets
    tweet_ids = []
    for i in range(3):
        tweet_data = sample_tweet_data.copy()
        tweet_data["content"] = f"Tweet number {i}"
        tweet_data["user_id"] = user_id
        create_response = await client.post("/api/v1/tweets/", json=tweet_data)
        tweet_ids.append(create_response.json()["id"])

    # Get tweets by user via API
    response = await client.get(f"/api/v1/tweets/user/{user_id}")

    assert response.status_code == 200
    api_tweets = response.json()

    # Verify count in database
    await db_session.commit()
    result = await db_session.execute(
        select(TweetModel).where(TweetModel.user_id == user_id)
    )
    db_tweets = result.scalars().all()

    assert len(db_tweets) == 3
    assert len(api_tweets) == 3
