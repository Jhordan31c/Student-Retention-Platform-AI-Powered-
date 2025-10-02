"""
Health check endpoints
"""
from fastapi import APIRouter, status
from pydantic import BaseModel
from datetime import datetime
import sys

from app.core.config import settings

router = APIRouter()


class HealthResponse(BaseModel):
    """Health check response model"""
    status: str
    timestamp: datetime
    version: str
    environment: str
    python_version: str


class StatusResponse(BaseModel):
    """Detailed status response"""
    api: str
    database: str
    redis: str
    ml_model: str
    timestamp: datetime


@router.get(
    "/health",
    response_model=HealthResponse,
    status_code=status.HTTP_200_OK,
    summary="Health Check",
    description="Check if the API is running"
)
async def health_check() -> HealthResponse:
    """
    Basic health check endpoint
    
    Returns:
        HealthResponse: Current health status
    """
    return HealthResponse(
        status="healthy",
        timestamp=datetime.now(),
        version=settings.VERSION,
        environment=settings.ENVIRONMENT,
        python_version=f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    )


@router.get(
    "/status",
    response_model=StatusResponse,
    status_code=status.HTTP_200_OK,
    summary="Detailed Status",
    description="Check status of all services"
)
async def status_check() -> StatusResponse:
    """
    Detailed status check for all services
    
    Returns:
        StatusResponse: Status of all services
    """
    # TODO: Implement actual checks for database, redis, and model
    return StatusResponse(
        api="operational",
        database="not_configured",
        redis="not_configured",
        ml_model="not_loaded",
        timestamp=datetime.now()
    )
