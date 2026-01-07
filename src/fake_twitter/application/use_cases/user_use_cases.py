from typing import List, Optional
from uuid import UUID

from fake_twitter.domain.entities.user import User
from fake_twitter.domain.repositories.user_repository import UserRepository
from fake_twitter.application.dtos.user_dtos import UserCreateDTO, UserUpdateDTO


class UserUseCases:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def create_user(self, user_dto: UserCreateDTO) -> User:
        user = User(
            username=user_dto.username,
            email=user_dto.email,
            full_name=user_dto.full_name,
            bio=user_dto.bio,
        )
        return await self.user_repository.create(user)

    async def get_user_by_id(self, user_id: UUID) -> Optional[User]:
        return await self.user_repository.get_by_id(user_id)

    async def get_user_by_username(self, username: str) -> Optional[User]:
        return await self.user_repository.get_by_username(username)

    async def get_all_users(self, skip: int = 0, limit: int = 100) -> List[User]:
        return await self.user_repository.get_all(skip, limit)

    async def update_user(self, user_id: UUID, user_dto: UserUpdateDTO) -> Optional[User]:
        user = await self.user_repository.get_by_id(user_id)
        if not user:
            return None
        
        if user_dto.full_name is not None:
            user.full_name = user_dto.full_name
        if user_dto.bio is not None:
            user.bio = user_dto.bio
        
        return await self.user_repository.update(user)

    async def delete_user(self, user_id: UUID) -> bool:
        return await self.user_repository.delete(user_id)

    async def follow_user(self, user_id: UUID) -> Optional[User]:
        user = await self.user_repository.get_by_id(user_id)
        if not user:
            return None
        
        user.follow()
        return await self.user_repository.update(user)

    async def unfollow_user(self, user_id: UUID) -> Optional[User]:
        user = await self.user_repository.get_by_id(user_id)
        if not user:
            return None
        
        user.unfollow()
        return await self.user_repository.update(user)
