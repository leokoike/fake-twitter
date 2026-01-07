from fastapi import APIRouter
from .users import router as users_router
from .tweets import router as tweets_router

router = APIRouter()
router.include_router(users_router)
router.include_router(tweets_router)

__all__ = ["router"]
