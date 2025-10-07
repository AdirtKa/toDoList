"""Tests verifying that the database schema is properly initialized."""

import pytest
from httpx import AsyncClient
from sqlalchemy import text


@pytest.mark.asyncio
async def test_database_alive(client: AsyncClient) -> None:
    """Ensure that the 'user' table exists in the public schema."""
    from src.database import SessionLocal  # noqa

    async with SessionLocal() as session:
        result = await session.execute(
            text("SELECT table_name FROM information_schema.tables WHERE table_schema='public';")
        )
        tables = [row[0] for row in result.fetchall()]
        print('📋 Tables:', tables)

        assert 'user' in tables, "The 'user' table was not found in the public schema."
