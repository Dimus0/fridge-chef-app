from collections.abc import AsyncGenerator
import uuid

from sqlalchemy import Column, String,Text,DateTime,ForeignKey,Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine,async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, relationship
from datetime import datetime, timezone

# Change to PostgreSQL
DATABASE_URL = "sqlite+aiosqlite:///./test.db"

engine = create_async_engine(DATABASE_URL, echo=True)
async_session = async_sessionmaker(engine, expire_on_commit=False)

class Base(DeclarativeBase): pass


class Recipe(Base):
    __tablename__ = "Recipe"

    id = Column(UUID(as_uuid=True), primary_key=True,default=uuid.uuid4)
    user_id = Column(Integer)
    title = Column(String(244), nullable=False)
    ingredients = Column(String(), nullable=False)
    instruction = Column(String(), nullable=False)

    prep_time = Column(Integer())
    created_at = Column(String(),default=datetime.now(timezone.utc))

class User(Base):
    __tablename__ = "User"

    id = Column(UUID(as_uuid=True), primary_key=True,default=uuid.uuid4)
    username = Column(String(255),nullable=False)
    email = Column(String(255),nullable=False)
    password = Column(String(255),nullable=False)


async def create_db_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session