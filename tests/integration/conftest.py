import pytest
from typing import AsyncGenerator
from testcontainers.postgres import PostgresContainer
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
    async_sessionmaker,
    AsyncEngine,
)
from httpx import ASGITransport, AsyncClient

from src.fake_twitter.main import create_app
from src.fake_twitter.infrastructure.database.connection import Base, get_db


@pytest.fixture(scope="session")
async def postgres_container() -> AsyncGenerator[PostgresContainer, None]:
    """Start a PostgreSQL container for testing"""
    with PostgresContainer("postgres:16-alpine", driver="asyncpg") as postgres:
        yield postgres


@pytest.fixture(scope="session")
async def test_database_url(postgres_container: PostgresContainer) -> str:
    """Get the database URL from the container"""
    return postgres_container.get_connection_url()


@pytest.fixture(scope="function")
async def test_engine(test_database_url: str) -> AsyncGenerator[AsyncEngine, None]:
    """Create a test database engine"""
    engine = create_async_engine(test_database_url, echo=True)

    # Create all tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield engine

    await engine.dispose()


@pytest.fixture
async def db_session(test_engine) -> AsyncGenerator[AsyncSession, None]:
    """Create a test database session for each test"""
    async_session_maker = async_sessionmaker(
        test_engine, class_=AsyncSession, expire_on_commit=False
    )

    async with async_session_maker() as session:
        yield session


@pytest.fixture
async def client(db_session: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    """Create a test client with database override"""
    app = create_app()

    # Override the database dependency to use test database
    async def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        yield ac

    app.dependency_overrides.clear()


@pytest.fixture
async def sample_user_data():
    """Sample user data for tests"""
    import uuid

    unique_id = str(uuid.uuid4())[:8]
    return {
        "username": f"testuser_{unique_id}",
        "email": f"test_{unique_id}@example.com",
        "full_name": "Test User",
        "bio": "This is a test user",
    }


@pytest.fixture
async def sample_tweet_data():
    """Sample tweet data for tests"""
    return {"content": "This is a test tweet!"}
