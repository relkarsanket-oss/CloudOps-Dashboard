import boto3

from backend.aws.config import AWS_REGION


def get_sts_client():
    return boto3.client("sts", region_name=AWS_REGION)


def get_ec2_client():
    return boto3.client("ec2", region_name=AWS_REGION)


def get_s3_client():
    return boto3.client("s3", region_name=AWS_REGION)

def get_rds_client():
    return boto3.client("rds", region_name=AWS_REGION)

def get_ec2_instances():
    ec2 = get_ec2_client()

    response = ec2.describe_instances()

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
                    "availability_zone": instance.get("Placement", {}).get(
                        "AvailabilityZone"
                    ),
                }
            )

    return instances


def get_s3_buckets():
    s3 = get_s3_client()

    response = s3.list_buckets()

    buckets = []

    for bucket in response.get("Buckets", []):
        buckets.append(
            {
                "name": bucket.get("Name"),
                "creation_date": bucket.get("CreationDate"),
            }
        )

    return buckets

def get_rds_instances():
    rds = get_rds_client()

    response = rds.describe_db_instances()

    instances = []

    for db_instance in response.get("DBInstances", []):
        instances.append(
            {
                "identifier": db_instance.get("DBInstanceIdentifier"),
                "engine": db_instance.get("Engine"),
                "engine_version": db_instance.get("EngineVersion"),
                "status": db_instance.get("DBInstanceStatus"),
                "instance_class": db_instance.get("DBInstanceClass"),
                "availability_zone": db_instance.get("AvailabilityZone"),
                "endpoint": db_instance.get("Endpoint", {}).get("Address"),
                "port": db_instance.get("Endpoint", {}).get("Port"),
            }
        )

    return instances
