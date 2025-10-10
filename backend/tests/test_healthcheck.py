"""Test for health check endpoint."""

from http import HTTPStatus

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_healthcheck(client: AsyncClient) -> None:
    """Test the healthcheck endpoint."""
    response = await client.get('/api/healthcheck')
    assert response.status_code == HTTPStatus.OK
