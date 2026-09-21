import boto3

from backend.aws.config import AWS_REGION


class ResourceService:
    """Service layer for AWS resource management operations."""

    def __init__(self):
        self.ec2 = boto3.client("ec2", region_name=AWS_REGION)
        self.rds = boto3.client("rds", region_name=AWS_REGION)
        self.s3 = boto3.client("s3", region_name=AWS_REGION)

    def get_ec2_instances(self):
        """Retrieve EC2 instances from the configured AWS region."""
        response = self.ec2.describe_instances()

        instances = []

        for reservation in response.get("Reservations", []):
            for instance in reservation.get("Instances", []):
                instances.append(
                    {
                        "instance_id": instance.get("InstanceId"),
                        "instance_type": instance.get("InstanceType"),
                        "state": instance.get("State", {}).get("Name"),
                        "private_ip": instance.get("PrivateIpAddress"),
                        "public_ip": instance.get("PublicIpAddress"),
                    }
                )

        return instances
