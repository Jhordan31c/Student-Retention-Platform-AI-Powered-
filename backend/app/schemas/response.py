"""
📤 Response Schemas
Modelos Pydantic para responses de la API
"""

from pydantic import BaseModel, Field
from typing import Dict, List, Any


class PredictionResponse(BaseModel):
    """Respuesta de predicción individual"""
    prediction: str = Field(..., description="Clase predicha: Dropout, Enrolled, o Graduate")
    probabilities: Dict[str, float] = Field(..., description="Probabilidades por clase")
    dropout_probability: float = Field(..., description="Probabilidad específica de deserción")
    risk_level: str = Field(..., description="Nivel de riesgo: MUY BAJO, BAJO, MEDIO, ALTO")
    risk_color: str = Field(..., description="Color para UI: green, yellow, orange, red")
    recommendation: str = Field(..., description="Recomendación de acción")
    insights: List[str] = Field(default=[], description="Hallazgos clave detectados")
    timestamp: str = Field(..., description="Timestamp ISO de la predicción")
    
    model_config = {
        "json_schema_extra": {
            "examples": [{
                "prediction": "Dropout",
                "probabilities": {
                    "Dropout": 0.85,
                    "Enrolled": 0.10,
                    "Graduate": 0.05
                },
                "dropout_probability": 0.85,
                "risk_level": "ALTO",
                "risk_color": "red",
                "recommendation": "🚨 INTERVENCIÓN URGENTE: Estudiante en riesgo crítico de deserción",
                "insights": [
                    "Matrícula atrasada: Factor crítico de riesgo financiero.",
                    "Bajo rendimiento en 1er semestre."
                ],
                "timestamp": "2025-10-23T15:30:00.000000"
            }]
        }
    }


class BatchPredictionResponse(BaseModel):
    """Respuesta de predicción por lotes"""
    predictions: List[PredictionResponse] = Field(..., description="Lista de predicciones")
    total_students: int = Field(..., description="Total de estudiantes procesados")
    high_risk_count: int = Field(..., description="Cantidad en riesgo alto (≥70%)")
    medium_risk_count: int = Field(..., description="Cantidad en riesgo medio (50-70%)")
    timestamp: str = Field(..., description="Timestamp del procesamiento")


class HealthResponse(BaseModel):
    """Respuesta del health check"""
    status: str = Field(..., description="Estado: 'healthy' o 'unhealthy'")
    timestamp: str = Field(..., description="Timestamp del check")
    model_loaded: bool = Field(..., description="¿Modelo ML cargado correctamente?")
    pipeline_loaded: bool = Field(..., description="¿Pipeline cargado correctamente?")
    
    model_config = {
        "json_schema_extra": {
            "examples": [{
                "status": "healthy",
                "timestamp": "2025-10-23T15:30:00.000000",
                "model_loaded": True,
                "pipeline_loaded": True
            }]
        }
    }


class ModelMetricsResponse(BaseModel):
    """Respuesta con métricas del modelo"""
    model_name: str = Field(..., description="Nombre del modelo (ej: CatBoost, LightGBM)")
    trained_date: str = Field(..., description="Fecha de entrenamiento")
    metrics: Dict[str, float] = Field(..., description="Métricas del modelo")
    dataset_info: Dict[str, Any] = Field(..., description="Información del dataset")
    
    model_config = {
        "json_schema_extra": {
            "examples": [{
                "model_name": "CatBoost",
                "trained_date": "2025-10-08T22:59:12",
                "metrics": {
                    "accuracy": 0.7446,
                    "f1_macro": 0.6917,
                    "dropout_recall": 0.8451,
                    "dropout_precision": 0.7385,
                    "dropout_f1": 0.7882
                },
                "dataset_info": {
                    "training_samples": 3539,
                    "test_samples": 885,
                    "n_features": 181
                }
            }]
        }
    }