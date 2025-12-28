"""
🔌 Dependencies
Dependency Injection para endpoints - Proporciona acceso a modelos ML
"""

from typing import Annotated
from fastapi import Depends, HTTPException, status
import redis.asyncio as redis

from app.core.lifespan import MLModels
from app.core.redis import get_redis_pool


async def get_redis() -> redis.Redis:
    """
    Dependency que provee el cliente de Redis
    """
    return await get_redis_pool()


def get_ml_model():
    """
    Dependency que provee el modelo ML cargado
    
    Raises:
        HTTPException: Si el modelo no está cargado
    """
    if MLModels.model is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Modelo ML no está cargado. Por favor reinicia el servidor."
        )
    return MLModels.model


def get_pipeline():
    """
    Dependency que provee el pipeline de preprocessing
    
    Raises:
        HTTPException: Si el pipeline no está cargado
    """
    if MLModels.pipeline is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Pipeline de preprocessing no está cargado. Por favor reinicia el servidor."
        )
    return MLModels.pipeline


def get_label_encoder():
    """
    Dependency que provee el label encoder
    
    Raises:
        HTTPException: Si el label encoder no está cargado
    """
    if MLModels.label_encoder is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Label encoder no está cargado. Por favor reinicia el servidor."
        )
    return MLModels.label_encoder


def get_model_metadata():
    """
    Dependency que provee la metadata del modelo
    
    Raises:
        HTTPException: Si la metadata no está disponible
    """
    if MLModels.metadata is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Metadata del modelo no está disponible."
        )
    return MLModels.metadata


# Type hints para usar en endpoints
MLModelDep = Annotated[object, Depends(get_ml_model)]
PipelineDep = Annotated[object, Depends(get_pipeline)]
LabelEncoderDep = Annotated[object, Depends(get_label_encoder)]
MetadataDep = Annotated[dict, Depends(get_model_metadata)]
RedisDep = Annotated[redis.Redis, Depends(get_redis)]