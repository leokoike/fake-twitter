from sqlalchemy import String, Integer, DateTime, Text, UUID
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
import uuid

from src.fake_twitter.infrastructure.database.connection import Base


class UserModel(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(UUID(), primary_key=True, default=uuid.uuid4)
    username: Mapped[str] = mapped_column(
        String(50), unique=True, nullable=False, index=True
    )
    email: Mapped[str] = mapped_column(
        String(100), unique=True, nullable=False, index=True
    )
    full_name: Mapped[str] = mapped_column(String(100), nullable=False)
    bio: Mapped[str] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now, nullable=False
    )
    followers_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    following_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)


class TweetModel(Base):
    __tablename__ = "tweets"

    id: Mapped[uuid.UUID] = mapped_column(UUID(), primary_key=True, default=uuid.uuid4)
    content: Mapped[str] = mapped_column(String(280), nullable=False)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(), nullable=False, index=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now, nullable=False
    )
    likes_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    retweets_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
