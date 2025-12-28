"""
🔧 Feature Engineering Module
Contiene la clase FeatureEngineer usada en el preprocessing pipeline
"""

import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin


class FeatureEngineer(BaseEstimator, TransformerMixin):
    """
    Transformer personalizado para feature engineering.
    Aplica todas las transformaciones definidas en el Día 3.
    
    Este transformer debe ser compatible con el pipeline guardado
    en preprocessing_pipeline.pkl
    """
    
    def __init__(self):
        pass
    
    def fit(self, X, y=None):
        """
        Aprende la mediana de edad del training set
        """
        # Calcular mediana de edad en training set
        self.median_age_ = X['Age at enrollment'].median()
        return self
    
    def transform(self, X):
        """
        Aplica feature engineering a los datos
        """
        X = X.copy()
        
        # ==========================================
        # 1. FEATURES ACADÉMICAS
        # ==========================================
        
        # Promedio de calificaciones
        X['avg_grade_overall'] = (
            X['Curricular units 1st sem (grade)'] + 
            X['Curricular units 2nd sem (grade)']
        ) / 2
        
        # Tasa de aprobación general
        X['approval_rate_overall'] = (
            np.where(
                X['Curricular units 1st sem (enrolled)'] > 0,
                X['Curricular units 1st sem (approved)'] / X['Curricular units 1st sem (enrolled)'],
                0
            ) +
            np.where(
                X['Curricular units 2nd sem (enrolled)'] > 0,
                X['Curricular units 2nd sem (approved)'] / X['Curricular units 2nd sem (enrolled)'],
                0
            )
        ) / 2
        
        # Total de materias aprobadas
        X['total_approved'] = (
            X['Curricular units 1st sem (approved)'] + 
            X['Curricular units 2nd sem (approved)']
        )
        
        # Mejora en calificaciones (2do sem - 1er sem)
        X['grade_improvement'] = (
            X['Curricular units 2nd sem (grade)'] - 
            X['Curricular units 1st sem (grade)']
        )
        
        # Tasa de aprobación por semestre
        X['approval_rate_1st'] = np.where(
            X['Curricular units 1st sem (enrolled)'] > 0,
            X['Curricular units 1st sem (approved)'] / X['Curricular units 1st sem (enrolled)'],
            0
        )
        
        X['approval_rate_2nd'] = np.where(
            X['Curricular units 2nd sem (enrolled)'] > 0,
            X['Curricular units 2nd sem (approved)'] / X['Curricular units 2nd sem (enrolled)'],
            0
        )
        
        # Promedio de calificaciones por semestre
        X['avg_grade_1st'] = X['Curricular units 1st sem (grade)']
        X['avg_grade_2nd'] = X['Curricular units 2nd sem (grade)']
        
        # Ratio de evaluaciones vs inscritas
        X['evaluation_rate_1st'] = np.where(
            X['Curricular units 1st sem (enrolled)'] > 0,
            X['Curricular units 1st sem (evaluations)'] / X['Curricular units 1st sem (enrolled)'],
            0
        )
        
        X['evaluation_rate_2nd'] = np.where(
            X['Curricular units 2nd sem (enrolled)'] > 0,
            X['Curricular units 2nd sem (evaluations)'] / X['Curricular units 2nd sem (enrolled)'],
            0
        )
        
        # Total de unidades inscritas
        X['total_enrolled'] = (
            X['Curricular units 1st sem (enrolled)'] +
            X['Curricular units 2nd sem (enrolled)']
        )
        
        # Tasa de éxito en evaluaciones
        X['success_rate_1st'] = np.where(
            X['Curricular units 1st sem (evaluations)'] > 0,
            X['Curricular units 1st sem (approved)'] / X['Curricular units 1st sem (evaluations)'],
            0
        )
        
        X['success_rate_2nd'] = np.where(
            X['Curricular units 2nd sem (evaluations)'] > 0,
            X['Curricular units 2nd sem (approved)'] / X['Curricular units 2nd sem (evaluations)'],
            0
        )
        
        # ==========================================
        # 2. FEATURES DE RIESGO
        # ==========================================
        
        # Regla de detección temprana: <4 aprobadas Y <11 promedio en 1er sem
        X['at_risk_1st_sem'] = (
            (X['Curricular units 1st sem (approved)'] < 4) & 
            (X['Curricular units 1st sem (grade)'] < 11)
        ).astype(int)
        
        # Rendimiento muy bajo en ambos semestres
        X['very_low_performance'] = (
            (X['Curricular units 1st sem (grade)'] < 10) & 
            (X['Curricular units 2nd sem (grade)'] < 10)
        ).astype(int)
        
        # Sin progreso (0 aprobadas en ambos semestres)
        X['no_progress'] = (
            (X['Curricular units 1st sem (approved)'] == 0) & 
            (X['Curricular units 2nd sem (approved)'] == 0)
        ).astype(int)
        
        # Score de riesgo compuesto
        X['risk_score'] = (
            (X['at_risk_1st_sem'] * 3) +
            (X['very_low_performance'] * 2) +
            (X['no_progress'] * 2) +
            ((X['approval_rate_overall'] < 0.5).astype(int) * 1)
        )
        
        # Riesgo de abandono temprano
        X['early_dropout_risk'] = (
            (X['Curricular units 1st sem (approved)'] == 0)
        ).astype(int)
        
        # Deterioro en rendimiento
        X['performance_deterioration'] = (
            X['grade_improvement'] < -2
        ).astype(int)
        
        # ==========================================
        # 3. FEATURES ECONÓMICAS
        # ==========================================
        
        # Índice socioeconómico compuesto
        X['socioeconomic_index'] = (
            X['Tuition fees up to date'] * 2 +
            (1 - X['Debtor']) +
            X['Scholarship holder']
        ) / 4
        
        # Riesgo económico (tiene deudas Y matrícula atrasada)
        X['economic_risk'] = (
            (X['Tuition fees up to date'] == 0) & 
            (X['Debtor'] == 1)
        ).astype(int)
        
        # Soporte financiero (beca O matrícula al día)
        X['has_financial_support'] = (
            (X['Scholarship holder'] == 1) | 
            (X['Tuition fees up to date'] == 1)
        ).astype(int)
        
        # Situación económica crítica
        X['critical_economic_situation'] = (
            (X['Debtor'] == 1) & 
            (X['Scholarship holder'] == 0) & 
            (X['Tuition fees up to date'] == 0)
        ).astype(int)
        
        # ==========================================
        # 4. FEATURES DEMOGRÁFICAS
        # ==========================================
        
        # Desviación de edad respecto a la mediana
        X['age_deviation'] = X['Age at enrollment'] - self.median_age_
        
        # Estudiante maduro (>25 años)
        X['is_mature_student'] = (X['Age at enrollment'] > 25).astype(int)
        
        return X
    
    def get_feature_names_out(self, input_features=None):
        """
        Retorna los nombres de las features generadas
        """
        # Features originales más las nuevas features
        new_features = [
            'avg_grade_overall', 'approval_rate_overall', 'total_approved',
            'grade_improvement', 'approval_rate_1st', 'approval_rate_2nd',
            'avg_grade_1st', 'avg_grade_2nd', 'evaluation_rate_1st',
            'evaluation_rate_2nd', 'total_enrolled', 'success_rate_1st',
            'success_rate_2nd', 'at_risk_1st_sem', 'very_low_performance',
            'no_progress', 'risk_score', 'early_dropout_risk',
            'performance_deterioration', 'socioeconomic_index', 'economic_risk',
            'has_financial_support', 'critical_economic_situation',
            'age_deviation', 'is_mature_student'
        ]
        
        if input_features is not None:
            return list(input_features) + new_features
        else:
            return new_features