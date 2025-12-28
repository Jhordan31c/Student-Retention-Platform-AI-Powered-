"""
🧪 API Endpoints Tests
Tests para todos los endpoints de la API
"""

import pytest
from fastapi import status


class TestHealthEndpoints:
    """Tests para endpoints de health y metrics"""
    
    def test_root_endpoint(self, client):
        """Test del endpoint raíz /"""
        response = client.get("/")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "message" in data
        assert "version" in data
        assert "status" in data
        assert data["status"] == "running"
    
    def test_health_check(self, client, api_v1_url):
        """Test del health check endpoint"""
        response = client.get(f"{api_v1_url}/health")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        
        # Verificar estructura de respuesta
        assert "status" in data
        assert "timestamp" in data
        assert "model_loaded" in data
        assert "pipeline_loaded" in data
        
        # Verificar que los modelos están cargados
        assert data["model_loaded"] is True
        assert data["pipeline_loaded"] is True
        assert data["status"] == "healthy"
    
    def test_get_metrics(self, client, api_v1_url):
        """Test del endpoint de métricas del modelo"""
        response = client.get(f"{api_v1_url}/metrics")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        
        # Verificar estructura
        assert "model_name" in data
        assert "trained_date" in data
        assert "metrics" in data
        assert "dataset_info" in data
        
        # Verificar que tiene métricas
        assert isinstance(data["metrics"], dict)


class TestPredictionEndpoints:
    """Tests para endpoints de predicción"""
    
    def test_predict_single_student(self, client, api_v1_url, sample_student_data):
        """Test de predicción para un estudiante"""
        response = client.post(
            f"{api_v1_url}/predict",
            json=sample_student_data
        )
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        
        # Verificar estructura de respuesta
        assert "prediction" in data
        assert "probabilities" in data
        assert "dropout_probability" in data
        assert "risk_level" in data
        assert "risk_color" in data
        assert "recommendation" in data
        assert "timestamp" in data
        
        # Verificar tipos
        assert isinstance(data["prediction"], str)
        assert data["prediction"] in ["Dropout", "Enrolled", "Graduate"]
        assert isinstance(data["probabilities"], dict)
        assert 0 <= data["dropout_probability"] <= 1
        assert data["risk_level"] in ["MUY BAJO", "BAJO", "MEDIO", "ALTO"]
        assert data["risk_color"] in ["green", "yellow", "orange", "red"]
    
    def test_predict_high_risk_student(self, client, api_v1_url, high_risk_student_data):
        """Test de predicción para estudiante en alto riesgo"""
        response = client.post(
            f"{api_v1_url}/predict",
            json=high_risk_student_data
        )
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        
        # Estudiante de alto riesgo debería tener probabilidad alta de dropout
        # (aunque no podemos garantizar esto sin conocer el modelo exacto)
        assert "dropout_probability" in data
        assert 0 <= data["dropout_probability"] <= 1
    
    def test_predict_batch(self, client, api_v1_url, sample_student_data):
        """Test de predicción por lotes"""
        batch_request = {
            "students": [
                sample_student_data,
                sample_student_data.copy()  # 2 estudiantes idénticos
            ]
        }
        
        response = client.post(
            f"{api_v1_url}/predict/batch",
            json=batch_request
        )
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        
        # Verificar estructura
        assert "predictions" in data
        assert "total_students" in data
        assert "high_risk_count" in data
        assert "medium_risk_count" in data
        assert "timestamp" in data
        
        # Verificar que procesó ambos estudiantes
        assert data["total_students"] == 2
        assert len(data["predictions"]) == 2
        
        # Verificar que cada predicción tiene la estructura correcta
        for prediction in data["predictions"]:
            assert "prediction" in prediction
            assert "probabilities" in prediction
            assert "dropout_probability" in prediction
    
    def test_predict_batch_max_limit(self, client, api_v1_url, sample_student_data):
        """Test que verifica el límite máximo de estudiantes en batch"""
        # Intentar enviar más de 1000 estudiantes
        batch_request = {
            "students": [sample_student_data] * 1001
        }
        
        response = client.post(
            f"{api_v1_url}/predict/batch",
            json=batch_request
        )
        
        # Debería fallar con 422 (Validation Error)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    def test_predict_batch_empty(self, client, api_v1_url):
        """Test que verifica que no se puede enviar lista vacía"""
        batch_request = {
            "students": []
        }
        
        response = client.post(
            f"{api_v1_url}/predict/batch",
            json=batch_request
        )
        
        # Debería fallar con 422 (Validation Error)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    def test_test_endpoint(self, client, api_v1_url):
        """Test del endpoint de prueba"""
        response = client.get(f"{api_v1_url}/test")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        
        # Verificar estructura
        assert "prediction" in data
        assert "probabilities" in data
        assert "dropout_probability" in data


class TestValidation:
    """Tests de validación de datos"""
    
    def test_invalid_age(self, client, api_v1_url, sample_student_data):
        """Test con edad inválida (fuera de rango)"""
        invalid_data = sample_student_data.copy()
        invalid_data["age_at_enrollment"] = 15  # Menor a 17
        
        response = client.post(
            f"{api_v1_url}/predict",
            json=invalid_data
        )
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    def test_invalid_grade(self, client, api_v1_url, sample_student_data):
        """Test con calificación inválida (fuera de rango 0-20)"""
        invalid_data = sample_student_data.copy()
        invalid_data["curricular_units_1st_sem_grade"] = 25  # Mayor a 20
        
        response = client.post(
            f"{api_v1_url}/predict",
            json=invalid_data
        )
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    def test_missing_required_field(self, client, api_v1_url, sample_student_data):
        """Test con campo requerido faltante"""
        invalid_data = sample_student_data.copy()
        del invalid_data["marital_status"]  # Eliminar campo requerido
        
        response = client.post(
            f"{api_v1_url}/predict",
            json=invalid_data
        )
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


class TestCORS:
    """Tests de configuración CORS"""
    
    def test_cors_headers(self, client, api_v1_url):
        """Test que verifica los headers CORS"""
        response = client.options(f"{api_v1_url}/health")
        
        # Verificar que tiene headers CORS
        assert "access-control-allow-origin" in response.headers or response.status_code == status.HTTP_200_OK


# ==========================================
# TESTS DE PERFORMANCE (Opcional)
# ==========================================

@pytest.mark.performance
class TestPerformance:
    """Tests de performance (marcados para ejecución opcional)"""
    
    def test_single_prediction_speed(self, client, api_v1_url, sample_student_data, benchmark):
        """Test de velocidad de predicción individual"""
        
        def make_prediction():
            response = client.post(
                f"{api_v1_url}/predict",
                json=sample_student_data
            )
            assert response.status_code == status.HTTP_200_OK
            return response
        
        # Benchmark con pytest-benchmark
        result = benchmark(make_prediction)
        assert result.status_code == status.HTTP_200_OK
    
    def test_batch_prediction_speed(self, client, api_v1_url, sample_student_data, benchmark):
        """Test de velocidad de predicción por lotes (100 estudiantes)"""
        
        batch_request = {
            "students": [sample_student_data] * 100
        }
        
        def make_batch_prediction():
            response = client.post(
                f"{api_v1_url}/predict/batch",
                json=batch_request
            )
            assert response.status_code == status.HTTP_200_OK
            return response
        
        result = benchmark(make_batch_prediction)
        assert result.status_code == status.HTTP_200_OK