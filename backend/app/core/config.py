"""
Application configuration using Pydantic Settings
"""
from typing import List
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings"""
    
    # Project Info
    PROJECT_NAME: str = "🎓 Predictor de Deserción Escolar"
    VERSION: str = "1.0.0"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    
    # Database
    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/predictor_db"
    
    # Redis
    REDIS_URL: str = "redis://default:redis123@localhost:6379/0"
    
    # Security
    SECRET_KEY: str = "your-secret-key-change-in-production-min-32-chars"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # CORS
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:8000",
    ]
    
    # MLflow
    MLFLOW_TRACKING_URI: str = "http://localhost:5000"
    MLFLOW_EXPERIMENT_NAME: str = "dropout-prediction"
    
    # API Configuration
    API_V1_STR: str = "/api/v1"
    RATE_LIMIT_PER_MINUTE: int = 60
    
    # Model Configuration
    MODEL_PATH: str = "ml/models"  # Path relativo desde backend/
    MODEL_VERSION: str = "latest"
    
    # Logging
    LOG_LEVEL: str = "INFO"
    
    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # Docs (agregado)
    SHOW_DOCS: bool = True
    
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
        extra="allow"
    )
    
    # ==========================================
    # COMPUTED PROPERTIES
    # ==========================================
    
    @property
    def base_dir(self) -> Path:
        """Directorio base del proyecto"""
        return Path(__file__).resolve().parent.parent.parent
    
    @property
    def models_dir(self) -> Path:
        """Directorio de modelos ML"""
        return self.base_dir / self.MODEL_PATH
    
    @property
    def docs_url(self) -> str | None:
        """URL de documentación Swagger"""
        if self.ENVIRONMENT == "production" and not self.SHOW_DOCS:
            return None
        return "/docs"
    
    @property
    def redoc_url(self) -> str | None:
        """URL de documentación ReDoc"""
        if self.ENVIRONMENT == "production" and not self.SHOW_DOCS:
            return None
        return "/redoc"


# Create global settings instance
settings = Settings()