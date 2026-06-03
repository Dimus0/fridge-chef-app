from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine,async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from datetime import datetime, timezone
from urllib.parse import quote_plus

password = "password"
encoded_password  = quote_plus(password)

DATABASE_NAME = "fridgechef_db"
DATABASE_URL = f"postgresql+asyncpg://postgres:{encoded_password}@localhost:5432/{DATABASE_NAME}"

engine = create_async_engine(DATABASE_URL, echo=True)
async_session = async_sessionmaker(engine, expire_on_commit=False)

class Base(DeclarativeBase): pass

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

async def create_db_tables():
    from app.models import recipe,user

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session