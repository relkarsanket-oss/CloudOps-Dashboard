from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.api.router import router

tags_metadata = [
    {
        "name": "Health",
        "description": "Application health check endpoints.",
    },
    {
        "name": "API",
        "description": "General CloudOps Dashboard API information.",
    },
    {
        "name": "AWS",
        "description": "AWS connection and identity endpoints.",
    },
    {
        "name": "Monitoring",
        "description": "AWS infrastructure monitoring endpoints.",
    },
]

app = FastAPI(
    title="CloudOps Dashboard API",
    description="Backend API for the CloudOps Dashboard",
    version="1.0.0",
    openapi_tags=tags_metadata,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["null"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)
