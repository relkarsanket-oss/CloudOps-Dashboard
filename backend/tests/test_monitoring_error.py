from unittest.mock import patch

from fastapi.testclient import TestClient

from backend.app.main import app


client = TestClient(app)


@patch("backend.app.api.router.get_monitoring_data")
def test_monitoring_error(mock_get_monitoring_data):
    mock_get_monitoring_data.side_effect = Exception("AWS service unavailable")

    response = client.get("/api/v1/monitoring")

    assert response.status_code == 200
    assert response.json() == {
        "status": "error",
        "message": "Unable to retrieve monitoring data",
    }

    mock_get_monitoring_data.assert_called_once()
