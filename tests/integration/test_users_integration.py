from httpx import AsyncClient
import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.fake_twitter.infrastructure.database.models import UserModel


@pytest.mark.asyncio(loop_scope="session")
async def test_create_user_and_verify_in_db(
    client: AsyncClient,
    db_session: AsyncSession,
    sample_user_data,
):
    """Test creating a user via API and verify it's in the database"""
    # Create user via API
    response = await client.post("/api/v1/users/", json=sample_user_data)

    assert response.status_code == 201
    data = response.json()
    user_id = data["id"]

    # Verify in database
    result = await db_session.execute(select(UserModel).where(UserModel.id == user_id))
    db_user = result.scalar_one_or_none()

    assert db_user is not None
    assert db_user.username == sample_user_data["username"]
    assert db_user.email == sample_user_data["email"]
    assert db_user.full_name == sample_user_data["full_name"]
    assert db_user.bio == sample_user_data["bio"]
    assert db_user.followers_count == 0
    assert db_user.following_count == 0


@pytest.mark.asyncio(loop_scope="session")
async def test_get_user_by_id(
    client: AsyncClient,
    db_session: AsyncSession,
    sample_user_data,
):
    """Test getting a user by ID"""
    # Create user
    create_response = await client.post("/api/v1/users/", json=sample_user_data)
    user_id = create_response.json()["id"]

    # Get user via API
    response = await client.get(f"/api/v1/users/{user_id}")

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == user_id
    assert data["username"] == sample_user_data["username"]


@pytest.mark.asyncio(loop_scope="session")
async def test_update_user_and_verify_in_db(
    client: AsyncClient,
    db_session: AsyncSession,
    sample_user_data,
):
    """Test updating a user via API and verify changes in database"""
    # Create user
    create_response = await client.post("/api/v1/users/", json=sample_user_data)
    user_id = create_response.json()["id"]

    # Update user via API
    update_data = {"full_name": "Updated Name", "bio": "Updated bio"}
    response = await client.put(f"/api/v1/users/{user_id}", json=update_data)

    assert response.status_code == 200

    # Verify in database
    await db_session.commit()  # Commit to see changes
    result = await db_session.execute(select(UserModel).where(UserModel.id == user_id))
    db_user = result.scalar_one_or_none()

    assert db_user is not None
    assert db_user.full_name == update_data["full_name"]
    assert db_user.bio == update_data["bio"]
    assert db_user.username == sample_user_data["username"]  # Unchanged


@pytest.mark.asyncio(loop_scope="session")
async def test_delete_user_and_verify_in_db(
    client: AsyncClient,
    db_session: AsyncSession,
    sample_user_data,
):
    """Test deleting a user via API and verify it's removed from database"""
    # Create user
    create_response = await client.post("/api/v1/users/", json=sample_user_data)
    user_id = create_response.json()["id"]

    # Delete user via API
    response = await client.delete(f"/api/v1/users/{user_id}")

    assert response.status_code == 204

    # Verify not in database
    await db_session.commit()  # Commit to see changes
    result = await db_session.execute(select(UserModel).where(UserModel.id == user_id))
    db_user = result.scalar_one_or_none()

    assert db_user is None


@pytest.mark.asyncio(loop_scope="session")
async def test_follow_user_and_verify_count_in_db(
    client: AsyncClient,
    db_session: AsyncSession,
    sample_user_data,
):
    """Test following a user and verify follower count in database"""
    # Create user
    create_response = await client.post("/api/v1/users/", json=sample_user_data)
    user_id = create_response.json()["id"]

    # Follow user via API
    response = await client.post(f"/api/v1/users/{user_id}/follow")

    assert response.status_code == 200
    data = response.json()
    assert data["followers_count"] == 1

    # Verify in database
    await db_session.commit()
    result = await db_session.execute(select(UserModel).where(UserModel.id == user_id))
    db_user = result.scalar_one_or_none()

    assert db_user is not None
    assert db_user.followers_count == 1


@pytest.mark.asyncio(loop_scope="session")
async def test_get_all_users_from_db(
    client: AsyncClient,
    db_session: AsyncSession,
    sample_user_data,
):
    """Test getting all users and verify count matches database"""
    # Create multiple users
    user_ids = []
    for i in range(3):
        user_data = sample_user_data.copy()
        user_data["username"] = f"{sample_user_data['username']}_{i}"
        user_data["email"] = f"{i}_{sample_user_data['email']}"
        create_response = await client.post("/api/v1/users/", json=user_data)
        user_ids.append(create_response.json()["id"])

    # Get all users via API
    response = await client.get("/api/v1/users/")

    assert response.status_code == 200
    api_users = response.json()

    # Verify count in database
    await db_session.commit()
    result = await db_session.execute(
        select(UserModel).where(UserModel.id.in_(user_ids))
    )
    db_users = result.scalars().all()

    assert len(db_users) == 3
    assert len(api_users) >= 3
