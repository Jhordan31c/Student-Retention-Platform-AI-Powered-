"""
📝 Request Schemas
Modelos Pydantic para validación de requests
"""

from pydantic import BaseModel, Field, field_validator
from typing import List


class StudentData(BaseModel):
    """
    Datos de un estudiante para predicción (35 features)
    """
    # Datos demográficos y de aplicación
    marital_status: int = Field(..., ge=1, le=6, description="Estado civil (1-6)")
    application_mode: int = Field(..., ge=1, description="Modo de aplicación")
    application_order: int = Field(..., ge=0, description="Orden de aplicación")
    course: int = Field(..., ge=1, description="ID del curso")
    daytime_evening_attendance: int = Field(..., ge=0, le=1, description="0=Nocturno, 1=Diurno")
    previous_qualification: int = Field(..., ge=1, description="Calificación previa")
    previous_qualification_grade: float = Field(..., ge=0, le=200, description="Nota previa (0-200)")
    admission_grade: float = Field(..., ge=0, le=200, description="Nota admisión (0-200)")
    nationality: int = Field(..., ge=1, description="Código de nacionalidad")
    mothers_qualification: int = Field(..., ge=1, description="Nivel educativo madre")
    fathers_qualification: int = Field(..., ge=1, description="Nivel educativo padre")
    mothers_occupation: int = Field(..., ge=0, description="Código ocupación madre")
    fathers_occupation: int = Field(..., ge=0, description="Código ocupación padre")
    displaced: int = Field(..., ge=0, le=1, description="¿Es desplazado? 0=No, 1=Sí")
    educational_special_needs: int = Field(..., ge=0, le=1, description="¿Necesidades especiales?")
    debtor: int = Field(..., ge=0, le=1, description="¿Tiene deudas? 0=No, 1=Sí")
    tuition_fees_up_to_date: int = Field(..., ge=0, le=1, description="¿Matrícula al día?")
    gender: int = Field(..., ge=0, le=1, description="0=Femenino, 1=Masculino")
    scholarship_holder: int = Field(..., ge=0, le=1, description="¿Tiene beca?")
    age_at_enrollment: int = Field(..., ge=17, le=70, description="Edad al inscribirse")
    international: int = Field(..., ge=0, le=1, description="¿Es internacional?")
    
    # Unidades curriculares 1er semestre
    curricular_units_1st_sem_credited: int = Field(..., ge=0, description="Unidades acreditadas")
    curricular_units_1st_sem_enrolled: int = Field(..., ge=0, description="Unidades inscritas")
    curricular_units_1st_sem_evaluations: int = Field(..., ge=0, description="Número de evaluaciones")
    curricular_units_1st_sem_approved: int = Field(..., ge=0, description="Unidades aprobadas")
    curricular_units_1st_sem_grade: float = Field(..., ge=0, le=20, description="Promedio (0-20)")
    curricular_units_1st_sem_without_evaluations: int = Field(..., ge=0, description="Sin evaluaciones")
    
    # Unidades curriculares 2do semestre
    curricular_units_2nd_sem_credited: int = Field(..., ge=0, description="Unidades acreditadas")
    curricular_units_2nd_sem_enrolled: int = Field(..., ge=0, description="Unidades inscritas")
    curricular_units_2nd_sem_evaluations: int = Field(..., ge=0, description="Número de evaluaciones")
    curricular_units_2nd_sem_approved: int = Field(..., ge=0, description="Unidades aprobadas")
    curricular_units_2nd_sem_grade: float = Field(..., ge=0, le=20, description="Promedio (0-20)")
    curricular_units_2nd_sem_without_evaluations: int = Field(..., ge=0, description="Sin evaluaciones")
    
    # Indicadores macroeconómicos
    unemployment_rate: float = Field(..., description="Tasa de desempleo (%)")
    inflation_rate: float = Field(..., description="Tasa de inflación (%)")
    gdp: float = Field(..., description="PIB")
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "marital_status": 1,
                    "application_mode": 1,
                    "application_order": 1,
                    "course": 33,
                    "daytime_evening_attendance": 1,
                    "previous_qualification": 1,
                    "previous_qualification_grade": 130.0,
                    "admission_grade": 125.0,
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
            ]
        }
    }


class BatchPredictionRequest(BaseModel):
    """Request para predicción por lotes"""
    students: List[StudentData] = Field(..., description="Lista de estudiantes (máx 1000)")
    
    @field_validator('students')
    @classmethod
    def validate_batch_size(cls, v):
        if len(v) > 1000:
            raise ValueError("Máximo 1000 estudiantes por lote")
        if len(v) == 0:
            raise ValueError("Debe incluir al menos un estudiante")
        return v