from unittest.mock import patch

from fastapi.testclient import TestClient

from backend.app.main import app


client = TestClient(app)


@patch("backend.app.api.router.ResourceService")
def test_ec2_resources(mock_resource_service):
    mock_service = mock_resource_service.return_value

    mock_service.get_ec2_instances.return_value = [
        {
            "instance_id": "i-1234567890abcdef0",
            "instance_type": "t3.micro",
            "state": "running",
            "private_ip": "10.0.1.10",
            "public_ip": "203.0.113.10",
        }
    ]

    response = client.get("/api/v1/resources/ec2")

    assert response.status_code == 200
    assert response.json() == {
        "resources": [
            {
                "instance_id": "i-1234567890abcdef0",
                "instance_type": "t3.micro",
                "state": "running",
                "private_ip": "10.0.1.10",
                "public_ip": "203.0.113.10",
            }
        ]
    }

    mock_service.get_ec2_instances.assert_called_once()


@patch("backend.app.api.router.ResourceService")
def test_s3_resources(mock_resource_service):
    mock_service = mock_resource_service.return_value

    mock_service.get_s3_buckets.return_value = [
        {
            "name": "securesync-iot-387512137867",
            "creation_date": "2026-08-20T12:04:00+00:00",
        }
    ]

    response = client.get("/api/v1/resources/s3")

    assert response.status_code == 200
    assert response.json() == {
        "resources": [
            {
                "name": "securesync-iot-387512137867",
                "creation_date": "2026-08-20T12:04:00+00:00",
            }
        ]
    }

    mock_service.get_s3_buckets.assert_called_once()
