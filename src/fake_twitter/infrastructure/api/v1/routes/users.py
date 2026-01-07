from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from fake_twitter.application.use_cases.user_use_cases import UserUseCases
from fake_twitter.application.dtos.user_dtos import (
    UserCreateDTO,
    UserUpdateDTO,
    UserResponseDTO,
)
from fake_twitter.infrastructure.api.dependencies import get_user_use_cases


router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", response_model=UserResponseDTO, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_dto: UserCreateDTO, use_cases: UserUseCases = Depends(get_user_use_cases)
):
    """Create a new user"""
    user = await use_cases.create_user(user_dto)
    return UserResponseDTO.model_validate(user)


@router.get("/{user_id}", response_model=UserResponseDTO)
async def get_user(
    user_id: UUID, use_cases: UserUseCases = Depends(get_user_use_cases)
):
    """Get a user by ID"""
    user = await use_cases.get_user_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return UserResponseDTO.model_validate(user)


@router.get("/username/{username}", response_model=UserResponseDTO)
async def get_user_by_username(
    username: str, use_cases: UserUseCases = Depends(get_user_use_cases)
):
    """Get a user by username"""
    user = await use_cases.get_user_by_username(username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return UserResponseDTO.model_validate(user)


@router.get("/", response_model=List[UserResponseDTO])
async def get_all_users(
    skip: int = 0,
    limit: int = 100,
    use_cases: UserUseCases = Depends(get_user_use_cases),
):
    """Get all users with pagination"""
    users = await use_cases.get_all_users(skip, limit)
    return [UserResponseDTO.model_validate(user) for user in users]


@router.put("/{user_id}", response_model=UserResponseDTO)
async def update_user(
    user_id: UUID,
    user_dto: UserUpdateDTO,
    use_cases: UserUseCases = Depends(get_user_use_cases),
):
    """Update a user"""
    user = await use_cases.update_user(user_id, user_dto)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return UserResponseDTO.model_validate(user)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: UUID, use_cases: UserUseCases = Depends(get_user_use_cases)
):
    """Delete a user"""
    deleted = await use_cases.delete_user(user_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )


@router.post("/{user_id}/follow", response_model=UserResponseDTO)
async def follow_user(
    user_id: UUID, use_cases: UserUseCases = Depends(get_user_use_cases)
):
    """Follow a user"""
    user = await use_cases.follow_user(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return UserResponseDTO.model_validate(user)


@router.post("/{user_id}/unfollow", response_model=UserResponseDTO)
async def unfollow_user(
    user_id: UUID, use_cases: UserUseCases = Depends(get_user_use_cases)
):
    """Unfollow a user"""
    user = await use_cases.unfollow_user(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return UserResponseDTO.model_validate(user)
