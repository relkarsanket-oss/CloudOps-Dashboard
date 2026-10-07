from unittest.mock import MagicMock, patch

from fastapi.testclient import TestClient

from backend.app.main import app
from backend.app.services.resource_service import ResourceService


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
def test_rds_resources(mock_resource_service):
    mock_service = mock_resource_service.return_value

    mock_service.get_rds_instances.return_value = [
        {
            "db_instance_identifier": "cloudops-db",
            "engine": "postgres",
            "status": "available",
            "instance_class": "db.t3.micro",
            "endpoint": None,
        }
    ]

    response = client.get("/api/v1/resources/rds")

    assert response.status_code == 200
    assert response.json() == {
        "resources": [
            {
                "db_instance_identifier": "cloudops-db",
                "engine": "postgres",
                "status": "available",
                "instance_class": "db.t3.micro",
                "endpoint": None,
            }
        ]
    }

    mock_service.get_rds_instances.assert_called_once()


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


@patch("backend.app.api.router.ResourceService")
def test_s3_resources_error(mock_resource_service):
    mock_service = mock_resource_service.return_value

    mock_service.get_s3_buckets.side_effect = RuntimeError(
        "Unable to retrieve S3 resources"
    )

    response = client.get("/api/v1/resources/s3")

    assert response.status_code == 200
    assert response.json() == {
        "status": "error",
        "message": "Unable to retrieve S3 resources",
    }

    mock_service.get_s3_buckets.assert_called_once()


@patch("backend.app.api.router.ResourceService")
def test_rds_resources_error(mock_resource_service):
    mock_service = mock_resource_service.return_value

    mock_service.get_rds_instances.side_effect = RuntimeError(
        "Unable to retrieve RDS resources"
    )

    response = client.get("/api/v1/resources/rds")

    assert response.status_code == 200
    assert response.json() == {
        "status": "error",
        "message": "Unable to retrieve RDS resources",
    }

    mock_service.get_rds_instances.assert_called_once()


@patch("backend.app.api.router.ResourceService")
def test_ec2_resources_error(mock_resource_service):
    mock_service = mock_resource_service.return_value

    mock_service.get_ec2_instances.side_effect = RuntimeError(
        "Unable to retrieve EC2 resources"
    )

    response = client.get("/api/v1/resources/ec2")

    assert response.status_code == 200
    assert response.json() == {
        "status": "error",
        "message": "Unable to retrieve EC2 resources",
    }

    mock_service.get_ec2_instances.assert_called_once()


@patch("backend.app.services.resource_service.boto3.client")
def test_start_ec2_instance(mock_boto_client):
    mock_ec2 = MagicMock()

    mock_boto_client.side_effect = [
        mock_ec2,
        MagicMock(),
        MagicMock(),
    ]

    service = ResourceService()

    result = service.start_ec2_instance("i-1234567890abcdef0")

    mock_ec2.start_instances.assert_called_once_with(
        InstanceIds=["i-1234567890abcdef0"]
    )

    assert result == {
        "instance_id": "i-1234567890abcdef0",
        "action": "start",
        "status": "initiated",
    }


@patch("backend.app.services.resource_service.boto3.client")
def test_stop_ec2_instance(mock_boto_client):
    mock_ec2 = MagicMock()

    mock_boto_client.side_effect = [
        mock_ec2,
        MagicMock(),
        MagicMock(),
    ]

    service = ResourceService()

    result = service.stop_ec2_instance("i-1234567890abcdef0")

    mock_ec2.stop_instances.assert_called_once_with(
        InstanceIds=["i-1234567890abcdef0"]
    )

    assert result == {
        "instance_id": "i-1234567890abcdef0",
        "action": "stop",
        "status": "initiated",
    }


@patch("backend.app.services.resource_service.boto3.client")
def test_reboot_ec2_instance(mock_boto_client):
    mock_ec2 = MagicMock()

    mock_boto_client.side_effect = [
        mock_ec2,
        MagicMock(),
        MagicMock(),
    ]

    service = ResourceService()

    result = service.reboot_ec2_instance("i-1234567890abcdef0")

    mock_ec2.reboot_instances.assert_called_once_with(
        InstanceIds=["i-1234567890abcdef0"]
    )

    assert result == {
        "instance_id": "i-1234567890abcdef0",
        "action": "reboot",
        "status": "initiated",
    }


@patch("backend.app.api.router.ResourceService")
def test_start_ec2_instance_api(mock_resource_service):
    mock_service = mock_resource_service.return_value

    mock_service.start_ec2_instance.return_value = {
        "instance_id": "i-1234567890abcdef0",
        "action": "start",
        "status": "initiated",
    }

    response = client.post(
        "/api/v1/resources/ec2/i-1234567890abcdef0/start"
    )

    assert response.status_code == 200
    assert response.json() == {
        "instance_id": "i-1234567890abcdef0",
        "action": "start",
        "status": "initiated",
    }

    mock_service.start_ec2_instance.assert_called_once_with(
        "i-1234567890abcdef0"
    )


@patch("backend.app.api.router.ResourceService")
def test_stop_ec2_instance_api(mock_resource_service):
    mock_service = mock_resource_service.return_value

    mock_service.stop_ec2_instance.return_value = {
        "instance_id": "i-1234567890abcdef0",
        "action": "stop",
        "status": "initiated",
    }

    response = client.post(
        "/api/v1/resources/ec2/i-1234567890abcdef0/stop"
    )

    assert response.status_code == 200
    assert response.json() == {
        "instance_id": "i-1234567890abcdef0",
        "action": "stop",
        "status": "initiated",
    }

    mock_service.stop_ec2_instance.assert_called_once_with(
        "i-1234567890abcdef0"
    )


@patch("backend.app.api.router.ResourceService")
def test_reboot_ec2_instance_api(mock_resource_service):
    mock_service = mock_resource_service.return_value

    mock_service.reboot_ec2_instance.return_value = {
        "instance_id": "i-1234567890abcdef0",
        "action": "reboot",
        "status": "initiated",
    }

    response = client.post(
        "/api/v1/resources/ec2/i-1234567890abcdef0/reboot"
    )

    assert response.status_code == 200
    assert response.json() == {
        "instance_id": "i-1234567890abcdef0",
        "action": "reboot",
        "status": "initiated",
    }

    mock_service.reboot_ec2_instance.assert_called_once_with(
        "i-1234567890abcdef0"
    )

@patch("backend.app.api.router.ResourceService")
def test_start_ec2_instance_api_error(mock_resource_service):
    mock_service = mock_resource_service.return_value

    mock_service.start_ec2_instance.side_effect = RuntimeError(
        "Unable to start EC2 instance"
    )

    response = client.post(
        "/api/v1/resources/ec2/i-1234567890abcdef0/start"
    )

    assert response.status_code == 200
    assert response.json() == {
        "status": "error",
        "message": "Unable to start EC2 instance",
    }

    mock_service.start_ec2_instance.assert_called_once_with(
        "i-1234567890abcdef0"
    )


@patch("backend.app.api.router.ResourceService")
def test_stop_ec2_instance_api_error(mock_resource_service):
    mock_service = mock_resource_service.return_value

    mock_service.stop_ec2_instance.side_effect = RuntimeError(
        "Unable to stop EC2 instance"
    )

    response = client.post(
        "/api/v1/resources/ec2/i-1234567890abcdef0/stop"
    )

    assert response.status_code == 200
    assert response.json() == {
        "status": "error",
        "message": "Unable to stop EC2 instance",
    }

    mock_service.stop_ec2_instance.assert_called_once_with(
        "i-1234567890abcdef0"
    )


@patch("backend.app.api.router.ResourceService")
def test_reboot_ec2_instance_api_error(mock_resource_service):
    mock_service = mock_resource_service.return_value

    mock_service.reboot_ec2_instance.side_effect = RuntimeError(
        "Unable to reboot EC2 instance"
    )

    response = client.post(
        "/api/v1/resources/ec2/i-1234567890abcdef0/reboot"
    )

    assert response.status_code == 200
    assert response.json() == {
        "status": "error",
        "message": "Unable to reboot EC2 instance",
    }

    mock_service.reboot_ec2_instance.assert_called_once_with(
        "i-1234567890abcdef0"
    )