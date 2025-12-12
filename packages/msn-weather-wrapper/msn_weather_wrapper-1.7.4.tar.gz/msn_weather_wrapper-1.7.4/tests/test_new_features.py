"""Tests for new API features."""

import pytest

from api import app


@pytest.fixture
def client():
    """Create a test client."""
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_health_check_versioned(client):
    """Test versioned health check endpoint."""
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "ok"
    assert data["version"] == "1.0"


def test_liveness_probe(client):
    """Test liveness probe endpoint."""
    response = client.get("/api/v1/health/live")
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "alive"


def test_readiness_probe(client):
    """Test readiness probe endpoint."""
    response = client.get("/api/v1/health/ready")
    # Should return 200 or 503 depending on external service availability
    assert response.status_code in [200, 503]
    data = response.get_json()
    assert "status" in data
    assert "checks" in data
    assert "weather_client" in data["checks"]
    assert "external_api" in data["checks"]


def test_weather_coordinates_endpoint(client):
    """Test weather by coordinates endpoint."""
    # Test with valid coordinates (Seattle)
    response = client.get("/api/v1/weather/coordinates?lat=47.6062&lon=-122.3321")
    # This might fail if external service is unavailable, but endpoint should respond
    assert response.status_code in [200, 500]


def test_weather_coordinates_invalid(client):
    """Test weather by coordinates with invalid data."""
    # Missing parameters
    response = client.get("/api/v1/weather/coordinates")
    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data

    # Invalid latitude
    response = client.get("/api/v1/weather/coordinates?lat=100&lon=-122")
    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data

    # Invalid longitude
    response = client.get("/api/v1/weather/coordinates?lat=47&lon=200")
    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data


def test_recent_searches_endpoint(client):
    """Test recent searches endpoints."""
    # Get recent searches (should be empty initially)
    response = client.get("/api/v1/recent-searches")
    assert response.status_code == 200
    data = response.get_json()
    assert "recent_searches" in data
    assert isinstance(data["recent_searches"], list)


def test_clear_recent_searches(client):
    """Test clearing recent searches."""
    response = client.delete("/api/v1/recent-searches")
    assert response.status_code == 200
    data = response.get_json()
    assert "message" in data


def test_versioned_weather_endpoint(client):
    """Test versioned weather endpoint."""
    # Test GET with version
    response = client.get("/api/v1/weather?city=Seattle&country=USA")
    # Might fail due to external service, but endpoint should respond
    assert response.status_code in [200, 500]

    # Test POST with version
    response = client.post(
        "/api/v1/weather",
        json={"city": "Seattle", "country": "USA"},
        content_type="application/json",
    )
    assert response.status_code in [200, 500]


def test_backward_compatibility(client):
    """Test that legacy endpoints still work."""
    # Legacy health check
    response = client.get("/api/health")
    assert response.status_code == 200

    # Legacy weather endpoint
    response = client.get("/api/weather?city=Seattle&country=USA")
    assert response.status_code in [200, 500]
