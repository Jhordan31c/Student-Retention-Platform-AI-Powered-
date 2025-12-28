"""
💚 Health Check Endpoints
Endpoints para verificar el estado de la API y obtener métricas del modelo
"""

from fastapi import APIRouter, Depends
from datetime import datetime

from app.schemas.response import HealthResponse, ModelMetricsResponse
from app.api.deps import MetadataDep
from app.core.lifespan import MLModels

router = APIRouter()


@router.get(
    "/health",
    response_model=HealthResponse,
    summary="Health Check",
    description="Verifica que la API y los modelos ML estén funcionando correctamente"
)
async def health_check() -> HealthResponse:
    """
    Health check endpoint
    
    Retorna el estado de la API y si los modelos están cargados
    """
    return HealthResponse(
        status="healthy" if (MLModels.model and MLModels.pipeline) else "unhealthy",
        timestamp=datetime.now().isoformat(),
        model_loaded=MLModels.model is not None,
        pipeline_loaded=MLModels.pipeline is not None
    )


@router.get(
    "/metrics",
    response_model=ModelMetricsResponse,
    summary="Model Metrics",
    description="Obtiene las métricas de performance del modelo ML entrenado"
)
async def get_model_metrics(
    metadata: MetadataDep
) -> ModelMetricsResponse:
    """
    Obtiene las métricas del modelo entrenado
    
    Args:
        metadata: Metadata del modelo (inyectada por dependency)
    
    Returns:
        ModelMetricsResponse con información del modelo y métricas
    """
    return ModelMetricsResponse(
        model_name=metadata.get('model_name', 'Unknown'),
        trained_date=metadata.get('trained_date', 'Unknown'),
        metrics=metadata.get('metrics', {}),
        dataset_info=metadata.get('dataset', {})
    )


@router.get(
    "/",
    summary="API Root",
    description="Endpoint raíz con información de la API"
)
async def root():
    """
    Root endpoint - Información básica de la API
    """
    return {
        "message": "🎓 API de Predicción de Deserción Estudiantil",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs",
        "health": "/api/v1/health",
        "metrics": "/api/v1/metrics"
    }