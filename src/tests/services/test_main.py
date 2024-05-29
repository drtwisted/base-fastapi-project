"""Contains tests for main services router."""

from fastapi.testclient import TestClient

from tests.services.fixtures.fastapi_client import fastapi_client


def test_main_get(fastapi_client: TestClient) -> None:
    response = fastapi_client.get("/main")

    assert response.status_code == 200
    assert response.json() == {"ok": True}


def test_root_get(fastapi_client: TestClient) -> None:
    response = fastapi_client.get("/")

    assert response.status_code == 404
