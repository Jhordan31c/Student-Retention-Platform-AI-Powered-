"""
🎓 Main Application
Entry point de la API FastAPI
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
import sys

from app.core.config import settings
from app.core.lifespan import lifespan
from app.api.v1.router import api_router

# ==========================================
# CONFIGURAR LOGGING
# ==========================================

# Configurar loguru
logger.remove()  # Remover handler por defecto
logger.add(
    sys.stdout,
    colorize=True,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <level>{message}</level>",
    level=settings.LOG_LEVEL
)

# Agregar logging a archivo si no es desarrollo
if settings.ENVIRONMENT != "development":
    logger.add(
        "logs/api_{time:YYYY-MM-DD}.log",
        rotation="00:00",  # Nueva archivo cada día
        retention="30 days",
        compression="zip",
        level=settings.LOG_LEVEL
    )

# ==========================================
# CREAR APLICACIÓN FASTAPI
# ==========================================

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description=(
        "API REST para predecir el riesgo de deserción estudiantil utilizando Machine Learning. "
        "Proporciona endpoints para predicciones individuales y por lotes, "
        "con análisis de riesgo y recomendaciones personalizadas."
    ),
    docs_url=settings.docs_url,
    redoc_url=settings.redoc_url,
    openapi_url=f"{settings.API_V1_STR}/openapi.json" if settings.docs_url else None,
    lifespan=lifespan,  # Lifecycle manager
)

# ==========================================
# MIDDLEWARES
# ==========================================

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==========================================
# ROUTERS
# ==========================================

# Incluir router principal de API v1
app.include_router(
    api_router,
    prefix=settings.API_V1_STR
)

# ==========================================
# ROOT ENDPOINT
# ==========================================

@app.get(
    "/",
    tags=["Root"],
    summary="API Root",
    description="Información básica de la API"
)
async def root():
    """
    Root endpoint - Información de bienvenida
    """
    return {
        "message": f"🎓 {settings.PROJECT_NAME}",
        "version": settings.VERSION,
        "environment": settings.ENVIRONMENT,
        "status": "running",
        "docs": settings.docs_url or "Disabled in production",
        "api_v1": f"{settings.API_V1_STR}",
        "endpoints": {
            "health": f"{settings.API_V1_STR}/health",
            "metrics": f"{settings.API_V1_STR}/metrics",
            "predict": f"{settings.API_V1_STR}/predict",
            "predict_batch": f"{settings.API_V1_STR}/predict/batch",
            "test": f"{settings.API_V1_STR}/test"
        }
    }


# ==========================================
# STARTUP EVENT (Opcional - ya está en lifespan)
# ==========================================

# Si necesitas agregar más lógica de startup, puedes usar:
# @app.on_event("startup")
# async def startup_event():
#     logger.info("Ejecutando tareas adicionales de startup...")


# ==========================================
# RUN APPLICATION
# ==========================================

if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level=settings.LOG_LEVEL.lower()
    )