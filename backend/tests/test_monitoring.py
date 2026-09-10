from unittest.mock import patch

from fastapi.testclient import TestClient

from backend.app.main import app


client = TestClient(app)


@patch("backend.app.api.router.get_monitoring_data")
def test_monitoring(mock_get_monitoring_data):
    mock_get_monitoring_data.return_value = {
        "ec2": [],
        "s3": [
            {
                "name": "test-bucket",
                "creation_date": "2026-01-01T00:00:00+00:00",
            }
        ],
        "rds": [],
    }

    response = client.get("/api/v1/monitoring")

    assert response.status_code == 200
    assert response.json() == {
        "ec2": [],
        "s3": [
            {
                "name": "test-bucket",
                "creation_date": "2026-01-01T00:00:00+00:00",
            }
        ],
        "rds": [],
    }

    mock_get_monitoring_data.assert_called_once()
