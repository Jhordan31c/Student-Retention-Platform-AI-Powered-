"""
🔮 Inference Module
Lógica centralizada para realizar predicciones
"""

import pandas as pd
from datetime import datetime
from typing import Dict, Any

from app.schemas.request import StudentData


# Mapeo de nombres de columnas: API -> Dataset
COLUMN_MAPPING = {
    'marital_status': 'Marital status',
    'application_mode': 'Application mode',
    'application_order': 'Application order',
    'course': 'Course',
    'daytime_evening_attendance': 'Daytime/evening attendance\t',
    'previous_qualification': 'Previous qualification',
    'previous_qualification_grade': 'Previous qualification (grade)',
    'admission_grade': 'Admission grade',
    'nationality': 'Nacionality',
    'mothers_qualification': "Mother's qualification",
    'fathers_qualification': "Father's qualification",
    'mothers_occupation': "Mother's occupation",
    'fathers_occupation': "Father's occupation",
    'displaced': 'Displaced',
    'educational_special_needs': 'Educational special needs',
    'debtor': 'Debtor',
    'tuition_fees_up_to_date': 'Tuition fees up to date',
    'gender': 'Gender',
    'scholarship_holder': 'Scholarship holder',
    'age_at_enrollment': 'Age at enrollment',
    'international': 'International',
    'curricular_units_1st_sem_credited': 'Curricular units 1st sem (credited)',
    'curricular_units_1st_sem_enrolled': 'Curricular units 1st sem (enrolled)',
    'curricular_units_1st_sem_evaluations': 'Curricular units 1st sem (evaluations)',
    'curricular_units_1st_sem_approved': 'Curricular units 1st sem (approved)',
    'curricular_units_1st_sem_grade': 'Curricular units 1st sem (grade)',
    'curricular_units_1st_sem_without_evaluations': 'Curricular units 1st sem (without evaluations)',
    'curricular_units_2nd_sem_credited': 'Curricular units 2nd sem (credited)',
    'curricular_units_2nd_sem_enrolled': 'Curricular units 2nd sem (enrolled)',
    'curricular_units_2nd_sem_evaluations': 'Curricular units 2nd sem (evaluations)',
    'curricular_units_2nd_sem_approved': 'Curricular units 2nd sem (approved)',
    'curricular_units_2nd_sem_grade': 'Curricular units 2nd sem (grade)',
    'curricular_units_2nd_sem_without_evaluations': 'Curricular units 2nd sem (without evaluations)',
    'unemployment_rate': 'Unemployment rate',
    'inflation_rate': 'Inflation rate',
    'gdp': 'GDP'
}


def create_student_dataframe(student: StudentData) -> pd.DataFrame:
    """
    Convierte StudentData a DataFrame con nombres de columnas correctos
    
    Args:
        student: Datos del estudiante (Pydantic model)
    
    Returns:
        DataFrame con una fila y columnas renombradas
    """
    # Convertir a dict
    student_dict = student.model_dump()
    
    # Crear DataFrame
    df = pd.DataFrame([student_dict])
    
    # Renombrar columnas al formato del dataset original
    df = df.rename(columns=COLUMN_MAPPING)
    
    return df


def calculate_risk_level(dropout_prob: float) -> Dict[str, str]:
    """
    Calcula el nivel de riesgo y recomendación basado en probabilidad de dropout
    
    Args:
        dropout_prob: Probabilidad de deserción (0-1)
    
    Returns:
        Dict con risk_level, risk_color y recommendation
    """
    if dropout_prob >= 0.7:
        return {
            "risk_level": "ALTO",
            "risk_color": "red",
            "recommendation": "🚨 INTERVENCIÓN URGENTE: Estudiante en riesgo crítico de deserción. "
                            "Se requiere acción inmediata del equipo de retención."
        }
    elif dropout_prob >= 0.5:
        return {
            "risk_level": "MEDIO",
            "risk_color": "orange",
            "recommendation": "⚠️ ATENCIÓN: Monitorear de cerca y ofrecer apoyo académico. "
                            "Considerar tutoría y seguimiento personalizado."
        }
    elif dropout_prob >= 0.3:
        return {
            "risk_level": "BAJO",
            "risk_color": "yellow",
            "recommendation": "⚡ PRECAUCIÓN: Mantener seguimiento preventivo. "
                            "Reforzar aspectos identificados como debilidades."
        }
    else:
        return {
            "risk_level": "MUY BAJO",
            "risk_color": "green",
            "recommendation": "✅ BIEN: Estudiante con buen pronóstico académico. "
                            "Continuar con seguimiento estándar."
        }


from loguru import logger

def extract_insights(df: pd.DataFrame) -> list[str]:
    """
    Identifica factores críticos de riesgo basados en los datos crudos
    """
    insights = []
    
    # Heurísticas basadas en los hallazgos del EDA
    if df['Tuition fees up to date'].iloc[0] == 0:
        insights.append("Matrícula atrasada: Factor crítico de riesgo financiero.")
    
    if df['Debtor'].iloc[0] == 1:
        insights.append("Situación de deuda: El estudiante tiene pagos pendientes.")
        
    if df['Curricular units 1st sem (approved)'].iloc[0] < (df['Curricular units 1st sem (enrolled)'].iloc[0] / 2):
        insights.append("Bajo rendimiento en 1er semestre: Aprobó menos de la mitad de materias.")

    if df['Curricular units 2nd sem (grade)'].iloc[0] < 10:
        insights.append("Calificación crítica: Promedio por debajo del umbral de aprobación en 2do semestre.")
        
    if df['Scholarship holder'].iloc[0] == 0 and df['Debtor'].iloc[0] == 1:
        insights.append("Sin apoyo financiero: El estudiante no tiene beca y presenta deudas.")

    if not insights:
        insights.append("No se detectaron factores de riesgo inmediatos en las variables principales.")
        
    return insights


def predict_student(
    df: pd.DataFrame,
    model: Any,
    pipeline: Any,
    label_encoder: Any
) -> Dict[str, Any]:
    """
    Realiza predicción para un estudiante
    """
    try:
        # 1. Aplicar feature engineering
        df_transformed = pipeline.transform(df)
        
        # 2. Hacer predicción
        prediction = model.predict(df_transformed)[0]
        probabilities = model.predict_proba(df_transformed)[0]
        
        # 3. Decodificar predicción
        prediction_label = label_encoder.inverse_transform([prediction])[0]
        
        # 4. Crear dict de probabilidades por clase
        class_probabilities = {
            label_encoder.classes_[i]: float(prob)
            for i, prob in enumerate(probabilities)
        }
        
        # 5. Obtener probabilidad de Dropout
        dropout_prob = class_probabilities.get('Dropout', 0.0)
        
        # 6. Calcular nivel de riesgo y recomendación
        risk_info = calculate_risk_level(dropout_prob)
        
        # 7. Extraer Insights
        insights = extract_insights(df)
        
        # 8. Construir resultado
        result = {
            "prediction": prediction_label,
            "probabilities": class_probabilities,
            "dropout_probability": dropout_prob,
            "risk_level": risk_info["risk_level"],
            "risk_color": risk_info["risk_color"],
            "recommendation": risk_info["recommendation"],
            "insights": insights,
            "timestamp": datetime.now().isoformat()
        }
        
        return result
    except Exception as e:
        logger.error(f"🔥 Error en predict_student: {str(e)}")
        raise e