"""
🧪 Pytest Configuration & Fixtures
Configuración global de pytest y fixtures compartidos
"""

import pytest
import sys
from pathlib import Path
from fastapi.testclient import TestClient

# Agregar el directorio app al path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.main import app
from app.core.config import settings


@pytest.fixture(scope="session")
def test_app():
    """
    Fixture que proporciona la aplicación FastAPI para testing
    """
    return app


@pytest.fixture(scope="session")
def client(test_app):
    """
    Fixture que proporciona un cliente de test sincrónico
    
    Scope: session - Se crea una sola vez para todas las pruebas
    """
    with TestClient(test_app) as test_client:
        yield test_client


@pytest.fixture(scope="session")
def api_v1_url():
    """
    Fixture que proporciona la URL base de API v1
    """
    return settings.API_V1_STR


@pytest.fixture
def sample_student_data():
    """
    Fixture con datos de ejemplo de un estudiante
    """
    return {
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


@pytest.fixture
def high_risk_student_data():
    """
    Fixture con datos de un estudiante en alto riesgo
    """
    return {
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
        "debtor": 1,  # Tiene deudas
        "tuition_fees_up_to_date": 0,  # No está al día
        "gender": 1,
        "scholarship_holder": 0,  # Sin beca
        "age_at_enrollment": 20,
        "international": 0,
        "curricular_units_1st_sem_credited": 0,
        "curricular_units_1st_sem_enrolled": 6,
        "curricular_units_1st_sem_evaluations": 6,
        "curricular_units_1st_sem_approved": 2,  # Solo 2/6
        "curricular_units_1st_sem_grade": 9.5,  # Bajo
        "curricular_units_1st_sem_without_evaluations": 0,
        "curricular_units_2nd_sem_credited": 0,
        "curricular_units_2nd_sem_enrolled": 6,
        "curricular_units_2nd_sem_evaluations": 6,
        "curricular_units_2nd_sem_approved": 3,  # Solo 3/6
        "curricular_units_2nd_sem_grade": 10.2,  # Bajo
        "curricular_units_2nd_sem_without_evaluations": 0,
        "unemployment_rate": 10.8,
        "inflation_rate": 1.4,
        "gdp": 1.74
    }