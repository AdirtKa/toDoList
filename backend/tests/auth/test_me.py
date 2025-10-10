"""/api/auth/me."""

from http import HTTPStatus

import pytest
from httpx import AsyncClient
from starlette.testclient import TestClient


@pytest.mark.asyncio
async def test_me_authenticated(client: AsyncClient) -> None:
    """Verify /me returns the correct user after successful registration."""
    register_resp = await client.post(
        '/api/auth/register',
        json={'username': 'me_user', 'password': 'abc123', 'confirm_password': 'abc123'},
    )
    assert register_resp.status_code == HTTPStatus.OK

    response = await client.get('/api/auth/me')
    assert response.status_code == HTTPStatus.OK

    data = response.json()
    assert data['username'] == 'me_user'


@pytest.mark.asyncio
async def test_me_unauthorized(client: AsyncClient) -> None:
    """Access without a valid token should return 401 Unauthorized."""
    from src.main import app  # noqa

    with TestClient(app) as new_client:
        response = new_client.get('/api/auth/me')

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert 'credentials' in response.json()['detail'].lower()
