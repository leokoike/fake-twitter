from fastapi import APIRouter
from .routes import router as routes_router

router = APIRouter(prefix="/v1")
router.include_router(routes_router)

__all__ = ["router"]
