from typing import Optional, List
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.fake_twitter.domain.entities.user import User
from src.fake_twitter.domain.repositories.user_repository import UserRepository
from src.fake_twitter.infrastructure.database.models import UserModel


class SQLAlchemyUserRepository(UserRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, user: User) -> User:
        user_model = UserModel(**user.model_dump())
        self.session.add(user_model)
        await self.session.flush()
        await self.session.refresh(user_model)
        return User.model_validate(user_model)

    async def get_by_id(self, user_id: UUID) -> Optional[User]:
        result = await self.session.execute(
            select(UserModel).where(UserModel.id == user_id)
        )
        user_model = result.scalar_one_or_none()
        return User.model_validate(user_model) if user_model else None

    async def get_by_username(self, username: str) -> Optional[User]:
        result = await self.session.execute(
            select(UserModel).where(UserModel.username == username)
        )
        user_model = result.scalar_one_or_none()
        return User.model_validate(user_model) if user_model else None

    async def get_all(self, skip: int = 0, limit: int = 100) -> List[User]:
        result = await self.session.execute(select(UserModel).offset(skip).limit(limit))
        user_models = result.scalars().all()
        return [User.model_validate(user_model) for user_model in user_models]

    async def update(self, user: User) -> User:
        result = await self.session.execute(
            select(UserModel).where(UserModel.id == user.id)
        )
        user_model = result.scalar_one_or_none()
        if user_model:
            for key, value in user.model_dump().items():
                setattr(user_model, key, value)
            await self.session.flush()
            await self.session.refresh(user_model)
            return User.model_validate(user_model)
        raise ValueError(f"User with id {user.id} not found")

    async def delete(self, user_id: UUID) -> bool:
        result = await self.session.execute(
            select(UserModel).where(UserModel.id == user_id)
        )
        user_model = result.scalar_one_or_none()
        if user_model:
            await self.session.delete(user_model)
            await self.session.flush()
            return True
        return False
