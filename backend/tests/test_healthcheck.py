"""Test for health check endpoint."""

from http import HTTPStatus

from starlette.testclient import TestClient


def test_healthcheck(client: TestClient) -> None:
    """Test the healthcheck endpoint."""
    response = client.get('/api/healthcheck')
    assert response.status_code == HTTPStatus.OK
