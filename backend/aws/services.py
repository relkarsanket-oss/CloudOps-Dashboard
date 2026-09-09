import boto3

from backend.aws.config import AWS_REGION


def get_sts_client():
    return boto3.client("sts", region_name=AWS_REGION)
