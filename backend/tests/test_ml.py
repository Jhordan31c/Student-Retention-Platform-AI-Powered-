"""
🧪 ML Pipeline Tests
Tests para el pipeline de Machine Learning
"""

import pytest
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder

from app.ml.feature_engineering import FeatureEngineer
from app.ml.inference import (
    create_student_dataframe,
    calculate_risk_level,
    predict_student,
    COLUMN_MAPPING
)
from app.schemas.request import StudentData


class TestFeatureEngineering:
    """Tests para FeatureEngineer"""
    
    def test_feature_engineer_init(self):
        """Test de inicialización del FeatureEngineer"""
        fe = FeatureEngineer()
        assert fe is not None
    
    def test_feature_engineer_fit(self):
        """Test del método fit"""
        fe = FeatureEngineer()
        
        # Datos de prueba
        df = pd.DataFrame({
            'Age at enrollment': [18, 20, 25, 30, 22]
        })
        
        fe.fit(df)
        
        # Verificar que calculó la mediana
        assert hasattr(fe, 'median_age_')
        assert fe.median_age_ == 22  # Mediana de [18, 20, 22, 25, 30]
    
    def test_feature_engineer_transform(self):
        """Test del método transform"""
        fe = FeatureEngineer()
        
        # Datos de prueba con todas las columnas necesarias
        df = pd.DataFrame({
            'Age at enrollment': [20],
            'Curricular units 1st sem (grade)': [15.0],
            'Curricular units 2nd sem (grade)': [16.0],
            'Curricular units 1st sem (enrolled)': [6],
            'Curricular units 1st sem (approved)': [5],
            'Curricular units 2nd sem (enrolled)': [6],
            'Curricular units 2nd sem (approved)': [5],
            'Curricular units 1st sem (evaluations)': [6],
            'Curricular units 2nd sem (evaluations)': [6],
            'Curricular units 1st sem (without evaluations)': [0],
            'Curricular units 2nd sem (without evaluations)': [0],
            'Tuition fees up to date': [1],
            'Debtor': [0],
            'Scholarship holder': [1]
        })
        
        # Fit y transform
        fe.fit(df)
        df_transformed = fe.transform(df)
        
        # Verificar que se crearon nuevas features
        assert 'avg_grade_overall' in df_transformed.columns
        assert 'approval_rate_overall' in df_transformed.columns
        assert 'total_approved' in df_transformed.columns
        assert 'risk_score' in df_transformed.columns
        assert 'socioeconomic_index' in df_transformed.columns
        
        # Verificar algunos cálculos
        assert df_transformed['avg_grade_overall'].iloc[0] == 15.5  # (15+16)/2
        assert df_transformed['total_approved'].iloc[0] == 10  # 5+5
    
    def test_feature_engineer_get_feature_names(self):
        """Test del método get_feature_names_out"""
        fe = FeatureEngineer()
        
        feature_names = fe.get_feature_names_out()
        
        # Verificar que retorna una lista
        assert isinstance(feature_names, list)
        assert len(feature_names) > 0
        
        # Verificar que incluye algunas features conocidas
        assert 'avg_grade_overall' in feature_names
        assert 'risk_score' in feature_names


class TestInference:
    """Tests para funciones de inferencia"""
    
    def test_create_student_dataframe(self, sample_student_data):
        """Test de creación de DataFrame desde StudentData"""
        student = StudentData(**sample_student_data)
        df = create_student_dataframe(student)
        
        # Verificar que es un DataFrame
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 1
        
        # Verificar que las columnas fueron renombradas correctamente
        assert 'Marital status' in df.columns
        assert 'Age at enrollment' in df.columns
        assert 'Curricular units 1st sem (grade)' in df.columns
        
        # Verificar que no tiene columnas con nombres de API
        assert 'marital_status' not in df.columns
        assert 'age_at_enrollment' not in df.columns
    
    def test_calculate_risk_level_high(self):
        """Test de cálculo de riesgo ALTO"""
        result = calculate_risk_level(0.85)
        
        assert result["risk_level"] == "ALTO"
        assert result["risk_color"] == "red"
        assert "URGENTE" in result["recommendation"]
    
    def test_calculate_risk_level_medium(self):
        """Test de cálculo de riesgo MEDIO"""
        result = calculate_risk_level(0.60)
        
        assert result["risk_level"] == "MEDIO"
        assert result["risk_color"] == "orange"
        assert "ATENCIÓN" in result["recommendation"]
    
    def test_calculate_risk_level_low(self):
        """Test de cálculo de riesgo BAJO"""
        result = calculate_risk_level(0.40)
        
        assert result["risk_level"] == "BAJO"
        assert result["risk_color"] == "yellow"
        assert "PRECAUCIÓN" in result["recommendation"]
    
    def test_calculate_risk_level_very_low(self):
        """Test de cálculo de riesgo MUY BAJO"""
        result = calculate_risk_level(0.15)
        
        assert result["risk_level"] == "MUY BAJO"
        assert result["risk_color"] == "green"
        assert "BIEN" in result["recommendation"]
    
    def test_column_mapping_complete(self):
        """Test que verifica que el mapeo de columnas está completo"""
        # Verificar que tiene las 35 features
        assert len(COLUMN_MAPPING) == 35
        
        # Verificar algunas columnas clave
        assert 'marital_status' in COLUMN_MAPPING
        assert 'age_at_enrollment' in COLUMN_MAPPING
        assert 'curricular_units_1st_sem_grade' in COLUMN_MAPPING


class TestDataValidation:
    """Tests de validación de datos"""
    
    def test_student_data_validation_success(self, sample_student_data):
        """Test de validación exitosa de StudentData"""
        student = StudentData(**sample_student_data)
        
        assert student is not None
        assert student.age_at_enrollment == 20
        assert student.marital_status == 1
    
    def test_student_data_validation_age_min(self, sample_student_data):
        """Test de validación de edad mínima"""
        invalid_data = sample_student_data.copy()
        invalid_data["age_at_enrollment"] = 16  # Menor a 17
        
        with pytest.raises(Exception):  # Pydantic ValidationError
            StudentData(**invalid_data)
    
    def test_student_data_validation_age_max(self, sample_student_data):
        """Test de validación de edad máxima"""
        invalid_data = sample_student_data.copy()
        invalid_data["age_at_enrollment"] = 75  # Mayor a 70
        
        with pytest.raises(Exception):
            StudentData(**invalid_data)
    
    def test_student_data_validation_grade_range(self, sample_student_data):
        """Test de validación de rango de calificaciones"""
        invalid_data = sample_student_data.copy()
        invalid_data["curricular_units_1st_sem_grade"] = 25  # Mayor a 20
        
        with pytest.raises(Exception):
            StudentData(**invalid_data)