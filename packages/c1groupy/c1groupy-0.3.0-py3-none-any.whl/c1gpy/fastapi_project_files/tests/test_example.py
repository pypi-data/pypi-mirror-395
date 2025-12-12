from fastapi.testclient import TestClient

from api_interface import rest_api

client = TestClient(rest_api)


def test_root():
    """Test root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()


def test_health_check():
    """Test health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_router1_example():
    """Test router1 example endpoint."""
    response = client.get("/router1/example")
    assert response.status_code == 200
    assert response.json()["status"] == "success"


def test_router2_status():
    """Test router2 status endpoint."""
    response = client.get("/router2/status")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
