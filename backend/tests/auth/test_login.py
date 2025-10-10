"""/api/auth/login."""

from http import HTTPStatus

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_login_success(client: AsyncClient) -> None:
    """Successful authentication of an existing user."""
    await client.post(
        '/api/auth/register',
        json={'username': 'login_user', 'password': 'qwerty', 'confirm_password': 'qwerty'},
    )

    response = await client.post(
        '/api/auth/login',
        json={'username': 'login_user', 'password': 'qwerty'},
    )

    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert 'access_token' in data
    assert 'refresh_token' in data


@pytest.mark.asyncio
async def test_login_wrong_password(client: AsyncClient) -> None:
    """Attempt to log in with an incorrect password."""
    await client.post(
        '/api/auth/register',
        json={'username': 'wrongpass', 'password': 'right', 'confirm_password': 'right'},
    )

    response = await client.post(
        '/api/auth/login',
        json={'username': 'wrongpass', 'password': 'WRONG'},
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json()['detail'] == 'Wrong Password'


@pytest.mark.asyncio
async def test_login_nonexistent_user(client: AsyncClient) -> None:
    """Attempt to log in with a non-existent username."""
    response = await client.post(
        '/api/auth/login',
        json={'username': 'ghost_user', 'password': '123'},
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json()['detail'] == 'User does not exist'
