"""Pytest fixtures for testing the FastAPI application.

Provides a `TestClient` instance used to send HTTP requests
to the main FastAPI app during test execution.
"""

import pytest
from fastapi.testclient import TestClient

from src import app


@pytest.fixture(scope='session')
def client() -> TestClient:
    """Fixture that returns a FastAPI TestClient instance."""
    return TestClient(app)
