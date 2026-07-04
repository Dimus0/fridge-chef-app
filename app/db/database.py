from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine,async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from urllib.parse import quote_plus
from app.config import settings

# password = "password"
# encoded_password  = quote_plus(password)

# DATABASE_NAME = "fridgechef_db"
# DATABASE_URL = f"postgresql+asyncpg://postgres:{encoded_password}@localhost:5432/{DATABASE_NAME}"

engine = create_async_engine(settings.async_database_url, echo=True)
async_session = async_sessionmaker(engine, expire_on_commit=False)

class Base(DeclarativeBase): pass

async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session