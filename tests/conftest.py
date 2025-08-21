from unittest.mock import AsyncMock

import pytest
import pytest_asyncio

from fastapi import FastAPI
from httpx import AsyncClient, ASGITransport
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from src.infrastructure.persistence.sqlalchemy.models import TaskORM
from src.main import app
from src.infrastructure.database.connection import Base
from src.infrastructure.database.dependencies import get_db_session

TEST_DATABASE_URL = 'sqlite+aiosqlite:///:memory:'


@pytest_asyncio.fixture(scope='session')
async def test_engine():
    """Создаёт асинхронный движок для тестовой SQLite-базы."""
    engine = create_async_engine(TEST_DATABASE_URL, echo=False, future=True)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    try:
        yield engine
    finally:
        await engine.dispose()


@pytest_asyncio.fixture(scope='session')
async def async_sessionmaker(test_engine):
    """Возвращает асинхронный sessionmaker для тестовой БД."""
    return sessionmaker(test_engine, class_=AsyncSession, expire_on_commit=False)


@pytest_asyncio.fixture(scope='session')
async def app_test(async_sessionmaker):
    """Создаёт тестовое FastAPI-приложение с подменённой зависимостью get_db_session."""
    async def _get_db_session():
        async with async_sessionmaker() as session:
            try:
                yield session
            finally:
                await session.rollback()

    app.dependency_overrides[get_db_session] = _get_db_session
    yield app
    app.dependency_overrides.clear()


@pytest_asyncio.fixture
async def client(app_test: FastAPI):
    """Возвращает асинхронного тестового клиента для FastAPI-приложения."""
    transport = ASGITransport(app=app_test)
    async with AsyncClient(transport=transport, base_url='http://testserver') as c:
        yield c


@pytest_asyncio.fixture(autouse=True)
async def clear_tasks_table(async_sessionmaker):
    """Очищает таблицу задач перед каждым тестом."""
    async with async_sessionmaker() as session:
        await session.execute(delete(TaskORM))
        await session.commit()


@pytest.fixture
def mock_repo():
    """Возвращает асинхронный мок-репозиторий для юнит-тестов."""
    return AsyncMock()
