"""Tests verifying that the database schema is properly initialized."""

import pytest
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession


@pytest.mark.asyncio
async def test_database_alive(db_session: AsyncSession) -> None:
    """Ensure that the 'user' table exists in the public schema."""
    result = await db_session.execute(
        text("SELECT table_name FROM information_schema.tables WHERE table_schema='public';")
    )
    tables = [row[0] for row in result.fetchall()]
    print('📋 Tables:', tables)

    assert 'user' in tables, "The 'user' table was not found in the public schema."
