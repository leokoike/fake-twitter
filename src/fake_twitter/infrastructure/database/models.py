from sqlalchemy import Column, String, Integer, DateTime, Text
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from datetime import datetime
import uuid

from fake_twitter.infrastructure.database.connection import Base


class UserModel(Base):
    __tablename__ = "users"

    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(100), unique=True, nullable=False, index=True)
    full_name = Column(String(100), nullable=False)
    bio = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    followers_count = Column(Integer, default=0, nullable=False)
    following_count = Column(Integer, default=0, nullable=False)


class TweetModel(Base):
    __tablename__ = "tweets"

    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    content = Column(String(280), nullable=False)
    user_id = Column(PG_UUID(as_uuid=True), nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    likes_count = Column(Integer, default=0, nullable=False)
    retweets_count = Column(Integer, default=0, nullable=False)
