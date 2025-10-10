"""Pytest fixtures for testing the FastAPI application with an async test database."""

from collections.abc import AsyncGenerator
from typing import Any

import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from src.config import settings
from src.database import get_db
from src.main import app
from src.models.base import Base

# ---------------------------------------------------------------------
# Use a dedicated test database (can be overridden via environment vars)
# ---------------------------------------------------------------------
TEST_DATABASE_URL = settings.database_url + '_test'


# ---------------------------------------------------------------------
# Async SQLAlchemy engine + schema setup/teardown
# ---------------------------------------------------------------------
@pytest_asyncio.fixture(scope='session')
async def test_engine() -> AsyncGenerator[AsyncEngine, None]:
    """Create a temporary async SQLAlchemy engine for testing."""
    engine = create_async_engine(TEST_DATABASE_URL, echo=False, poolclass=NullPool)

    # Create all tables before the test session starts
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield engine

    # Drop all tables after the test session finishes
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await engine.dispose()


# ---------------------------------------------------------------------
# Async session per test
# ---------------------------------------------------------------------
@pytest_asyncio.fixture()
async def db_session(test_engine: AsyncEngine) -> AsyncGenerator[AsyncSession, None]:
    """Provide a transactional scope around a series of operations."""
    async_session = async_sessionmaker(
        bind=test_engine,
        expire_on_commit=False,
        class_=AsyncSession,
    )
    async with async_session() as session:
        yield session


# ---------------------------------------------------------------------
# Override FastAPI dependency
# ---------------------------------------------------------------------
@pytest_asyncio.fixture()
async def override_get_db(db_session: AsyncSession) -> AsyncGenerator[None, None]:
    """Override FastAPI's get_db dependency with the async test session."""

    async def _get_db() -> AsyncGenerator[AsyncSession, None]:
        yield db_session

    app.dependency_overrides[get_db] = _get_db
    yield
    app.dependency_overrides.clear()


# ---------------------------------------------------------------------
# HTTPX AsyncClient fixture
# ---------------------------------------------------------------------
@pytest_asyncio.fixture()
async def client(override_get_db: Any) -> AsyncGenerator[AsyncClient, None]:  # noqa
    """Create an AsyncClient using FastAPI's ASGITransport."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url='http://test') as ac:
        yield ac
