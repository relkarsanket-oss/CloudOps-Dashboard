from backend.aws.services import (
    get_ec2_instances,
    get_s3_buckets,
    get_rds_instances,
)


def get_monitoring_data():
    """Retrieve monitoring data from all configured AWS services."""
    return {
        "ec2": get_ec2_instances(),
        "s3": get_s3_buckets(),
        "rds": get_rds_instances(),
    }