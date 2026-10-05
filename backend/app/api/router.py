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


router.include_router(api_v1_router)