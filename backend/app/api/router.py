from fastapi import APIRouter

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


router.include_router(api_v1_router)
