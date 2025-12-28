"""
🔮 Prediction Endpoints
Endpoints para realizar predicciones de deserción estudiantil
"""

from fastapi import APIRouter, Depends, HTTPException, status
from datetime import datetime
import pandas as pd
import json
import hashlib
from loguru import logger

from app.schemas.request import StudentData, BatchPredictionRequest
from app.schemas.response import PredictionResponse, BatchPredictionResponse
from app.api.deps import MLModelDep, PipelineDep, LabelEncoderDep, RedisDep
from app.ml.inference import predict_student, create_student_dataframe
from app.ml.llm_explainer import GeminiExplainer

router = APIRouter()
llm_explainer = GeminiExplainer()  # Instancia global reutilizable


@router.post(
    "/predict",
    response_model=PredictionResponse,
    status_code=status.HTTP_200_OK,
    summary="Predict Single Student",
    description="Predice el riesgo de deserción para un estudiante individual (con caché e insights IA)"
)
async def predict_single_student(
    student: StudentData,
    model: MLModelDep,
    pipeline: PipelineDep,
    label_encoder: LabelEncoderDep,
    redis: RedisDep
) -> PredictionResponse:
    """
    Predice el riesgo de deserción para UN estudiante
    """
    try:
        # 1. Generar Cache Key
        student_json = student.model_dump_json()
        cache_key = f"pred:{hashlib.sha256(student_json.encode()).hexdigest()}"
        
        # 2. Consultar Caché
        cached_result = await redis.get(cache_key)
        if cached_result:
            logger.info(f"⚡ Cache Hit: {cache_key}")
            return PredictionResponse(**json.loads(cached_result))
            
        # Log de la petición (solo en desarrollo)
        logger.debug(f"📥 Predicción solicitada para estudiante")
        
        # Crear DataFrame desde los datos del estudiante
        df = create_student_dataframe(student)
        
        # Realizar predicción (incluye insights heurísticos básicos)
        result = predict_student(
            df=df,
            model=model,
            pipeline=pipeline,
            label_encoder=label_encoder
        )
        
        # 3. Enriquecer con Insights de LLM (Gemini)
        # Solo si el riesgo es medio o alto para ahorrar tokens/tiempo, o siempre si queremos impresionar
        if llm_explainer.model:
            logger.info("🤖 Generando explicación con Gemini...")
            llm_insights = await llm_explainer.generate_explanation(
                df=df,
                prediction_label=result['prediction'],
                probability=result['dropout_probability']
            )
            if llm_insights:
                result['insights'] = llm_insights
                logger.info("✨ Insights de IA generados correctamente")
        
        # 4. Guardar en Caché (1 hora)
        await redis.setex(cache_key, 3600, json.dumps(result))
        
        logger.info(
            f"✅ Predicción exitosa: {result['prediction']} "
            f"(Riesgo: {result['risk_level']}, Prob: {result['dropout_probability']:.2%})"
        )
        
        return PredictionResponse(**result)
        
    except Exception as e:
        logger.error(f"❌ Error en predicción: {str(e)}")
        import traceback
        traceback.print_exc()
        
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al realizar la predicción: {str(e)}"
        )


@router.post(
    "/predict/batch",
    response_model=BatchPredictionResponse,
    status_code=status.HTTP_200_OK,
    summary="Predict Multiple Students",
    description="Predice el riesgo de deserción para múltiples estudiantes (hasta 1000)"
)
async def predict_batch_students(
    request: BatchPredictionRequest,
    model: MLModelDep,
    pipeline: PipelineDep,
    label_encoder: LabelEncoderDep
) -> BatchPredictionResponse:
    """
    Predice el riesgo de deserción para MÚLTIPLES estudiantes
    
    Args:
        request: Lista de estudiantes (máx 1000)
        model: Modelo ML (inyectado)
        pipeline: Pipeline de preprocessing (inyectado)
        label_encoder: Label encoder (inyectado)
    
    Returns:
        BatchPredictionResponse con lista de predicciones y estadísticas
    
    Raises:
        HTTPException: Si ocurre un error en el procesamiento
    """
    try:
        logger.info(f"📥 Predicción batch solicitada para {len(request.students)} estudiantes")
        
        predictions = []
        
        # Procesar cada estudiante
        for idx, student in enumerate(request.students, 1):
            try:
                # Crear DataFrame
                df = create_student_dataframe(student)
                
                # Realizar predicción
                result = predict_student(
                    df=df,
                    model=model,
                    pipeline=pipeline,
                    label_encoder=label_encoder
                )
                
                predictions.append(PredictionResponse(**result))
                
                # Log de progreso cada 100 estudiantes
                if idx % 100 == 0:
                    logger.info(f"📊 Procesados {idx}/{len(request.students)} estudiantes")
                    
            except Exception as e:
                logger.error(f"❌ Error procesando estudiante {idx}: {str(e)}")
                # Continuar con el siguiente estudiante
                continue
        
        # Calcular estadísticas del batch
        high_risk_count = sum(
            1 for p in predictions 
            if p.dropout_probability >= 0.7
        )
        medium_risk_count = sum(
            1 for p in predictions 
            if 0.5 <= p.dropout_probability < 0.7
        )
        
        logger.success(
            f"✅ Batch completado: {len(predictions)}/{len(request.students)} exitosas. "
            f"Alto riesgo: {high_risk_count}, Medio riesgo: {medium_risk_count}"
        )
        
        return BatchPredictionResponse(
            predictions=predictions,
            total_students=len(predictions),
            high_risk_count=high_risk_count,
            medium_risk_count=medium_risk_count,
            timestamp=datetime.now().isoformat()
        )
        
    except Exception as e:
        logger.error(f"❌ Error en predicción batch: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al procesar el batch: {str(e)}"
        )


@router.get(
    "/test",
    response_model=PredictionResponse,
    summary="Test Prediction",
    description="Endpoint de prueba con datos de ejemplo (estudiante en riesgo)"
)
async def test_prediction(
    model: MLModelDep,
    pipeline: PipelineDep,
    label_encoder: LabelEncoderDep
) -> PredictionResponse:
    """
    Endpoint de prueba con datos de ejemplo
    
    Útil para verificar que la API está funcionando correctamente
    """
    # Estudiante de ejemplo en RIESGO
    test_student = StudentData(
        marital_status=1,
        application_mode=1,
        application_order=1,
        course=33,
        daytime_evening_attendance=1,
        previous_qualification=1,
        nationality=1,
        mothers_qualification=1,
        fathers_qualification=1,
        mothers_occupation=1,
        fathers_occupation=1,
        displaced=0,
        educational_special_needs=0,
        debtor=1,  # Tiene deudas
        tuition_fees_up_to_date=0,  # No está al día
        gender=1,
        scholarship_holder=0,  # Sin beca
        age_at_enrollment=20,
        international=0,
        curricular_units_1st_sem_credited=0,
        curricular_units_1st_sem_enrolled=6,
        curricular_units_1st_sem_evaluations=6,
        curricular_units_1st_sem_approved=2,  # Solo 2/6 aprobadas
        curricular_units_1st_sem_grade=9.5,  # Promedio bajo
        curricular_units_1st_sem_without_evaluations=0,
        curricular_units_2nd_sem_credited=0,
        curricular_units_2nd_sem_enrolled=6,
        curricular_units_2nd_sem_evaluations=6,
        curricular_units_2nd_sem_approved=3,  # Solo 3/6 aprobadas
        curricular_units_2nd_sem_grade=10.2,  # Promedio bajo
        curricular_units_2nd_sem_without_evaluations=0,
        unemployment_rate=10.8,
        inflation_rate=1.4,
        gdp=1.74
    )
    
    logger.info("🧪 Ejecutando predicción de prueba")
    
    # Reutilizar la lógica de predict_single_student
    df = create_student_dataframe(test_student)
    result = predict_student(
        df=df,
        model=model,
        pipeline=pipeline,
        label_encoder=label_encoder
    )
    
    return PredictionResponse(**result)