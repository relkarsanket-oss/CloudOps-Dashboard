from unittest.mock import MagicMock, patch

from fastapi.testclient import TestClient

from backend.app.main import app


client = TestClient(app)


@patch("backend.app.api.router.get_sts_client")
def test_aws_status(mock_get_sts_client):
    mock_sts_client = MagicMock()

    mock_sts_client.get_caller_identity.return_value = {
        "Account": "123456789012",
        "Arn": "arn:aws:iam::123456789012:user/test-user",
    }

    mock_get_sts_client.return_value = mock_sts_client

    response = client.get("/api/v1/aws/status")

    assert response.status_code == 200
    assert response.json() == {
        "service": "AWS",
        "status": "connected",
        "account_id": "123456789012",
        "arn": "arn:aws:iam::123456789012:user/test-user",
    }

    mock_sts_client.get_caller_identity.assert_called_once()
