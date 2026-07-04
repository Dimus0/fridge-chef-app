# tests/conftest.py
import asyncio
from typing import AsyncGenerator
import uuid

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy import delete
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from ..app import app
from app.db.database import Base, get_async_session
from app.models.user import User
from app.routers.auth import get_current_user_dependency

# 1. Створюємо ізольований SQL-рушій для тестів в оперативній пам'яті (SQLite Async)
# Це набагато швидше, ніж щоразу піднімати важкий Postgres під час тестів
DATABASE_URL = "sqlite+aiosqlite:///:memory:"

engine = create_async_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool, # Гарантує, що всі з'єднання використовують одну базу в пам'яті
)

TestingSessionLocal = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

# 2. Фікстура, яка створює таблиці перед тестами та видаляє після їх завершення
@pytest.fixture(autouse=True, scope="session")
async def prepare_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

# 3. Перевизначаємо залежність сесії БД у FastAPI на нашу тестову сесію
@pytest.fixture
async def override_get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with TestingSessionLocal() as session:
        yield session


async def override_current_user() -> User:
    return User(
        id=uuid.uuid4(),
        username="test-user",
        email="test@example.com",
        password="hashed",
        is_active=True,
        is_superuser=True,
    )

# Замінюємо оригінальну сесію на тестову всередині FastAPI додатка
app.dependency_overrides[get_async_session] = override_get_async_session
app.dependency_overrides[get_current_user_dependency] = override_current_user


@pytest.fixture(autouse=True)
async def clear_data() -> AsyncGenerator[None, None]:
    async with engine.begin() as conn:
        for table in reversed(Base.metadata.sorted_tables):
            await conn.execute(delete(table))
    yield

# 4. Спеціальне налаштування для роботи асинхронного pytest з циклами подій
@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

# 5. ГОЛОВНА ФІКСТУРА: Асинхронний клієнт для надсилання HTTP-запитів до роутів
@pytest.fixture
async def ac() -> AsyncGenerator[AsyncClient, None]:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client