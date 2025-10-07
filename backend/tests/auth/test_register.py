"""/api/auth/register."""

from http import HTTPStatus

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_register_success(client: AsyncClient) -> None:
    """Successful user registration should return JWT tokens."""
    response = await client.post(
        '/api/auth/register',
        json={
            'username': 'test_user',
            'password': '123456',
            'confirm_password': '123456',
        },
    )
    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert 'access_token' in data
    assert 'refresh_token' in data


@pytest.mark.asyncio
async def test_register_password_mismatch(client: AsyncClient) -> None:
    """Registration should fail if passwords do not match."""
    response = await client.post(
        '/api/auth/register',
        json={
            'username': 'mismatch_user',
            'password': '123',
            'confirm_password': '456',
        },
    )
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json()['detail'] == 'Passwords do not match'


@pytest.mark.asyncio
async def test_register_existing_user(client: AsyncClient) -> None:
    """Registration should fail if the username is already taken."""
    await client.post(
        '/api/auth/register',
        json={'username': 'dupe_user', 'password': 'pass', 'confirm_password': 'pass'},
    )

    response = await client.post(
        '/api/auth/register',
        json={'username': 'dupe_user', 'password': 'pass', 'confirm_password': 'pass'},
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json()['detail'] == 'Username already registered'
