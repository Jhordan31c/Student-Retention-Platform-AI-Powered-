"""
🔀 API v1 Router
Agrupa todos los endpoints de la versión 1 de la API
"""

from fastapi import APIRouter

from app.api.v1.endpoints import health, predictions

# Router principal de API v1
api_router = APIRouter()

# Incluir routers de cada módulo
api_router.include_router(
    health.router,
    tags=["Health"]
)

api_router.include_router(
    predictions.router,
    tags=["Predictions"]
)