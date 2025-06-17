import pytest
from fastapi.testclient import TestClient
from condominio_api.main import app  # Adjusted import to match project structure


def test_health(client: TestClient):
    response = client.get("/health")
    # Check if the response status code is 200 and the response body is as expected
    # Adjust the expected response based on your actual health check implementation
    assert isinstance(response, TestClient)
    assert response is not None
    assert response.status_code == 200