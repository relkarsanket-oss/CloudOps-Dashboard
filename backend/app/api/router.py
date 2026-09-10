from fastapi import APIRouter

from backend.aws.services import get_sts_client
from backend.app.services.monitoring_service import get_monitoring_data

router = APIRouter()


@router.get("/health")
def health_check():
    return {"status": "healthy"}


api_v1_router = APIRouter(prefix="/api/v1")


@api_v1_router.get("/status")
def api_status():
    return {
        "service": "CloudOps Dashboard API",
        "version": "v1",
        "status": "operational",
    }


@api_v1_router.get("/aws/status")
def aws_status():
    sts_client = get_sts_client()
    identity = sts_client.get_caller_identity()

    return {
        "service": "AWS",
        "status": "connected",
        "account_id": identity["Account"],
        "arn": identity["Arn"],
    }


@api_v1_router.get("/monitoring")
def monitoring():
    return get_monitoring_data()


router.include_router(api_v1_router)
