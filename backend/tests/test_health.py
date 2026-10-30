from fastapi.testclient import TestClient

from backend.app.main import app


client = TestClient(app)


def test_health_check():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_cors_allows_local_frontend_origin():
    response = client.get(
        "/health",
        headers={"Origin": "http://127.0.0.1:5500"},
    )

    assert response.status_code == 200
    assert response.headers["access-control-allow-origin"] == (
        "http://127.0.0.1:5500"
    )


def test_cors_rejects_unconfigured_origin():
    response = client.get(
        "/health",
        headers={"Origin": "http://example.com"},
    )

    assert response.status_code == 200
    assert "access-control-allow-origin" not in response.headers
