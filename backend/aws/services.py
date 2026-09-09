import boto3

from backend.aws.config import AWS_REGION


def get_sts_client():
    return boto3.client("sts", region_name=AWS_REGION)


def get_ec2_client():
    return boto3.client("ec2", region_name=AWS_REGION)


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
