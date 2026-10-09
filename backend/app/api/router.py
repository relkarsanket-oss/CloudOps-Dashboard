from fastapi import APIRouter

from backend.app.models.monitoring import MonitoringData, MonitoringError
from backend.app.models.resources import ResourceError, ResourceResponse
from backend.aws.services import get_sts_client
from backend.app.services.monitoring_service import get_monitoring_data
from backend.app.services.resource_service import ResourceService


router = APIRouter()


@router.get("/health", tags=["Health"])
def health_check():
    return {"status": "healthy"}


api_v1_router = APIRouter(prefix="/api/v1")


@api_v1_router.get("/status", tags=["API"])
def api_status():
    return {
        "service": "CloudOps Dashboard API",
        "version": "v1",
        "status": "operational",
    }


@api_v1_router.get("/aws/status", tags=["AWS"])
def aws_status():
    sts_client = get_sts_client()
    identity = sts_client.get_caller_identity()

    return {
        "service": "AWS",
        "status": "connected",
        "account_id": identity["Account"],
        "arn": identity["Arn"],
    }


@api_v1_router.get(
    "/monitoring",
    response_model=MonitoringData | MonitoringError,
    tags=["Monitoring"],
)
def monitoring():
    try:
        return get_monitoring_data()
    except Exception:
        return {
            "status": "error",
            "message": "Unable to retrieve monitoring data",
        }


@api_v1_router.get(
    "/resources/ec2",
    response_model=ResourceResponse | ResourceError,
    tags=["Resources"],
    summary="List EC2 instances",
    description="Retrieve EC2 instances from the configured AWS region.",
)
def ec2_resources():
    service = ResourceService()

    try:
        return {
            "resources": service.get_ec2_instances()
        }
    except RuntimeError:
        return {
            "status": "error",
            "message": "Unable to retrieve EC2 resources",
        }


@api_v1_router.get(
    "/resources/rds",
    response_model=ResourceResponse | ResourceError,
    tags=["Resources"],
    summary="List RDS instances",
    description="Retrieve RDS database instances from the configured AWS region.",
)
def rds_resources():
    service = ResourceService()

    try:
        return {
            "resources": service.get_rds_instances()
        }
    except RuntimeError:
        return {
            "status": "error",
            "message": "Unable to retrieve RDS resources",
        }


@api_v1_router.get(
    "/resources/s3",
    response_model=ResourceResponse | ResourceError,
    tags=["Resources"],
    summary="List S3 buckets",
    description="Retrieve S3 buckets available to the AWS account.",
)
def get_s3_resources():
    """Retrieve S3 buckets available to the AWS account."""
    service = ResourceService()

    try:
        return {
            "resources": service.get_s3_buckets()
        }
    except RuntimeError:
        return {
            "status": "error",
            "message": "Unable to retrieve S3 resources",
        }


@api_v1_router.post("/resources/ec2/{instance_id}/start")
def start_ec2_instance(instance_id: str):
    service = ResourceService()

    try:
        return service.start_ec2_instance(instance_id)
    except RuntimeError as exc:
        return {
            "status": "error",
            "message": str(exc),
        }


@api_v1_router.post("/resources/ec2/{instance_id}/stop")
def stop_ec2_instance(instance_id: str):
    service = ResourceService()

    try:
        return service.stop_ec2_instance(instance_id)
    except RuntimeError as exc:
        return {
            "status": "error",
            "message": str(exc),
        }


@api_v1_router.post("/resources/ec2/{instance_id}/reboot")
def reboot_ec2_instance(instance_id: str):
    service = ResourceService()

    try:
        return service.reboot_ec2_instance(instance_id)
    except RuntimeError as exc:
        return {
            "status": "error",
            "message": str(exc),
        }


@api_v1_router.post("/resources/rds/{db_instance_identifier}/start")
def start_rds_instance(db_instance_identifier: str):
    service = ResourceService()

    try:
        return service.start_rds_instance(db_instance_identifier)
    except RuntimeError as exc:
        return {
            "status": "error",
            "message": str(exc),
        }


@api_v1_router.post("/resources/rds/{db_instance_identifier}/stop")
def stop_rds_instance(db_instance_identifier: str):
    service = ResourceService()

    try:
        return service.stop_rds_instance(db_instance_identifier)
    except RuntimeError as exc:
        return {
            "status": "error",
            "message": str(exc),
        }


@api_v1_router.post("/resources/rds/{db_instance_identifier}/reboot")
def reboot_rds_instance(db_instance_identifier: str):
    service = ResourceService()

    try:
        return service.reboot_rds_instance(db_instance_identifier)
    except RuntimeError as exc:
        return {
            "status": "error",
            "message": str(exc),
        }


router.include_router(api_v1_router)