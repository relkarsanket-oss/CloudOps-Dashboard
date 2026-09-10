from unittest.mock import patch

from backend.app.services.monitoring_service import get_monitoring_data


@patch("backend.app.services.monitoring_service.get_rds_instances")
@patch("backend.app.services.monitoring_service.get_s3_buckets")
@patch("backend.app.services.monitoring_service.get_ec2_instances")
def test_get_monitoring_data(
    mock_get_ec2_instances,
    mock_get_s3_buckets,
    mock_get_rds_instances,
):
    mock_get_ec2_instances.return_value = [{"id": "i-test"}]
    mock_get_s3_buckets.return_value = [{"name": "test-bucket"}]
    mock_get_rds_instances.return_value = [{"identifier": "test-db"}]

    result = get_monitoring_data()

    assert result == {
        "ec2": [{"id": "i-test"}],
        "s3": [{"name": "test-bucket"}],
        "rds": [{"identifier": "test-db"}],
    }

    mock_get_ec2_instances.assert_called_once()
    mock_get_s3_buckets.assert_called_once()
    mock_get_rds_instances.assert_called_once()
