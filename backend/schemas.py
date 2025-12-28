"""
🎓 Schemas de Pydantic para validación de datos
Define los modelos de entrada y salida de la API
"""

from pydantic import BaseModel, Field, validator
from typing import Dict, List, Optional
from datetime import datetime


class StudentData(BaseModel):
    """
    Datos de un estudiante para predicción (36 features)
    Corresponde a las columnas originales del dataset
    """
    # Datos demográficos y de aplicación
    marital_status: int = Field(..., ge=1, le=6, description="Estado civil")
    application_mode: int = Field(..., ge=1, description="Modo de aplicación")
    application_order: int = Field(..., ge=0, description="Orden de aplicación")
    course: int = Field(..., ge=1, description="ID del curso")
    daytime_evening_attendance: int = Field(..., ge=0, le=1, description="Asistencia diurna/nocturna")
    previous_qualification: int = Field(..., ge=1, description="Calificación previa")
    nationality: int = Field(..., ge=1, description="Nacionalidad")
    mothers_qualification: int = Field(..., ge=1, description="Calificación de la madre")
    fathers_qualification: int = Field(..., ge=1, description="Calificación del padre")
    mothers_occupation: int = Field(..., ge=0, description="Ocupación de la madre")
    fathers_occupation: int = Field(..., ge=0, description="Ocupación del padre")
    displaced: int = Field(..., ge=0, le=1, description="Desplazado")
    educational_special_needs: int = Field(..., ge=0, le=1, description="Necesidades educativas especiales")
    debtor: int = Field(..., ge=0, le=1, description="Es deudor")
    tuition_fees_up_to_date: int = Field(..., ge=0, le=1, description="Matrícula al día")
    gender: int = Field(..., ge=0, le=1, description="Género")
    scholarship_holder: int = Field(..., ge=0, le=1, description="Becario")
    age_at_enrollment: int = Field(..., ge=17, le=70, description="Edad al inscribirse")
    international: int = Field(..., ge=0, le=1, description="Estudiante internacional")
    
    # Unidades curriculares 1er semestre
    curricular_units_1st_sem_credited: int = Field(..., ge=0, description="Unidades acreditadas 1er sem")
    curricular_units_1st_sem_enrolled: int = Field(..., ge=0, description="Unidades inscritas 1er sem")
    curricular_units_1st_sem_evaluations: int = Field(..., ge=0, description="Evaluaciones 1er sem")
    curricular_units_1st_sem_approved: int = Field(..., ge=0, description="Unidades aprobadas 1er sem")
    curricular_units_1st_sem_grade: float = Field(..., ge=0, le=20, description="Calificación 1er sem")
    curricular_units_1st_sem_without_evaluations: int = Field(..., ge=0, description="Sin evaluaciones 1er sem")
    
    # Unidades curriculares 2do semestre
    curricular_units_2nd_sem_credited: int = Field(..., ge=0, description="Unidades acreditadas 2do sem")
    curricular_units_2nd_sem_enrolled: int = Field(..., ge=0, description="Unidades inscritas 2do sem")
    curricular_units_2nd_sem_evaluations: int = Field(..., ge=0, description="Evaluaciones 2do sem")
    curricular_units_2nd_sem_approved: int = Field(..., ge=0, description="Unidades aprobadas 2do sem")
    curricular_units_2nd_sem_grade: float = Field(..., ge=0, le=20, description="Calificación 2do sem")
    curricular_units_2nd_sem_without_evaluations: int = Field(..., ge=0, description="Sin evaluaciones 2do sem")
    
    # Indicadores macroeconómicos
    unemployment_rate: float = Field(..., description="Tasa de desempleo")
    inflation_rate: float = Field(..., description="Tasa de inflación")
    gdp: float = Field(..., description="PIB")
    
    class Config:
        json_schema_extra = {
            "example": {
                "marital_status": 1,
                "application_mode": 1,
                "application_order": 1,
                "course": 33,
                "daytime_evening_attendance": 1,
                "previous_qualification": 1,
                "nationality": 1,
                "mothers_qualification": 1,
                "fathers_qualification": 1,
                "mothers_occupation": 1,
                "fathers_occupation": 1,
                "displaced": 0,
                "educational_special_needs": 0,
                "debtor": 0,
                "tuition_fees_up_to_date": 1,
                "gender": 1,
                "scholarship_holder": 1,
                "age_at_enrollment": 20,
                "international": 0,
                "curricular_units_1st_sem_credited": 0,
                "curricular_units_1st_sem_enrolled": 6,
                "curricular_units_1st_sem_evaluations": 6,
                "curricular_units_1st_sem_approved": 5,
                "curricular_units_1st_sem_grade": 13.5,
                "curricular_units_1st_sem_without_evaluations": 0,
                "curricular_units_2nd_sem_credited": 0,
                "curricular_units_2nd_sem_enrolled": 6,
                "curricular_units_2nd_sem_evaluations": 6,
                "curricular_units_2nd_sem_approved": 5,
                "curricular_units_2nd_sem_grade": 14.0,
                "curricular_units_2nd_sem_without_evaluations": 0,
                "unemployment_rate": 10.8,
                "inflation_rate": 1.4,
                "gdp": 1.74
            }
        }


class PredictionResponse(BaseModel):
    """Respuesta de predicción para un estudiante"""
    prediction: str = Field(..., description="Clase predicha: Dropout, Enrolled, o Graduate")
    probabilities: Dict[str, float] = Field(..., description="Probabilidades por clase")
    dropout_probability: float = Field(..., description="Probabilidad de deserción")
    risk_level: str = Field(..., description="Nivel de riesgo: MUY BAJO, BAJO, MEDIO, ALTO")
    risk_color: str = Field(..., description="Color para UI: green, yellow, orange, red")
    recommendation: str = Field(..., description="Recomendación de acción")
    timestamp: str = Field(..., description="Timestamp de la predicción")
    
    class Config:
        json_schema_extra = {
            "example": {
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
                "timestamp": "2025-10-08T10:30:00"
            }
        }


class BatchPredictionRequest(BaseModel):
    """Request para predicción por lotes"""
    students: List[StudentData] = Field(..., description="Lista de estudiantes")
    
    @validator('students')
    def validate_batch_size(cls, v):
        if len(v) > 1000:
            raise ValueError("Máximo 1000 estudiantes por lote")
        if len(v) == 0:
            raise ValueError("Debe incluir al menos un estudiante")
        return v


class BatchPredictionResponse(BaseModel):
    """Respuesta de predicción por lotes"""
    predictions: List[PredictionResponse] = Field(..., description="Lista de predicciones")
    total_students: int = Field(..., description="Total de estudiantes procesados")
    high_risk_count: int = Field(..., description="Cantidad en riesgo alto")
    medium_risk_count: int = Field(..., description="Cantidad en riesgo medio")
    timestamp: str = Field(..., description="Timestamp del procesamiento")


class HealthResponse(BaseModel):
    """Respuesta del health check"""
    status: str = Field(..., description="Estado de la API")
    timestamp: str = Field(..., description="Timestamp del check")
    model_loaded: bool = Field(..., description="¿Modelo ML cargado?")
    pipeline_loaded: bool = Field(..., description="¿Pipeline cargado?")
    
    class Config:
        json_schema_extra = {
            "example": {
                "status": "healthy",
                "timestamp": "2025-10-08T10:30:00",
                "model_loaded": True,
                "pipeline_loaded": True
            }
        }


class ModelMetricsResponse(BaseModel):
    """Respuesta con métricas del modelo"""
    model_name: str = Field(..., description="Nombre del modelo")
    trained_date: str = Field(..., description="Fecha de entrenamiento")
    metrics: Dict[str, float] = Field(..., description="Métricas del modelo")
    dataset_info: Dict = Field(..., description="Información del dataset")
    
    class Config:
        json_schema_extra = {
            "example": {
                "model_name": "LightGBM",
                "trained_date": "2025-10-08T09:00:00",
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
                    "n_features": 80
                }
            }
        }