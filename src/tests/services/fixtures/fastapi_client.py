"""Contains fixture for FastAPI client."""

import pytest
from app import app
from fastapi.testclient import TestClient


@pytest.fixture(scope="package")
def fastapi_client() -> TestClient:
    """Use this test client to test your FastAPI endpoints."""
    return TestClient(app)
