import boto3
from botocore.exceptions import ClientError

from backend.aws.config import AWS_REGION


class ResourceService:
    """Service layer for AWS resource management operations."""

    def __init__(self):
        self.ec2 = boto3.client("ec2", region_name=AWS_REGION)
        self.rds = boto3.client("rds", region_name=AWS_REGION)
        self.s3 = boto3.client("s3", region_name=AWS_REGION)

    def get_ec2_instances(self):
        """Retrieve EC2 instances from the configured AWS region."""
        try:
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

        except ClientError as exc:
            raise RuntimeError(
                "Unable to retrieve EC2 resources"
            ) from exc

    def start_ec2_instance(self, instance_id):
        """Start an EC2 instance."""
        try:
            self.ec2.start_instances(InstanceIds=[instance_id])

            return {
                "instance_id": instance_id,
                "action": "start",
                "status": "initiated",
            }

        except ClientError as exc:
            raise RuntimeError(
                "Unable to start EC2 instance"
            ) from exc

    def stop_ec2_instance(self, instance_id):
        """Stop an EC2 instance."""
        try:
            self.ec2.stop_instances(InstanceIds=[instance_id])

            return {
                "instance_id": instance_id,
                "action": "stop",
                "status": "initiated",
            }

        except ClientError as exc:
            raise RuntimeError(
                "Unable to stop EC2 instance"
            ) from exc

    def reboot_ec2_instance(self, instance_id):
        """Reboot an EC2 instance."""
        try:
            self.ec2.reboot_instances(InstanceIds=[instance_id])

            return {
                "instance_id": instance_id,
                "action": "reboot",
                "status": "initiated",
            }

        except ClientError as exc:
            raise RuntimeError(
                "Unable to reboot EC2 instance"
            ) from exc


    def get_rds_instances(self):
        """Retrieve RDS instances from the configured AWS region."""
        try:
            response = self.rds.describe_db_instances()

            instances = []

            for instance in response.get("DBInstances", []):
                instances.append(
                    {
                        "db_instance_identifier": instance.get(
                            "DBInstanceIdentifier"
                        ),
                        "engine": instance.get("Engine"),
                        "status": instance.get("DBInstanceStatus"),
                        "instance_class": instance.get("DBInstanceClass"),
                        "endpoint": instance.get("Endpoint", {}).get("Address"),
                    }
                )

            return instances

        except ClientError as exc:
            raise RuntimeError(
                "Unable to retrieve RDS resources"
            ) from exc

    def start_rds_instance(self, db_instance_identifier):
        """Start an RDS database instance."""
        try:
            self.rds.start_db_instance(
                DBInstanceIdentifier=db_instance_identifier
            )

            return {
                "db_instance_identifier": db_instance_identifier,
                "action": "start",
                "status": "initiated",
            }

        except ClientError as exc:
            raise RuntimeError(
                "Unable to start RDS instance"
            ) from exc

    def stop_rds_instance(self, db_instance_identifier):
        """Stop an RDS database instance."""
        try:
            self.rds.stop_db_instance(
                DBInstanceIdentifier=db_instance_identifier
            )

            return {
                "db_instance_identifier": db_instance_identifier,
                "action": "stop",
                "status": "initiated",
            }

        except ClientError as exc:
            raise RuntimeError(
                "Unable to stop RDS instance"
            ) from exc

    def reboot_rds_instance(self, db_instance_identifier):
        """Reboot an RDS database instance."""
        try:
            self.rds.reboot_db_instance(
                DBInstanceIdentifier=db_instance_identifier
            )

            return {
                "db_instance_identifier": db_instance_identifier,
                "action": "reboot",
                "status": "initiated",
            }

        except ClientError as exc:
            raise RuntimeError(
                "Unable to reboot RDS instance"
            ) from exc

    def get_s3_buckets(self):
        """Retrieve S3 buckets available to the AWS account."""
        try:
            response = self.s3.list_buckets()

            buckets = []

            for bucket in response.get("Buckets", []):
                buckets.append(
                    {
                        "name": bucket.get("Name"),
                        "creation_date": bucket.get("CreationDate"),
                    }
                )

            return buckets

        except ClientError as exc:
            raise RuntimeError(
                "Unable to retrieve S3 resources"
            ) from exc
