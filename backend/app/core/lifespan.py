"""
🔄 Lifecycle Management
Maneja la carga y descarga de modelos ML al iniciar/cerrar la app
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
import json
from loguru import logger

from app.core.config import settings
from app.ml.model_loader import load_model
from app.core.redis import get_redis_pool, close_redis_pool


# Variables globales para modelos
class MLModels:
    """Contenedor global para modelos ML"""
    model = None
    pipeline = None
    label_encoder = None
    metadata = None


async def load_ml_models():
    """Carga todos los modelos ML necesarios usando el loader centralizado"""
    try:
        logger.info("=" * 70)
        logger.info(f"🚀 CARGANDO MODELOS ML - Environment: {settings.ENVIRONMENT}")
        logger.info("=" * 70)
        
        # Cargar todo desde model_loader.py
        model, pipeline, label_encoder = load_model()
        
        MLModels.model = model
        MLModels.pipeline = pipeline
        MLModels.label_encoder = label_encoder
        
        # Cargar metadata del modelo (opcional para logs)
        metadata_path = settings.models_dir / "model_metadata.json"
        if metadata_path.exists():
            with open(metadata_path, 'r') as f:
                MLModels.metadata = json.load(f)
        
        logger.info("=" * 70)
        logger.info("🎉 TODOS LOS MODELOS CARGADOS EXITOSAMENTE")
        logger.info("=" * 70)
        
        return True
        
    except Exception as e:
        logger.error(f"❌ ERROR CRÍTICO al cargar modelos: {e}")
        import traceback
        traceback.print_exc()
        raise


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager - Maneja startup y shutdown de la app
    """
    # ==========================================
    # STARTUP
    # ==========================================
    logger.info("=" * 70)
    logger.info(f"🚀 INICIANDO {settings.PROJECT_NAME} v{settings.VERSION}")
    logger.info("=" * 70)
    logger.info(f"🌍 Environment: {settings.ENVIRONMENT}")
    logger.info(f"🔧 Debug Mode: {settings.DEBUG}")
    logger.info(f"🗄️  Database: {settings.DATABASE_URL.split('@')[1] if '@' in settings.DATABASE_URL else 'Not configured'}")
    logger.info(f"📊 MLflow: {settings.MLFLOW_TRACKING_URI}")
    logger.info(f"📖 Docs: {settings.docs_url or 'Disabled'}")
    logger.info("=" * 70)
    
    # Inicializar Redis
    await get_redis_pool()
    
    # Cargar modelos ML
    await load_ml_models()
    
    logger.info("✅ API lista para recibir peticiones!")
    logger.info("=" * 70)
    
    yield  # La aplicación corre aquí
    
    # ==========================================
    # SHUTDOWN
    # ==========================================
    logger.info("=" * 70)
    logger.info("👋 Cerrando API...")
    logger.info("🧹 Liberando recursos...")
    
    # Cerrar Redis
    await close_redis_pool()
    
    # Limpiar modelos de memoria
    MLModels.model = None
    MLModels.pipeline = None
    MLModels.label_encoder = None
    MLModels.metadata = None
    
    logger.info("✅ Recursos liberados")
    logger.info("=" * 70)
