from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from fake_twitter.infrastructure.api import router as api_router


def create_app() -> FastAPI:
    app = FastAPI(
        title="Fake Twitter API",
        description="A Twitter-like API built with FastAPI and DDD architecture",
        version="1.0.0",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(api_router)

    @app.get("/")
    async def root():
        return {
            "message": "Welcome to Fake Twitter API",
            "docs": "/docs",
            "redoc": "/redoc",
        }

    @app.get("/health")
    async def health():
        return {"status": "healthy"}

    return app


app = create_app()
